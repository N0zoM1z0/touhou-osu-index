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
from touhou_osu.http import HttpError
from touhou_osu.models import Entry
from touhou_osu.osu_api import OsuApi

ORIGIN_GAMES = [
    "東方紅魔郷 ～ the Embodiment of Scarlet Devil.",
    "東方花映塚 ～ Phantasmagoria of Flower View.",
]
ORIGINAL_THEMES = ["フラワリングナイト", "月時計 ～ ルナ・ダイアル"]
MIXED_IDS = {1528497, 337187, 1598539, 1675793, 1976379, 2274999, 2534273}
SUBSTANTIVE_FIELDS = ("artist", "title", "creator", "source", "status", "modes", "osu_last_updated")

base_raw = json.loads(subprocess.check_output(["git", "show", "origin/main:data/catalog.json"], text=True))
base = {int(item["beatmapset_id"]): item for item in base_raw["entries"]}
catalog_path = Path("data/catalog.json")
catalog = Catalog.load(catalog_path)
new_ids = sorted(set(catalog.entries) - set(base))
assert len(base) == 3632, len(base)
assert len(new_ids) == 357, len(new_ids)
assert set(base) <= set(catalog.entries)

# Normalize structured provenance only on the 357 already-reviewed new entries.
for beatmapset_id in new_ids:
    entry = catalog.entries[beatmapset_id]
    assert entry.confidence == "verified", (beatmapset_id, entry.confidence)
    assert "audit:night-of-knights-2026-08" in entry.evidence, (beatmapset_id, entry.evidence)
    entry.origin_games = list(ORIGIN_GAMES)
    entry.original_themes = list(ORIGINAL_THEMES)
    entry.touhou_kind = "mixed" if beatmapset_id in MIXED_IDS else "arrangement"

# Two pre-existing title-family candidates need separate handling. Always rebuild both
# from main first so this one-shot writeback is idempotent and cannot preserve an
# accidental intermediate mutation from an earlier CI attempt.
base_target = base[154426]
base_unresolved = base[1561908]
assert base_target["confidence"] == "candidate"
assert "manual:candidate" not in base_target["evidence"] and "manual:excluded" not in base_target["evidence"]
assert base_unresolved["confidence"] == "candidate"
assert not any(x in base_unresolved["evidence"] for x in ("manual:verified", "manual:excluded"))

api = OsuApi.from_env()
api.token()
raw = api.beatmapset(154426)
assert int(raw["id"]) == 154426
assert raw.get("artist") == base_target["artist"] == "beatMARIO"
assert raw.get("title") == base_target["title"] == "Night of Knights"
tags = (raw.get("tags") or "").casefold()
assert "touhou" in tags and ("cool&create" in tags or "cool create" in tags), tags

# This historical USAO candidate is intentionally NOT upgraded while the live set is unresolved.
try:
    api.beatmapset(1561908)
except HttpError as exc:
    assert "HTTP 404" in str(exc), str(exc)
else:
    raise AssertionError("1561908 unexpectedly resolves; requires fresh manual review")

# Minimal deterministic mutation for 154426: start from main, preserve all live/catalog
# metadata and dates, then add only the reviewed confidence/provenance fields.
target = Entry.from_dict(base_target)
target.confidence = "verified"
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
target.normalize()
target.validate()
for field in SUBSTANTIVE_FIELDS:
    assert target.to_dict()[field] == base_target[field], (154426, field, target.to_dict()[field], base_target[field])
assert target.last_checked == base_target.get("last_checked")

catalog.entries[154426] = target
catalog.entries[1561908] = Entry.from_dict(base_unresolved)
assert catalog.entries[1561908].to_dict() == base_unresolved
catalog.save(catalog_path)

doc_path = Path("docs/source-audit-2026-08-night-of-knights.md")
doc = doc_path.read_text(encoding="utf-8")
start = "<!-- NIGHT_EXISTING_CANDIDATE_START -->"
end = "<!-- NIGHT_EXISTING_CANDIDATE_END -->"
block = f"""{start}

## Existing candidate boundary

A separate scan of the pre-change catalog found two historical `candidate` entries with controlled Night-of-Knights titles:

- `154426` — `beatMARIO - Night of Knights`. The set still resolves through the official osu! API; current artist/title remain exact, and current mapper tags include both `cool&create` and `touhou`. It has no sticky `manual:candidate` / `manual:excluded` boundary. Combined with COOL&CREATE's first-party provenance for the parent track, this entry is upgraded to `verified` with sticky `manual:verified` evidence. The upgrade intentionally preserves its pre-existing artist/title/creator/source/status/modes/osu-last-updated and last-checked metadata from `main`.
- `1561908` — historical metadata `USAO - Night of Nights (USAO Remix)`. COOL&CREATE's 2019 first-party album independently confirms that exact derivative exists, but the current osu! API returns HTTP 404 for the beatmapset. Under the conservative unresolved-link boundary, this catalog entry remains byte-for-byte field-equivalent to `main` as `candidate` and receives no manual override.

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

The title/metadata review identifies **7 mixed-source derivatives** rather than pure arrangements: `{mixed}`. Those seven use `touhou_kind: mixed`; the remaining **350 new sets** and `154426` use `touhou_kind: arrangement`.

No confidence decision is changed by this normalization except the separately reviewed `154426` candidate upgrade described above. The unresolved `1561908` entry remains unchanged.

{end}"""
if start in doc:
    doc = doc[: doc.index(start)] + block + doc[doc.index(end) + len(end) :]
else:
    doc = doc.rstrip() + "\n\n" + block + "\n"
doc_path.write_text(doc, encoding="utf-8")

print("PR27_FINAL_WRITEBACK_OK")
print("new_verified=357")
print("mixed=", sorted(MIXED_IDS))
print("arrangement_new=350")
print("upgraded=154426")
print("unresolved_candidate_404=1561908")
