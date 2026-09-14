#!/usr/bin/env python3
"""Temporary one-shot harness for the September status-depth completeness pass.

This file is intentionally removed after the generated catalog/audit changes pass
Deep Review.  It only accepts beatmapsets that are absent from the current
catalog, still expose a concrete recognized Touhou game source on a direct osu!
API refetch, and do not produce a THBWiki/TouhouDB contradiction/ambiguity.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict, deque
from pathlib import Path

from touhou_osu.catalog import Catalog
from touhou_osu.classifier import is_touhou_game_source, normalized_source
from touhou_osu.models import Entry
from touhou_osu.osu_api import OsuApi, entry_from_osu
from touhou_osu.provenance import audit_entries

CATALOG_PATH = Path("data/catalog")
SEEDS_PATH = Path("config/seeds.json")
AUDIT_PATH = Path("docs/source-audit-2026-09-status-depth-wave2.md")
RUN_DATE = "2026-09-14"
STATUSES = ("graveyard", "wip", "pending")
MAX_SEARCH_PAGES = 4
DIRECT_REFETCH_TARGET = 380
FINAL_TARGET = 250
# Open PR #42 currently touches only these two shard ranges.  Avoid them
# entirely so this addition-only PR has no changed-file collision with #42.
COLLISION_LOW = 500_000
COLLISION_HIGH = 699_999


def md(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def source_queries() -> list[str]:
    payload = json.loads(SEEDS_PATH.read_text(encoding="utf-8"))
    queries: list[str] = []
    for query in payload["discovery_queries"]:
        if not query.startswith("source="):
            continue
        source = query.split("=", 1)[1]
        if is_touhou_game_source(source):
            queries.append(query)
    if not queries:
        raise RuntimeError("no concrete Touhou game-source queries found")
    return queries


def search_backlog(api: OsuApi, base: Catalog, queries: list[str]):
    hits: dict[int, dict] = {}
    pages = 0
    buckets = 0
    for status in STATUSES:
        for query in queries:
            buckets += 1
            cursor: str | None = None
            for _ in range(MAX_SEARCH_PAGES):
                params = {"q": query, "s": status}
                if cursor:
                    params["cursor_string"] = cursor
                payload = api.get("/beatmapsets/search", params)
                pages += 1
                for raw in payload.get("beatmapsets", []):
                    beatmapset_id = int(raw["id"])
                    if beatmapset_id in base.entries:
                        continue
                    if COLLISION_LOW <= beatmapset_id <= COLLISION_HIGH:
                        continue
                    entry = entry_from_osu(
                        raw,
                        evidence=[f"discovery_query:{query}"],
                    )
                    if entry.confidence != "verified" or not is_touhou_game_source(entry.source):
                        continue
                    record = hits.setdefault(
                        beatmapset_id,
                        {
                            "entry": entry,
                            "queries": set(),
                            "search_statuses": set(),
                        },
                    )
                    record["queries"].add(query)
                    record["search_statuses"].add(status)
                cursor = payload.get("cursor_string")
                if not cursor:
                    break
    return hits, pages, buckets


def balanced_ids(hits: dict[int, dict], limit: int) -> list[int]:
    groups: dict[tuple[str, str], list[int]] = defaultdict(list)
    for beatmapset_id, record in hits.items():
        entry: Entry = record["entry"]
        key = (entry.status, normalized_source(entry.source))
        groups[key].append(beatmapset_id)

    queues: dict[tuple[str, str], deque[int]] = {}
    for key, ids in groups.items():
        ids.sort(key=lambda item: (-len(hits[item]["queries"]), item))
        queues[key] = deque(ids)

    # Stable order, with larger groups first, then status/source.  The loop takes
    # only one row from each group per cycle, avoiding a single game/source from
    # dominating the batch.
    keys = sorted(queues, key=lambda key: (-len(queues[key]), key[0], key[1]))
    chosen: list[int] = []
    while len(chosen) < limit:
        progressed = False
        for key in keys:
            queue = queues[key]
            if not queue:
                continue
            chosen.append(queue.popleft())
            progressed = True
            if len(chosen) >= limit:
                break
        if not progressed:
            break
    return chosen


def direct_refetch(
    api: OsuApi,
    base: Catalog,
    hits: dict[int, dict],
    shortlist: list[int],
) -> tuple[list[Entry], list[dict]]:
    accepted: list[Entry] = []
    rejected: list[dict] = []
    for beatmapset_id in shortlist:
        try:
            raw = api.beatmapset(beatmapset_id)
            evidence = [
                f"discovery_query:{query}"
                for query in sorted(hits[beatmapset_id]["queries"], key=str.casefold)
            ]
            entry = entry_from_osu(raw, evidence=evidence)
            reasons: list[str] = []
            if entry.beatmapset_id != beatmapset_id:
                reasons.append("id drift")
            if beatmapset_id in base.entries:
                reasons.append("became present in base")
            if entry.confidence != "verified":
                reasons.append(f"confidence={entry.confidence}")
            if not is_touhou_game_source(entry.source):
                reasons.append("source is not a concrete recognized Touhou game")
            if entry.status not in STATUSES:
                reasons.append(f"status drifted to {entry.status}")
            if reasons:
                rejected.append({"beatmapset_id": beatmapset_id, "reason": "; ".join(reasons)})
                continue
            accepted.append(entry)
            if len(accepted) >= DIRECT_REFETCH_TARGET:
                break
        except Exception as exc:  # fail closed on any live lookup problem
            rejected.append({"beatmapset_id": beatmapset_id, "reason": str(exc)})
    return accepted, rejected


def select_final(entries: list[Entry], hits: dict[int, dict]):
    audits = audit_entries(entries, workers=4)
    by_id = {audit.beatmapset_id: audit for audit in audits}
    rejected = [
        audit
        for audit in audits
        if audit.verdict in {"red_flag", "ambiguous"}
    ]
    eligible = [
        entry
        for entry in entries
        if by_id[entry.beatmapset_id].verdict not in {"red_flag", "ambiguous"}
    ]

    # Prefer independently supported rows, then clean unknowns. Provider errors
    # are a last-resort ordering penalty, not evidence of correctness.
    def score(entry: Entry):
        audit = by_id[entry.beatmapset_id]
        return (
            0 if audit.verdict == "supported" else 1,
            1 if audit.errors else 0,
            -len(hits[entry.beatmapset_id]["queries"]),
            entry.beatmapset_id,
        )

    groups: dict[tuple[str, str], list[Entry]] = defaultdict(list)
    for entry in eligible:
        groups[(entry.status, normalized_source(entry.source))].append(entry)
    queues: dict[tuple[str, str], deque[Entry]] = {}
    for key, values in groups.items():
        values.sort(key=score)
        queues[key] = deque(values)
    keys = sorted(
        queues,
        key=lambda key: (score(queues[key][0]), -len(queues[key]), key[0], key[1]),
    )

    selected: list[Entry] = []
    while len(selected) < FINAL_TARGET:
        progressed = False
        for key in keys:
            queue = queues[key]
            if not queue:
                continue
            selected.append(queue.popleft())
            progressed = True
            if len(selected) >= FINAL_TARGET:
                break
        if not progressed:
            break
    if len(selected) != FINAL_TARGET:
        raise RuntimeError(
            f"only {len(selected)} contradiction-free direct-refetched rows remain; "
            f"need {FINAL_TARGET}"
        )
    return selected, audits, rejected


def write_audit(
    *,
    base_count: int,
    queries: list[str],
    pages: int,
    buckets: int,
    hit_count: int,
    shortlist_count: int,
    direct_entries: list[Entry],
    direct_rejected: list[dict],
    selected: list[Entry],
    audits,
    provenance_rejected,
    hits: dict[int, dict],
) -> None:
    audit_by_id = {audit.beatmapset_id: audit for audit in audits}
    status_counts = Counter(entry.status for entry in selected)
    mode_counts = Counter(mode for entry in selected for mode in entry.modes)
    verdict_counts = Counter(audit_by_id[entry.beatmapset_id].verdict for entry in selected)
    selected_provider_errors = sum(bool(audit_by_id[entry.beatmapset_id].errors) for entry in selected)

    lines = [
        "# Status-scoped Touhou discovery audit — wave 2 (2026-09-14)",
        "",
        "## Decision",
        "",
        f"Add **{len(selected)}** beatmapsets absent from the current `main` catalog. "
        "This is an addition-only continuation of the 2026-09-07 status-depth pass: every accepted row "
        "still exposes a concrete recognized Touhou game source on a fresh direct osu! API refetch, and "
        "rows with THBWiki/TouhouDB contradictions or ambiguity are withheld.",
        "",
        "Open weekly PR #42 touches only `0500000-0599999` and `0600000-0699999`; this pass deliberately "
        "excludes beatmapset IDs 500000–699999 so the final changed-file set cannot collide with that PR.",
        "",
        "## Search breadth",
        "",
        f"- base catalog: **{base_count}** beatmapsets",
        f"- concrete configured game-source queries: **{len(queries)}**",
        f"- status buckets: **{len(STATUSES)}** (`graveyard`, `wip`, `pending`)",
        f"- query/status buckets attempted: **{buckets}**",
        f"- official osu! search pages fetched: **{pages}**",
        f"- unique absent verified search hits outside the #42 collision range: **{hit_count}**",
        f"- diversified direct-refetch shortlist: **{shortlist_count}**",
        f"- accepted after direct `/api/v2/beatmapsets/<id>` refetch: **{len(direct_entries)}**",
        f"- direct-refetch failures/drift withheld: **{len(direct_rejected)}**",
        f"- THBWiki/TouhouDB rows audited before selection: **{len(audits)}**",
        f"- red/ambiguous provenance rows withheld: **{len(provenance_rejected)}**",
        f"- final accepted rows: **{len(selected)}**",
        f"- final provenance verdicts: **{json.dumps(dict(sorted(verdict_counts.items())), ensure_ascii=False)}**",
        f"- final rows with advisory provider transport/errors: **{selected_provider_errors}**",
        f"- status distribution: **{json.dumps(dict(sorted(status_counts.items())), ensure_ascii=False)}**",
        f"- mode coverage: **{json.dumps(dict(sorted(mode_counts.items())), ensure_ascii=False)}**",
        "",
        "Search membership alone is never acceptance evidence. The search object first has to cross the "
        "repository's deterministic `verified` boundary through a concrete recognized Touhou game source; "
        "then the ID is fetched again directly from the official beatmapset endpoint. External composition "
        "provenance is checked before the final boundary is frozen. The repository Deep Review subsequently "
        "repeats external provenance and performs an additional exact identity comparison between the stored "
        "row, a fresh osu! API object, and the public beatmapset page.",
        "",
        "## Accepted beatmapsets",
        "",
        "| Beatmapset ID | Artist | Title | Source | Status | Modes | Query hits | Provenance verdict |",
        "| ---: | --- | --- | --- | --- | --- | ---: | --- |",
    ]
    for entry in sorted(selected, key=lambda item: item.beatmapset_id):
        audit = audit_by_id[entry.beatmapset_id]
        lines.append(
            f"| {entry.beatmapset_id} | {md(entry.artist)} | {md(entry.title)} | {md(entry.source)} | "
            f"{md(entry.status)} | {md(','.join(entry.modes))} | {len(hits[entry.beatmapset_id]['queries'])} | "
            f"{md(audit.verdict)} |"
        )

    lines += [
        "",
        "## Negative boundary",
        "",
        "The following classes are intentionally outside this batch:",
        "",
        "- any beatmapset already present in the base catalog;",
        "- IDs 500000–699999 while weekly PR #42 is open, solely to avoid shard conflicts;",
        "- generic `Touhou` / `東方Project` source rows that do not name a concrete recognized game;",
        "- search hits that fail a fresh direct beatmapset refetch, change status, or no longer classify as verified;",
        "- any external-provenance `red_flag` or `ambiguous` result.",
    ]
    if provenance_rejected:
        lines += ["", "Explicit provenance rejects from this run:", ""]
        for audit in sorted(provenance_rejected, key=lambda item: item.beatmapset_id)[:40]:
            lines.append(
                f"- `{audit.beatmapset_id}` — {md(audit.artist)} — **{audit.verdict}**"
            )
    if direct_rejected:
        lines += ["", "Representative direct-refetch rejects/drift (first 40):", ""]
        for item in direct_rejected[:40]:
            lines.append(f"- `{item['beatmapset_id']}` — {md(item['reason'])}")

    lines += [
        "",
        "## Verification contract",
        "",
        "The final branch is required to pass:",
        "",
        "- `make check`;",
        "- `make build`;",
        "- `git diff --check`;",
        "- Deep Review in `mode=all`, `scope=added`, with exactly 250 additions and `--forbid-existing-changes`;",
        "- Deep Review live osu! identity: catalog row = fresh API object = public beatmapset-page object for every added ID.",
        "",
    ]
    AUDIT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    base = Catalog.load(CATALOG_PATH)
    queries = source_queries()
    api = OsuApi.from_env()
    api.token()

    hits, pages, buckets = search_backlog(api, base, queries)
    if len(hits) < FINAL_TARGET:
        raise RuntimeError(f"only {len(hits)} absent verified hits discovered")

    shortlist = balanced_ids(hits, max(DIRECT_REFETCH_TARGET + 120, FINAL_TARGET + 150))
    direct_entries, direct_rejected = direct_refetch(api, base, hits, shortlist)
    if len(direct_entries) < FINAL_TARGET:
        raise RuntimeError(
            f"only {len(direct_entries)} rows survived direct refetch; need {FINAL_TARGET}"
        )

    selected, audits, provenance_rejected = select_final(direct_entries, hits)
    selected_ids = {entry.beatmapset_id for entry in selected}
    if len(selected_ids) != FINAL_TARGET:
        raise RuntimeError("final selection contains duplicate IDs")
    if selected_ids & set(base.entries):
        raise RuntimeError("final selection overlaps the base catalog")

    current = Catalog.load(CATALOG_PATH)
    for entry in selected:
        merged, changed = current.merge(entry)
        if not changed or merged.beatmapset_id != entry.beatmapset_id:
            raise RuntimeError(f"failed to add beatmapset {entry.beatmapset_id}")
    if len(current.entries) != len(base.entries) + FINAL_TARGET:
        raise RuntimeError("catalog cardinality is not addition-only +250")
    current.save_shards(CATALOG_PATH)

    write_audit(
        base_count=len(base.entries),
        queries=queries,
        pages=pages,
        buckets=buckets,
        hit_count=len(hits),
        shortlist_count=len(shortlist),
        direct_entries=direct_entries,
        direct_rejected=direct_rejected,
        selected=selected,
        audits=audits,
        provenance_rejected=provenance_rejected,
        hits=hits,
    )

    summary = {
        "base": len(base.entries),
        "current": len(current.entries),
        "added": FINAL_TARGET,
        "queries": len(queries),
        "pages": pages,
        "absent_verified_hits": len(hits),
        "direct_refetched": len(direct_entries),
        "provenance_checked": len(audits),
        "provenance_rejected": len(provenance_rejected),
        "selected_supported": sum(
            1
            for audit in audits
            if audit.beatmapset_id in selected_ids and audit.verdict == "supported"
        ),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
