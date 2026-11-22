"""Command-line interface for the Touhou osu! index."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import time
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, as_completed, wait
from datetime import date, timedelta
from pathlib import Path

from .catalog import IDENTITY_MISMATCH_MARKER, Catalog
from .classifier import normalize as normalize_text
from .http import HttpError, get_text
from .models import CatalogError, Entry
from .osu_api import MissingCredentials, OsuApi, entry_from_osu
from .provenance import demote_generic_verification_debt
from .site import build, statistics
from .sources import import_all, parse_beatmapset_page

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = ROOT / "data" / "catalog"
DEFAULT_CONFIG = ROOT / "config" / "seeds.json"
DEFAULT_OUTPUT = ROOT / "dist"
DISCOVERY_CONFIDENCE_ORDER = {"verified": 0, "probable": 1, "candidate": 2, "excluded": 3}
# Spend the weekly change budget on what reviewers care about first: unseen
# beatmapsets, then confidence transitions, then other metadata/evidence.
DISCOVERY_CHANGE_PRIORITY = {"new": 0, "confidence": 1, "metadata": 2}
RECONCILE_PROGRESS_INTERVAL = 500
RECONCILE_REVIEWED_IDENTITY_PREFIXES = (
    "audit:",
    "manual:",
    "provenance:",
)
RECONCILE_STRONG_IDENTITY_PREFIXES = (
    *RECONCILE_REVIEWED_IDENTITY_PREFIXES,
    "official_pack:",
    "official_pack_item:",
    "tmc:",
    "tournament:",
)
RECONCILE_STALE_IDENTITY_PREFIXES = (
    "audit:",
    "forum_queue:",
    "manual:",
    "official_pack:",
    "official_pack_item:",
    "provenance:",
    "tmc:",
    "tournament:",
    "tournament_candidate:",
)
RECONCILE_STALE_IDENTITY_EVIDENCE = {
    "known_touhou_artist",
    "known_touhou_metadata",
    "mapper_tags",
    "osu_source",
}


def load_catalog(path: Path) -> Catalog:
    return Catalog.load(path) if path.exists() else Catalog()


def load_config(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def print_stats(catalog: Catalog) -> None:
    stats = statistics(catalog)
    details = ", ".join(f"{key}={value}" for key, value in stats["confidence"].items())
    print(f"Catalog: {stats['total']} beatmapsets ({details}); accepted={stats['accepted']}")


def enforce_generic_source_policy(catalog: Catalog) -> int:
    """Demote automation-introduced generic-source verification debt and report it."""

    demoted = demote_generic_verification_debt(catalog)
    if demoted:
        print(
            f"warning: demoted {len(demoted)} generic-source verified rows without independent "
            "verification: " + ", ".join(map(str, demoted[:50])),
            file=sys.stderr,
        )
    return len(demoted)


def command_validate(args: argparse.Namespace) -> int:
    catalog = Catalog.load(args.catalog)
    catalog.validate()
    print_stats(catalog)
    return 0


def command_build(args: argparse.Namespace) -> int:
    catalog = Catalog.load(args.catalog)
    stats = build(catalog, args.output)
    print(f"Built {stats['accepted']} accepted beatmapsets to {args.output}")
    return 0


def command_assemble(args: argparse.Namespace) -> int:
    catalog = Catalog.load(args.catalog)
    catalog.save_aggregate(args.output)
    print(f"Assembled {len(catalog.entries)} beatmapsets to {args.output}")
    return 0


def command_clean(args: argparse.Namespace) -> int:
    if args.output.resolve() == Path("/"):
        raise RuntimeError("refusing to clean filesystem root")
    if args.output.exists():
        shutil.rmtree(args.output)
    print(f"Cleaned {args.output}")
    return 0


def command_import_seeds(args: argparse.Namespace) -> int:
    catalog = load_catalog(args.catalog)
    imported, reports = import_all(load_config(args.config), workers=args.workers)
    changed = 0
    for entry in imported:
        current = catalog.entries.get(entry.beatmapset_id)
        checked_on = entry.last_checked
        if current is not None:
            # Like discovery, seed import must not bump last_checked on rows it
            # does not otherwise change: reconciliation owns freshness and
            # refreshes the stalest rows first, so a date-only bump here would
            # push seed rows to the back of its queue without an osu! refresh.
            entry.last_checked = current.last_checked
        merged, did_change = catalog.merge(entry, fill_metadata_only=True)
        if did_change and current is not None:
            merged.last_checked = max(filter(None, (merged.last_checked, checked_on)))
        changed += did_change
    changed += enforce_generic_source_policy(catalog)
    for report in reports:
        print(report.message())
    print(f"Merged {len(imported)} source records; {changed} catalog entries changed")
    if args.write:
        catalog.save(args.catalog)
        print(f"Wrote {args.catalog}")
    print_stats(catalog)
    return 0


def command_audit_sources(args: argparse.Namespace) -> int:
    imported, reports = import_all(load_config(args.config), workers=args.workers)
    unique = len({entry.beatmapset_id for entry in imported})
    if args.json:
        print(
            json.dumps(
                {
                    "source_records": len(imported),
                    "unique_beatmapsets": unique,
                    "sources": [
                        {
                            "kind": report.kind,
                            "name": report.name,
                            "url": report.url,
                            "beatmapsets": report.beatmapsets,
                        }
                        for report in reports
                    ],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        for report in reports:
            print(report.message())
        print(f"Sources: {len(reports)}; records={len(imported)}; unique beatmapsets={unique}")
    return 0


def command_hydrate(args: argparse.Namespace) -> int:
    """Fill incomplete source records from public osu! beatmapset pages."""
    catalog = load_catalog(args.catalog)
    prefixes = (
        "forum_queue:",
        "tournament_candidate:",
        "tournament:google_sheet:",
        "official_pack:",
        "official_pack_item:",
    )
    pending = [
        entry
        for entry in catalog.entries.values()
        if any(item.startswith(prefixes) for item in entry.evidence)
        and (not entry.artist or not entry.title or not entry.source or entry.status == "unknown")
    ]
    demoted = 0
    for entry in pending:
        if "manual:verified" not in entry.evidence and any(
            item.startswith("forum_queue:") for item in entry.evidence
        ) and entry.confidence != "candidate":
            # A queue link proves relevance, but incomplete metadata should not
            # be published until the public beatmapset page has been resolved.
            entry.confidence = "candidate"
            demoted += 1
    pending.sort(
        key=lambda entry: (
            not any(item.startswith("forum_queue:") for item in entry.evidence),
            entry.beatmapset_id,
        )
    )
    if args.limit:
        pending = pending[: args.limit]

    def fetch(entry):
        raw = parse_beatmapset_page(get_text(f"https://osu.ppy.sh/beatmapsets/{entry.beatmapset_id}"))
        incoming = entry_from_osu(raw, evidence=entry.evidence, confidence=entry.confidence)
        incoming.touhou_kind = entry.touhou_kind
        incoming.origin_games = entry.origin_games
        incoming.original_themes = entry.original_themes
        return incoming

    changed = demoted
    failures: list[str] = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(fetch, entry): entry.beatmapset_id for entry in pending}
        for future in as_completed(futures):
            beatmapset_id = futures[future]
            try:
                incoming = future.result()
            except Exception as exc:  # keep deleted or temporarily unavailable sets reviewable
                failures.append(f"beatmapset {beatmapset_id}: {exc}")
                continue
            _, did_change = catalog.merge(incoming)
            changed += did_change
    changed += enforce_generic_source_policy(catalog)

    for failure in sorted(failures):
        print(f"warning: {failure}", file=sys.stderr)
    print(f"Hydrated {len(pending) - len(failures)} beatmapsets; {changed} entries changed")
    if args.write:
        catalog.save(args.catalog)
        print(f"Wrote {args.catalog}")
    print_stats(catalog)
    if failures and args.strict:
        return 1
    return 0


def command_discover(args: argparse.Namespace) -> int:
    if args.max_changes < 0:
        raise RuntimeError("--max-changes must be zero or greater")
    catalog = load_catalog(args.catalog)
    config = load_config(args.config)
    api = OsuApi.from_env()
    discovered: dict[int, dict] = {}
    discovery_evidence: dict[int, set[str]] = {}
    fuzzy_hits = 0
    for query in config.get("discovery_queries", []):
        for raw in api.search(query, max_pages=args.max_pages):
            if not _hit_matches_query(raw, query):
                fuzzy_hits += 1
                continue
            beatmapset_id = int(raw["id"])
            discovered[beatmapset_id] = raw
            discovery_evidence.setdefault(beatmapset_id, set()).add(f"discovery_query:{query}")

    prepared = []
    provenance_only = 0
    for beatmapset_id in sorted(discovered):
        current = catalog.entries.get(beatmapset_id)
        evidence = set(discovery_evidence[beatmapset_id])
        if current:
            evidence.update(current.evidence)
        entry = entry_from_osu(discovered[beatmapset_id], evidence=sorted(evidence), confidence="candidate")
        checked_on = entry.last_checked
        if current:
            # Reconciliation owns routine freshness updates. Weekly discovery
            # should not create a diff solely because today's date changed.
            entry.last_checked = current.last_checked
        kind = _discovery_change_kind(current, entry)
        if kind is None:
            continue
        if kind == "provenance":
            provenance_only += 1
            continue
        prepared.append(
            (
                DISCOVERY_CHANGE_PRIORITY[kind],
                DISCOVERY_CONFIDENCE_ORDER[entry.confidence],
                beatmapset_id,
                kind,
                entry,
                checked_on,
            )
        )

    applied = {kind: 0 for kind in DISCOVERY_CHANGE_PRIORITY}
    changed = 0
    processed = 0
    for _, _, _, kind, entry, checked_on in sorted(prepared, key=lambda item: item[:3]):
        if args.max_changes and changed >= args.max_changes:
            break
        processed += 1
        merged, did_change = catalog.merge(entry)
        if did_change:
            merged.last_checked = checked_on
            applied[kind] += 1
        changed += did_change
    deferred = len(prepared) - processed
    demoted = enforce_generic_source_policy(catalog)
    changed += demoted
    breakdown = ", ".join(f"{kind}={count}" for kind, count in applied.items())
    notes = [f"{changed} entries changed ({breakdown})"]
    if demoted:
        notes.append(f"{demoted} generic-source verifications demoted")
    if provenance_only:
        notes.append(f"{provenance_only} query-provenance-only updates skipped")
    if deferred:
        notes.append(f"change limit {args.max_changes} reached, {deferred} deferred")
    print(
        f"Discovery examined {len(discovered)} unique beatmapsets "
        f"({fuzzy_hits} fuzzy search hits without the query text rejected); " + "; ".join(notes)
    )
    if args.write:
        catalog.save(args.catalog)
        print(f"Wrote {args.catalog}")
    print_stats(catalog)
    return 0


DISCOVERY_FIELD_QUERY_RE = re.compile(r"^(artist|title|source|creator|tags?)\s*=\s*(.+)$", re.IGNORECASE)
DISCOVERY_MATCH_FIELDS = ("artist", "artist_unicode", "title", "title_unicode", "source", "tags", "creator")


def _phrase_tokens(value: str) -> list[str]:
    return [token for token in re.split(r"[\W_]+", normalize_text(value)) if token]


def _compact(value: str) -> str:
    return re.sub(r"[\s_]+", "", normalize_text(value))


def _contains_phrase(haystack: str, needle: str) -> bool:
    """Whole-token phrase match for Latin text, substring match for CJK text."""

    if not needle.isascii():
        return bool(_compact(needle)) and _compact(needle) in _compact(haystack)
    tokens = _phrase_tokens(needle)
    words = _phrase_tokens(haystack)
    width = len(tokens)
    return bool(tokens) and any(words[index : index + width] == tokens for index in range(len(words) - width + 1))


def _hit_matches_query(raw: dict, query: str) -> bool:
    """Return whether an osu! search hit literally contains its query.

    osu! search tokenizes queries loosely: ``A-One`` returns "Another One Bites
    the Dust", ``東方Project`` returns ALI PROJECT, ``ZUN`` returns Zuntata. Such
    hits are not discovery evidence, so they are dropped before classification.
    ``field=value`` queries are checked against that field only.
    """

    field_query = DISCOVERY_FIELD_QUERY_RE.match(query.strip())
    if field_query:
        field_name = field_query.group(1).casefold()
        field_name = "tags" if field_name.startswith("tag") else field_name
        value = field_query.group(2).strip().strip('"')
        fields = [field_name, f"{field_name}_unicode"]
        return _contains_phrase(" ".join(str(raw.get(name) or "") for name in fields), value)
    return _contains_phrase(" ".join(str(raw.get(name) or "") for name in DISCOVERY_MATCH_FIELDS), query)


def _discovery_change_kind(current: Entry | None, incoming: Entry) -> str | None:
    """Classify what merging a discovery hit would change, without mutating the catalog.

    Returns ``None`` when nothing would change and ``"provenance"`` when the
    merge would only add ``discovery_query:`` evidence to an already catalogued
    row. That provenance never affects classification, and letting it count
    toward the weekly change cap starved discovery of genuinely new beatmapsets,
    so callers skip both.
    """

    if current is None:
        return "new"
    before = current.to_dict()
    merged, did_change = Catalog([Entry.from_dict(before)]).merge(Entry.from_dict(incoming.to_dict()))
    if not did_change:
        return None
    after = merged.to_dict()
    if after["confidence"] != before["confidence"]:
        return "confidence"
    if any(after[key] != before[key] for key in after if key not in {"evidence", "last_checked"}):
        return "metadata"
    added = set(after["evidence"]) - set(before["evidence"])
    removed = set(before["evidence"]) - set(after["evidence"])
    if removed or any(not item.startswith("discovery_query:") for item in added):
        return "metadata"
    return "provenance"


def _same_reconciled_title(left: str, right: str) -> bool:
    left_normalized = normalize_text(left)
    right_normalized = normalize_text(right)
    return bool(
        left_normalized
        and right_normalized
        and (
            left_normalized == right_normalized
            or left_normalized in right_normalized
            or right_normalized in left_normalized
        )
    )


def _quarantine_replaced_identity(current, raw: dict) -> list[str]:
    incoming_artist = str(raw.get("artist", "")).strip()
    incoming_title = str(raw.get("title", "")).strip()
    if not current.artist or not current.title or not incoming_artist or not incoming_title:
        return []
    artist_matches = normalize_text(current.artist) == normalize_text(incoming_artist)
    if _same_reconciled_title(current.title, incoming_title):
        return []
    if artist_matches and not any(
        item.startswith(RECONCILE_REVIEWED_IDENTITY_PREFIXES) for item in current.evidence
    ):
        return []
    if not any(
        item.startswith(RECONCILE_STRONG_IDENTITY_PREFIXES) for item in current.evidence
    ):
        return []

    stale = [
        item
        for item in current.evidence
        if item in RECONCILE_STALE_IDENTITY_EVIDENCE
        or item.startswith(RECONCILE_STALE_IDENTITY_PREFIXES)
    ]
    if not stale:
        return []

    current.evidence = [item for item in current.evidence if item not in stale]
    current.evidence.append(IDENTITY_MISMATCH_MARKER)
    current.confidence = "candidate"
    current.touhou_kind = "unknown"
    current.origin_games = []
    current.original_themes = []
    # Catalog.merge is intentionally conservative for partial seed records.
    # A confirmed identity replacement is different: old osu! metadata belongs
    # to the stale identity and must not survive when the new API value is blank
    # or has a different mode set.
    current.creator = ""
    current.source = ""
    current.status = "unknown"
    current.modes = []
    current.osu_last_updated = None
    return stale


def _reconcile_order(catalog: Catalog, *, limit: int = 0, min_age_days: int = 0) -> list[int]:
    """Return IDs to refresh, stalest ``last_checked`` first.

    Successful refreshes bump ``last_checked``, so a run that stops early (time
    budget, timeout, ``--limit``) resumes with the rows it skipped next time
    instead of starting over from the lowest beatmapset ID.
    """

    cutoff = (date.today() - timedelta(days=min_age_days)).isoformat() if min_age_days > 0 else None
    order = sorted(
        (
            beatmapset_id
            for beatmapset_id, entry in catalog.entries.items()
            if cutoff is None or not entry.last_checked or entry.last_checked <= cutoff
        ),
        key=lambda beatmapset_id: (catalog.entries[beatmapset_id].last_checked or "", beatmapset_id),
    )
    return order[:limit] if limit > 0 else order


def _reconcile_entry(catalog: Catalog, beatmapset_id: int, raw: dict) -> tuple[bool, tuple | None]:
    current = catalog.entries[beatmapset_id]
    previous_identity = f"{current.artist} - {current.title}"
    stale_evidence = _quarantine_replaced_identity(current, raw)
    quarantine = None
    if stale_evidence:
        incoming_identity = f"{raw.get('artist', '')} - {raw.get('title', '')}"
        quarantine = (beatmapset_id, previous_identity, incoming_identity, stale_evidence)
    incoming = entry_from_osu(raw, evidence=current.evidence, confidence=current.confidence)
    incoming.touhou_kind = current.touhou_kind
    incoming.origin_games = current.origin_games
    incoming.original_themes = current.original_themes
    _, did_change = catalog.merge(incoming)
    return did_change or bool(stale_evidence), quarantine


def command_reconcile(args: argparse.Namespace) -> int:
    catalog = Catalog.load(args.catalog)
    api = OsuApi.from_env()
    api.token()
    order = _reconcile_order(catalog, limit=args.limit, min_age_days=args.min_age_days)
    started = time.monotonic()
    deadline = started + args.time_budget if args.time_budget > 0 else None
    changed = 0
    processed = 0
    failures: list[int] = []
    missing: list[int] = []
    identity_quarantines: list[tuple[int, str, str, list[str]]] = []
    print(f"Reconciling {len(order)} of {len(catalog.entries)} beatmapsets (stalest first)", flush=True)

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        queue = iter(order)
        in_flight: dict[Future, int] = {}

        def submit_next() -> None:
            if deadline is not None and time.monotonic() >= deadline:
                return
            beatmapset_id = next(queue, None)
            if beatmapset_id is not None:
                in_flight[executor.submit(api.beatmapset, beatmapset_id)] = beatmapset_id

        # Keep a bounded window in flight so the time budget can stop new work
        # without abandoning results that have already been fetched.
        for _ in range(max(1, args.workers) * 2):
            submit_next()
        while in_flight:
            done, _ = wait(in_flight, return_when=FIRST_COMPLETED)
            for future in done:
                beatmapset_id = in_flight.pop(future)
                processed += 1
                try:
                    raw = future.result()
                    did_change, quarantine = _reconcile_entry(catalog, beatmapset_id, raw)
                except Exception as exc:
                    # One bad payload must not discard everything fetched so far.
                    failures.append(beatmapset_id)
                    if isinstance(exc, HttpError) and exc.status == 404:
                        missing.append(beatmapset_id)
                    elif not isinstance(exc, HttpError):
                        print(f"warning: beatmapset {beatmapset_id}: {exc}", file=sys.stderr)
                else:
                    changed += did_change
                    if quarantine:
                        identity_quarantines.append(quarantine)
                if processed % RECONCILE_PROGRESS_INTERVAL == 0:
                    elapsed = time.monotonic() - started
                    print(
                        f"progress: {processed}/{len(order)} fetched in {elapsed:.0f}s "
                        f"({processed / max(elapsed, 1e-9):.1f}/s); {len(failures)} failed",
                        flush=True,
                    )
                submit_next()

    demoted = enforce_generic_source_policy(catalog)
    changed += demoted
    for beatmapset_id, previous, incoming, stale in sorted(identity_quarantines):
        print(
            f"warning: beatmapset {beatmapset_id} identity changed "
            f"{previous!r} -> {incoming!r}; quarantined evidence: {', '.join(stale)}",
            file=sys.stderr,
        )
    deferred = len(order) - processed
    summary = (
        f"Reconciled {processed - len(failures)} beatmapsets; {changed} changed; "
        f"{len(failures)} failed ({len(missing)} not found)"
    )
    if deferred:
        summary += f"; time budget reached, {deferred} stalest-first rows deferred to the next run"
    print(summary)
    if failures:
        print("Failed IDs: " + ", ".join(map(str, sorted(failures)[:50])), file=sys.stderr)
    if args.write:
        catalog.save(args.catalog)
        print(f"Wrote {args.catalog}")
    print_stats(catalog)
    return 1 if failures and args.strict else 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    subparsers = result.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="validate canonical catalog")
    validate.set_defaults(func=command_validate)

    build_parser = subparsers.add_parser("build", help="generate site and exports")
    build_parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    build_parser.set_defaults(func=command_build)

    assemble = subparsers.add_parser("assemble", help="combine canonical shards into one JSON file")
    assemble.add_argument("--output", type=Path, default=DEFAULT_OUTPUT / "catalog-full.json")
    assemble.set_defaults(func=command_assemble)

    clean = subparsers.add_parser("clean", help="remove generated output")
    clean.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    clean.set_defaults(func=command_clean)

    audit = subparsers.add_parser("audit-sources", help="query every configured source and report coverage")
    audit.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    audit.add_argument("--workers", type=int, default=4)
    audit.add_argument("--json", action="store_true")
    audit.set_defaults(func=command_audit_sources)

    hydrate = subparsers.add_parser("hydrate", help="fill incomplete source records from public pages")
    hydrate.add_argument("--workers", type=int, default=2)
    hydrate.add_argument("--limit", type=int, default=0, help="maximum records; use 0 for unlimited")
    hydrate.add_argument("--write", action="store_true")
    hydrate.add_argument("--strict", action="store_true")
    hydrate.set_defaults(func=command_hydrate)

    for name, help_text, function in (
        ("import-seeds", "import configured seed sources", command_import_seeds),
        ("discover", "search osu! API for new candidates", command_discover),
    ):
        item = subparsers.add_parser(name, help=help_text)
        item.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
        item.add_argument("--write", action="store_true")
        if name == "import-seeds":
            item.add_argument("--workers", type=int, default=4)
        else:
            item.add_argument("--max-pages", type=int, default=4)
            item.add_argument(
                "--max-changes",
                type=int,
                default=50,
                help="maximum catalog changes per run; use 0 for unlimited",
            )
        item.set_defaults(func=function)

    reconcile = subparsers.add_parser("reconcile", help="refresh catalog entries from osu! API, stalest first")
    reconcile.add_argument("--write", action="store_true")
    reconcile.add_argument("--workers", type=int, default=4)
    reconcile.add_argument("--strict", action="store_true")
    reconcile.add_argument("--limit", type=int, default=0, help="maximum records; use 0 for unlimited")
    reconcile.add_argument(
        "--time-budget",
        type=float,
        default=0,
        help="stop starting new requests after this many seconds and write partial results; 0 disables",
    )
    reconcile.add_argument(
        "--min-age-days",
        type=int,
        default=0,
        help="only refresh rows last checked at least this many days ago; 0 refreshes every row",
    )
    reconcile.set_defaults(func=command_reconcile)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        return args.func(args)
    except (CatalogError, MissingCredentials, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
