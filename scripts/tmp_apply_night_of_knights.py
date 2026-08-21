#!/usr/bin/env python3
"""Temporary one-shot PR #27 writeback, removed after final verification."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from touhou_osu.catalog import Catalog
from touhou_osu.classifier import apply_classification
from touhou_osu.http import HttpError
from touhou_osu.osu_api import OsuApi, entry_from_osu

ORIGIN_GAMES = [
    "東方紅魔郷 ～ the Embodiment of Scarlet Devil.",
    "東方花映塚 ～ Phantasmagoria of Flower View.",
]
ORIGINAL_THEMES = ["フラワリングナイト", "月時計 ～ ルナ・ダイアル"]
MIXED_IDS = {1528497, 337187, 1598539, 1675793, 1976379, 2274999, 2534273}

base_raw = json.loads(subprocess.check_output(["git", "show", "origin/main:data/catalog.json"], text=True))
base = {int(item["beatmapset_id"]): item for item in base_raw["entries"]}
catalog_path = Path("data/catalog.json")
catalog = Catalog.load(catalog_path)
new_ids = sorted(set(catalog.entries) - set(base))
assert len(base) == 3632, len(base)
assert len(new_ids) == 357, len(new_ids)

for beatmapset_id in new_ids:
    entry = catalog.entries[beatmapset_id]
    assert entry.confidence == "verified", (beatmapset_id, entry.confidence)
    assert "audit:night-of-knights-2026-08" in entry.evidence, (beatmapset_id, entry.evidence)
    entry.origin_games = list(ORIGIN_GAMES)
    entry.original_themes = list(ORIGINAL_THEMES)
    entry.touhou_kind = "mixed" if beatmapset_id in MIXED_IDS else "arrangement"

target = catalog.entries[154426]
unresolved = catalog.entries[1561908]
assert "manual:candidate" not in target.evidence
assert "manual:excluded" not in target.evidence
assert unresolved.confidence == "candidate"
assert "manual:verified" not in unresolved.evidence

api = OsuApi.from_env()
api.token()
raw = api.beatmapset(154426)
assert int(raw["id"]) == 154426
assert raw.get("artist") == "beatMARIO", raw.get("artist")
assert raw.get("title") == "Night of Knights", raw.get("title")
tags = (raw.get("tags") or "").casefold()
assert "touhou" in tags and ("cool&create" in tags or "cool create" in tags), tags

try:
    api.beatmapset(1561908)
except HttpError as exc:
    assert "HTTP 404" in str(exc), str(exc)
else:
    raise AssertionError("1561908 unexpectedly resolves; requires fresh manual review")

if target.confidence == "candidate":
    incoming = entry_from_osu(
        raw,
        evidence=[
            "audit:night-of-knights-2026-08",
            "manual:verified",
            "composition:cool-create:night-of-knights",
            "corroboration:cool-create:base-track",
        ],
        confidence="candidate",
    )
    incoming.touhou_kind = "arrangement"
    incoming.origin_games = list(ORIGIN_GAMES)
    incoming.original_themes = list(ORIGINAL_THEMES)
    incoming = apply_classification(incoming, tags=raw.get("tags", ""))
    assert incoming.confidence == "verified"
    _, changed = catalog.merge(incoming)
    assert changed
else:
    assert target.confidence == "verified"
    target.touhou_kind = "arrangement"
    target.origin_games = list(ORIGIN_GAMES)
    target.original_themes = list(ORIGINAL_THEMES)
    for evidence in [
        "audit:night-of-knights-2026-08",
        "manual:verified",
        "composition:cool-create:night-of-knights",
        "corroboration:cool-create:base-track",
    ]:
        if evidence not in target.evidence:
            target.evidence.append(evidence)

catalog.save(catalog_path)

doc_path = Path("docs/source-audit-2026-08-night-of-knights.md")
doc = doc_path.read_text(encoding="utf-8")
start = "<!-- NIGHT_EXISTING_CANDIDATE_START -->"
end = "<!-- NIGHT_EXISTING_CANDIDATE_END -->"
block = f"""{start}

## Existing candidate boundary

A separate scan of the pre-change catalog found two historical `candidate` entries with controlled Night-of-Knights titles that were not both represented in the 440 absent-set pool:

- `154426` — `beatMARIO - Night of Knights`. The set still resolves through the official osu! API; current artist/title remain exact, and current mapper tags include both `cool&create` and `touhou`. Combined with COOL&CREATE's first-party provenance for the parent track, this entry is upgraded to `verified` with sticky `manual:verified` evidence.
- `1561908` — historical metadata `USAO - Night of Nights (USAO Remix)`. COOL&CREATE's 2019 first-party album independently confirms that exact derivative exists, but the current osu! API returns HTTP 404 for the beatmapset. Under the conservative unresolved-link boundary, this catalog entry remains `candidate` and receives no manual override.

The separate non-family first-party recall pass searched `ナイト・オブ・ニーツ` / `Night of NEETs`, `ナイト・オブ・IQの低いナイツ` / `Night of Low IQ Nights`, and `NIGHT OF FLOWER -幻想郷最速伝説-` / `NIGHT OF FLOWER` across `graveyard`, `ranked`, `loved`, `qualified`, `pending`, and `wip`: **36 query/status pairs, zero guarded title+artist direct matches, and zero API query errors**. Therefore no extra beatmapsets are added from that recall pass.

{end}"""
if start in doc:
    doc = doc[: doc.index(start)] + block + doc[doc.index(end) + len(end) :]
else:
    doc = doc.rstrip() + "\n\n" + block + "\n"

start = "<!-- NIGHT_STRUCTURED_PROVENANCE_START -->"
end = "<!-- NIGHT_STRUCTURED_PROVENANCE_END -->"
mixed = ",".join(map(str, sorted(MIXED_IDS)))
block = f"""{start}

## Structured provenance normalization

COOL&CREATE's first-party provenance identifies the parent `ナイト・オブ・ナイツ` as an arrangement of both `フラワリングナイト` (東方花映塚) and `月時計 ～ ルナ・ダイアル` (東方紅魔郷). The final catalog pass therefore records both canonical games and both original themes on all **357 newly added derivative sets** and on the reviewed existing set `154426`.

The title/metadata review identifies **7 mixed-source derivatives** rather than pure arrangements: `{mixed}`. These include the previously identified `The kid vs DjSray` mashup plus live-metadata-confirmed McDonald's/Happy Set, Gachi, Otomad collaboration, Super Mario 64, Lucky Star, and S3RL/Bass Slut variants. Those seven use `touhou_kind: mixed`; the remaining 350 new sets and `154426` use `touhou_kind: arrangement`.

No confidence decision is changed by this normalization; it only fills structured provenance already supported by the same first-party composition chain.

{end}"""
if start in doc:
    doc = doc[: doc.index(start)] + block + doc[doc.index(end) + len(end) :]
else:
    doc = doc.rstrip() + "\n\n" + block + "\n"
doc_path.write_text(doc, encoding="utf-8")

print("PR27_FINAL_WRITEBACK_OK")
print("new_verified=357")
print("mixed=", sorted(MIXED_IDS))
print("arrangement=350")
print("upgraded=154426")
print("unresolved_candidate=1561908")
