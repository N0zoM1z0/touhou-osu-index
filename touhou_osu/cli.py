"""Command-line interface for the Touhou osu! index."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from .catalog import Catalog
from .http import get_text
from .models import CatalogError
from .osu_api import MissingCredentials, OsuApi, entry_from_osu
from .site import build, statistics
from .sources import import_all, parse_beatmapset_page

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = ROOT / "data" / "catalog.json"
DEFAULT_CONFIG = ROOT / "config" / "seeds.json"
DEFAULT_OUTPUT = ROOT / "dist"
DISCOVERY_CONFIDENCE_ORDER = {"verified": 0, "probable": 1, "candidate": 2, "excluded": 3}


def load_catalog(path: Path) -> Catalog:
    return Catalog.load(path) if path.exists() else Catalog()


def load_config(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def print_stats(catalog: Catalog) -> None:
    stats = statistics(catalog)
    details = ", ".join(f"{key}={value}" for key, value in stats["confidence"].items())
    print(f"Catalog: {stats['total']} beatmapsets ({details}); accepted={stats['accepted']}")


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
        _, did_change = catalog.merge(entry)
        changed += did_change
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
    prefixes = ("forum_queue:", "tournament_candidate:")
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
    for query in config.get("discovery_queries", []):
        for raw in api.search(query, max_pages=args.max_pages):
            beatmapset_id = int(raw["id"])
            discovered[beatmapset_id] = raw
            discovery_evidence.setdefault(beatmapset_id, set()).add(f"discovery_query:{query}")

    prepared = []
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
        prepared.append((DISCOVERY_CONFIDENCE_ORDER[entry.confidence], beatmapset_id, entry, checked_on))

    changed = 0
    processed = 0
    for _, _, entry, checked_on in sorted(prepared):
        if args.max_changes and changed >= args.max_changes:
            break
        merged, did_change = catalog.merge(entry)
        processed += 1
        if did_change:
            merged.last_checked = checked_on
        changed += did_change
    limit_note = ""
    if args.max_changes and changed >= args.max_changes and processed < len(prepared):
        limit_note = f"; change limit {args.max_changes} reached, remainder deferred"
    print(f"Discovery examined {len(discovered)} unique beatmapsets; {changed} entries changed{limit_note}")
    if args.write:
        catalog.save(args.catalog)
        print(f"Wrote {args.catalog}")
    print_stats(catalog)
    return 0


def command_reconcile(args: argparse.Namespace) -> int:
    catalog = Catalog.load(args.catalog)
    api = OsuApi.from_env()
    api.token()
    changed = 0
    failures: list[int] = []

    def fetch(beatmapset_id: int):
        return beatmapset_id, api.beatmapset(beatmapset_id)

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(fetch, item): item for item in catalog.entries}
        for future in as_completed(futures):
            beatmapset_id = futures[future]
            try:
                _, raw = future.result()
            except Exception:
                failures.append(beatmapset_id)
                continue
            current = catalog.entries[beatmapset_id]
            incoming = entry_from_osu(raw, evidence=current.evidence, confidence=current.confidence)
            incoming.touhou_kind = current.touhou_kind
            incoming.origin_games = current.origin_games
            incoming.original_themes = current.original_themes
            _, did_change = catalog.merge(incoming)
            changed += did_change

    print(f"Reconciled {len(catalog.entries) - len(failures)} beatmapsets; {changed} changed; {len(failures)} failed")
    if failures:
        print("Failed IDs: " + ", ".join(map(str, sorted(failures)[:50])), file=sys.stderr)
    if args.write:
        catalog.save(args.catalog)
        print(f"Wrote {args.catalog}")
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

    reconcile = subparsers.add_parser("reconcile", help="refresh every catalog entry from osu! API")
    reconcile.add_argument("--write", action="store_true")
    reconcile.add_argument("--workers", type=int, default=4)
    reconcile.add_argument("--strict", action="store_true")
    reconcile.set_defaults(func=command_reconcile)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        return args.func(args)
    except (CatalogError, MissingCredentials, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
