from __future__ import annotations

import json
import re
import sys
import unicodedata
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from touhou_osu.catalog import Catalog
from touhou_osu.classifier import apply_classification
from touhou_osu.osu_api import OsuApi, entry_from_osu

STATUS_LOG = Path(sys.argv[1])


def norm(value: str) -> str:
    return "".join(
        ch
        for ch in unicodedata.normalize("NFKC", value or "").casefold()
        if ch.isalnum()
    )


def load_status_report(path: Path) -> dict:
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    begins = [i for i, line in enumerate(lines) if "NIGHT_STATUS_ENUM_BEGIN" in line]
    ends = [i for i, line in enumerate(lines) if "NIGHT_STATUS_ENUM_END" in line]
    assert begins and ends
    begin = begins[-1]
    end = next(i for i in ends if i > begin)
    payload = []
    for line in lines[begin + 1 : end]:
        payload.append(
            re.sub(
                r"^.*?\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z\s*",
                "",
                line,
            )
        )
    text = "\n".join(payload).strip()
    return json.loads(text[text.find("{") : text.rfind("}") + 1])


GROUPS: dict[str, list[int]] = {
    "direct_parent_metadata": [108242, 154684, 938028, 1528497, 2051058, 2374830, 2498021],
    "official_game_parent": [143771, 200969, 2374763],
    "koraido_artist_store": [2056127],
}
ID_TO_GROUP = {
    beatmapset_id: group
    for group, beatmapset_ids in GROUPS.items()
    for beatmapset_id in beatmapset_ids
}
assert len(ID_TO_GROUP) == 11

EXPECTED_TITLE_TOKENS: dict[int, tuple[str, ...]] = {
    108242: ("nightofknights", "pianoremix"),
    154684: ("nightofnights",),
    938028: ("nightofnights", "samstringremix"),
    1528497: ("nightofnights",),
    2051058: ("knightofknights",),
    2374830: ("nightofknights", "frenchcoreremix"),
    2498021: ("nightofknights", "skipped"),
    143771: ("nightofknights",),
    200969: ("nightofknights",),
    2374763: ("nightofknights",),
    2056127: ("nightofknights", "koraidoremix"),
}


def validate_fresh(beatmapset_id: int, group: str, raw: dict) -> None:
    artist = raw.get("artist", "")
    title = raw.get("title", "")
    source = raw.get("source", "")
    tags = raw.get("tags", "")
    title_n = norm(title)
    combined_n = norm(" ".join([artist, title, source, tags]))
    assert all(token in title_n for token in EXPECTED_TITLE_TOKENS[beatmapset_id]), (
        beatmapset_id,
        "title-drift",
        artist,
        title,
        source,
    )

    if group == "direct_parent_metadata":
        if beatmapset_id == 2051058:
            assert "touhouproject" in norm(source) and "beatmario" in norm(source), (
                beatmapset_id,
                source,
            )
        else:
            assert "beatmario" in combined_n or "coolcreate" in combined_n, (
                beatmapset_id,
                artist,
                title,
                source,
                tags,
            )
        if beatmapset_id == 154684:
            assert norm(artist) == "beatmario" and "동방" in source, (beatmapset_id, artist, source)
        if beatmapset_id == 2374830:
            assert "touhou" in norm(tags), (beatmapset_id, tags)
        if beatmapset_id == 2498021:
            assert "coolcreate" in norm(tags) and "touhou" in norm(tags), (beatmapset_id, tags)
    elif group == "official_game_parent":
        if beatmapset_id == 143771:
            assert "taikonotatsujin" in norm(artist) and "太鼓" in source, (beatmapset_id, artist, source)
        elif beatmapset_id == 200969:
            assert "soundvoltexii" in norm(source), (beatmapset_id, source)
        elif beatmapset_id == 2374763:
            assert "peposoft" in norm(artist) and "touhoulunanights" in norm(source), (
                beatmapset_id,
                artist,
                source,
            )
    elif group == "koraido_artist_store":
        assert "koraido" in norm(artist) and "koraidoremix" in title_n, (
            beatmapset_id,
            artist,
            title,
        )
    else:
        raise AssertionError((beatmapset_id, group))


report = load_status_report(STATUS_LOG)
original_missing = {int(row["beatmapset_id"]) for row in report["missing"]}
assert set(ID_TO_GROUP) <= original_missing

catalog_path = Path("data/catalog.json")
catalog = Catalog.load(catalog_path)
pending = [beatmapset_id for beatmapset_id in sorted(ID_TO_GROUP) if beatmapset_id not in catalog.entries]
assert len(pending) in {0, 11}, (len(pending), pending)
if not pending:
    print("NIGHT_MANUAL_WAVE3_ALREADY_COMPLETE")
    raise SystemExit(0)

api = OsuApi.from_env()
api.token()


def fetch(beatmapset_id: int) -> tuple[int, str, dict]:
    raw = api.beatmapset(beatmapset_id)
    assert int(raw["id"]) == beatmapset_id
    group = ID_TO_GROUP[beatmapset_id]
    validate_fresh(beatmapset_id, group, raw)
    return beatmapset_id, group, raw


with ThreadPoolExecutor(max_workers=8) as pool:
    fetched = list(pool.map(fetch, pending))

EVIDENCE_BY_GROUP = {
    "direct_parent_metadata": "corroboration:osu-metadata-direct-parent-attribution",
    "official_game_parent": "corroboration:official-game-night-of-knights-credit",
    "koraido_artist_store": "corroboration:koraido-booth-night-of-knights-remix",
}
counts = {group: 0 for group in GROUPS}
ids_by = {group: [] for group in GROUPS}
for beatmapset_id, group, raw in fetched:
    incoming = entry_from_osu(
        raw,
        evidence=[
            "audit:night-of-knights-2026-08",
            "manual:verified",
            "composition:cool-create:night-of-knights",
            EVIDENCE_BY_GROUP[group],
        ],
        confidence="candidate",
    )
    incoming = apply_classification(incoming, tags=raw.get("tags", ""))
    assert incoming.confidence == "verified", (beatmapset_id, group, incoming.confidence)
    incoming.touhou_kind = "mixed" if beatmapset_id == 1528497 else "arrangement"
    _, changed = catalog.merge(incoming)
    assert changed, (beatmapset_id, "expected-new-entry")
    counts[group] += 1
    ids_by[group].append(beatmapset_id)

assert sum(counts.values()) == 11
catalog.save(catalog_path)

doc_path = Path("docs/source-audit-2026-08-night-of-knights.md")
doc = doc_path.read_text(encoding="utf-8")
start = "<!-- NIGHT_MANUAL_WAVE3_START -->"
end = "<!-- NIGHT_MANUAL_WAVE3_END -->"
block = f'''{start}

## Final conservative manual wave and withheld boundary

A final fresh read-only audit of the 94 still-unresolved title-family hits produced **49 unattributed base titles, 15 cover/remix labels, 10 mashup/meme labels, and 20 other variants**. Rather than treating any of those labels or mapper tags as proof, this audit accepts only **11 additional sets** with a direct parent attribution or an independent official/artist-controlled source.

Accepted evidence paths:

- **{counts['direct_parent_metadata']} direct-parent metadata sets**: current osu! metadata explicitly attributes the recording/edit to beatMARIO / COOL&CREATE (or, for set `2051058`, the current source literally states `Touhou Project / beatMARIO`) and the title is a controlled Night-of-Knights derivative/edit. Each was re-fetched immediately before writing and checked against an ID-specific title guard.
- **{counts['official_game_parent']} official-game sets**: Bandai Namco's official Taiko song list credits `Night of Knights / Knight of Nights` as `Touhou Project Arrange / beatMARIO`; KONAMI's official SOUND VOLTEX/e-amusement list credits `ナイト・オブ・ナイツ` to `ビートまりお（COOL&CREATE）`; PLAYISM/Steam's official `Touhou Luna Nights` soundtrack notes explicitly say peposoft re-arranged beatMARIO's `ナイト・オブ・ナイツ` and lists it as Final Boss 3.
- **{counts['koraido_artist_store']} Koraido set**: Koraido's own BOOTH storefront sells the exact work as `【東方アレンジ】ナイト・オブ・ナイツ (Koraido remix)`.

Independent sources used for this final wave:

- Bandai Namco official Taiko song list: https://dondafulfestival-20th.taiko-ch.net/en/music/songlist.php
- KONAMI official SOUND VOLTEX song list: https://p.eagate.573.jp/game/eacsdvx/iii/p/common/info/sdvx_mlist_basic.html
- PLAYISM official Touhou Luna Nights soundtrack announcement: https://playism.com/news/2019/1014/gnf_tlnost-2/
- Steam official Touhou Luna Nights OST page / peposoft comment: https://store.steampowered.com/app/1142470/Touhou_Luna_Nights__Original_Soundtrack/
- Koraido BOOTH search result, tagged as Touhou arrangement: https://booth.pm/ja/search/%E3%83%8A%E3%82%A4%E3%83%88%E3%83%BB%E3%82%AA%E3%83%96%E3%83%BB%E3%83%8A%E3%82%A4%E3%83%84?tags%5B%5D=%E6%9D%B1%E6%96%B9%E3%82%A2%E3%83%AC%E3%83%B3%E3%82%B8

Accepted IDs:

- `direct_parent_metadata`: `{','.join(map(str, ids_by['direct_parent_metadata']))}`
- `official_game_parent`: `{','.join(map(str, ids_by['official_game_parent']))}`
- `koraido_artist_store`: `{','.join(map(str, ids_by['koraido_artist_store']))}`

After this wave, **83 title-family hits remain deliberately withheld**. Typical withheld cases include blank/unknown attribution, mapper-only Touhou tags, BMS/community-pack source labels, phone/nightcore/Black-MIDI variants without a reliable author/composition chain, and meme/mashup uploads where the Night-of-Knights ingredient is plausible but not independently sourced. Examples include `10809` (Unknown / blank source), `1240116` (score farm / source `ur mum`), and `2408535` (a deliberately silent joke file). No withheld set is promoted merely because its title resembles the target song.

{end}'''
if start in doc:
    doc = doc[: doc.index(start)] + block + doc[doc.index(end) + len(end) :]
else:
    doc = doc.rstrip() + "\n\n" + block + "\n"
doc_path.write_text(doc, encoding="utf-8")

print("NIGHT_MANUAL_WAVE3_OK", len(fetched), counts)
