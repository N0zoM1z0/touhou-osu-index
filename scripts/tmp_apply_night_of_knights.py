from __future__ import annotations

import unicodedata
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from touhou_osu.catalog import Catalog
from touhou_osu.classifier import apply_classification
from touhou_osu.osu_api import OsuApi, entry_from_osu


def norm(value: str) -> str:
    return "".join(
        ch
        for ch in unicodedata.normalize("NFKC", value or "").casefold()
        if ch.isalnum()
    )


BASE = [
    norm(x)
    for x in [
        "ナイト・オブ・ナイツ",
        "Night of Nights",
        "Night of Knights",
        "Knight of Nights",
    ]
]


def base_family(title: str) -> bool:
    title_n = norm(title)
    return any(token in title_n for token in BASE)


def combined(raw: dict) -> str:
    return norm(
        " ".join(
            [
                raw.get("artist", ""),
                raw.get("title", ""),
                raw.get("source", ""),
            ]
        )
    )


GROUPS: dict[str, list[int]] = {
    "richaadeb_official_cover": [
        980644,
        1069719,
        1091120,
        1124709,
        1185570,
        1206509,
        1237255,
        1242798,
        1248702,
        1387796,
        1440648,
        1474280,
        1491917,
        1637957,
        2156156,
        2346402,
        2540421,
        2553057,
    ],
    "paradot_official_remix": [
        2116110,
        2136000,
        2148515,
        2269337,
        2351463,
        2359033,
        2360975,
    ],
    "coolcreate_first_party_variant": [
        1128048,
        1556967,
        2086454,
        2138418,
        2567202,
        2581537,
    ],
    "chou_super_alias": [2377256, 2406327],
    "falkkone_official_cover": [1314079],
    "marasy_official_cover": [1316202, 2514864],
    "nick_nitro_official_remix": [1326567],
    "parent_attributed_base_or_edit": [
        157478,
        355683,
        360703,
        398092,
        436838,
        496056,
        514686,
        529863,
        599360,
        801144,
        887683,
        1064108,
        1110991,
        1257327,
        1264459,
        1365207,
        1393896,
        1434008,
        1501621,
        1626057,
        2187567,
        2255745,
        2336636,
        2414814,
        2523604,
    ],
}

ID_TO_GROUP = {
    beatmapset_id: group
    for group, beatmapset_ids in GROUPS.items()
    for beatmapset_id in beatmapset_ids
}
assert len(ID_TO_GROUP) == 62

FIRST_PARTY_REQUIRED = {
    1128048: ("crankyremix",),
    1556967: ("amaterasrecordsremix",),
    2086454: ("camellia", "remix"),
    2138418: ("xi", "remix"),
    2567202: ("hachiojipremix",),
    2581537: ("gamever",),
}


def validate_group(beatmapset_id: int, group: str, raw: dict) -> None:
    title = raw.get("title", "")
    artist = raw.get("artist", "")
    all_n = combined(raw)
    assert base_family(title), (beatmapset_id, group, "title-family-drift", artist, title)

    if group == "richaadeb_official_cover":
        assert "richaad" in norm(artist + " " + title), (beatmapset_id, group, artist, title)
    elif group == "paradot_official_remix":
        assert "paradot" in norm(artist + " " + title), (beatmapset_id, group, artist, title)
    elif group == "coolcreate_first_party_variant":
        title_artist = norm(artist + " " + title)
        assert all(token in title_artist for token in FIRST_PARTY_REQUIRED[beatmapset_id]), (
            beatmapset_id,
            group,
            artist,
            title,
        )
    elif group == "chou_super_alias":
        title_n = norm(title)
        assert "supernightofnights" in title_n or "supernightofknights" in title_n, (
            beatmapset_id,
            group,
            artist,
            title,
        )
        assert "beatmario" in all_n or "coolcreate" in all_n, (
            beatmapset_id,
            group,
            artist,
            title,
        )
    elif group == "falkkone_official_cover":
        assert "falkkone" in norm(artist), (beatmapset_id, group, artist, title)
    elif group == "marasy_official_cover":
        artist_n = norm(artist)
        assert "marasy" in artist_n or "まらしぃ" in artist_n, (
            beatmapset_id,
            group,
            artist,
            title,
        )
    elif group == "nick_nitro_official_remix":
        assert "nicknitro" in norm(artist), (beatmapset_id, group, artist, title)
    elif group == "parent_attributed_base_or_edit":
        assert "beatmario" in all_n or "coolcreate" in all_n, (
            beatmapset_id,
            group,
            artist,
            title,
            raw.get("source", ""),
        )
    else:
        raise AssertionError((beatmapset_id, "unknown-group", group))


EVIDENCE_BY_GROUP = {
    "richaadeb_official_cover": "corroboration:richaadeb-official-night-of-nights-cover",
    "paradot_official_remix": "corroboration:para-dot-official-night-of-knights-remix",
    "coolcreate_first_party_variant": "corroboration:cool-create-all-night-of-knights",
    "chou_super_alias": "corroboration:cool-create-chou-night-of-knights",
    "falkkone_official_cover": "corroboration:falkkone-official-night-of-nights-cover",
    "marasy_official_cover": "corroboration:marasy-official-night-of-knights-cover",
    "nick_nitro_official_remix": "corroboration:nick-nitro-official-night-of-nights-remix",
    "parent_attributed_base_or_edit": "corroboration:cool-create-night-of-knights-parent",
}

catalog_path = Path("data/catalog.json")
catalog = Catalog.load(catalog_path)
pending = [beatmapset_id for beatmapset_id in sorted(ID_TO_GROUP) if beatmapset_id not in catalog.entries]
assert len(pending) in {0, 62}, (len(pending), pending)
if not pending:
    print("NIGHT_MANUAL_WAVE2_ALREADY_COMPLETE")
    raise SystemExit(0)

api = OsuApi.from_env()
api.token()


def fetch(beatmapset_id: int) -> tuple[int, str, dict]:
    raw = api.beatmapset(beatmapset_id)
    assert int(raw["id"]) == beatmapset_id
    group = ID_TO_GROUP[beatmapset_id]
    validate_group(beatmapset_id, group, raw)
    return beatmapset_id, group, raw


with ThreadPoolExecutor(max_workers=8) as pool:
    fetched = list(pool.map(fetch, pending))

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
    incoming.touhou_kind = "arrangement"
    incoming = apply_classification(incoming, tags=raw.get("tags", ""))
    assert incoming.confidence == "verified", (
        beatmapset_id,
        group,
        incoming.confidence,
        incoming.source,
    )
    _, changed = catalog.merge(incoming)
    assert changed, (beatmapset_id, "expected-new-entry")
    counts[group] += 1
    ids_by[group].append(beatmapset_id)

assert sum(counts.values()) == 62
catalog.save(catalog_path)

doc_path = Path("docs/source-audit-2026-08-night-of-knights.md")
doc = doc_path.read_text(encoding="utf-8")
start = "<!-- NIGHT_MANUAL_WAVE2_START -->"
end = "<!-- NIGHT_MANUAL_WAVE2_END -->"
block = f'''{start}

## Manual composition-chain wave

After the automatic/fail-closed 284-set wave, the remaining 156 title-family hits were reviewed by composition chain rather than by keyword. A second **62-set** wave is accepted with sticky `manual:verified` evidence. Every accepted set was direct-refetched again immediately before writing and had to pass a group-specific artist/title guard on the fresh response.

Primary / artist-controlled corroboration used for this wave:

- COOL&CREATE 2018 all-`ナイト・オブ・ナイツ` release: https://cool-create.cc/cd/cccd50/
- COOL&CREATE 2019 `ルナティック` release: https://cool-create.cc/cd/cccd59/
- COOL&CREATE 2025 `プロジェクト` release: https://cool-create.cc/cd/cccd75/
- RichaadEB Official Artist Channel, `NIGHT OF NIGHTS (Flowering Night) || Metal Cover`: https://www.youtube.com/watch?v=ugqjcXjpCts
- Para Dot. official channel, `Night of Knights（Para Dot. Remix）`: https://www.youtube.com/watch?v=Qju7jPjXPNE
- FalKKonE Official Artist Channel, `Touhou - Night of Nights [Intense Symphonic Metal Cover]`: https://www.youtube.com/watch?v=bQI9xedYQQE
- marasy8 Official Artist Channel, `「ナイト・オブ・ナイツ」を弾き直してみたんですが...`: https://www.youtube.com/watch?v=OyUJnV2R-5g
- Nick Nitro verified channel, `Touhou - Night Of Nights [Ver. 3] [NITRO Remix]`: https://www.youtube.com/watch?v=2N2s0f5fRsc

Accepted groups:

- RichaadEB official metal-cover family: **{counts['richaadeb_official_cover']}**
- Para Dot. explicit remix-of-remix family: **{counts['paradot_official_remix']}**
- COOL&CREATE first-party named variants missed by the strict first pass: **{counts['coolcreate_first_party_variant']}**
- English `Super Night of Nights` / `Super Night of Knights` alias of `超ナイト・オブ・ナイツ`: **{counts['chou_super_alias']}**
- FalKKonE official cover: **{counts['falkkone_official_cover']}**
- marasy official piano-cover family: **{counts['marasy_official_cover']}**
- Nick Nitro official remix: **{counts['nick_nitro_official_remix']}**
- Base/edit uploads whose fresh osu! metadata itself directly attributes the recording to beatMARIO / COOL&CREATE: **{counts['parent_attributed_base_or_edit']}**

These 62 are arrangements/covers/edits of the beatMARIO parent, not merely independent arrangements of `フラワリングナイト`. The other **94** unresolved title-family hits remain held for additional review; no confidence is inferred from title tokens alone.

<details><summary>Manual wave IDs by group</summary>

{chr(10).join(f'- `{group}`: '+','.join(map(str, ids_by[group])) for group in GROUPS)}

</details>

{end}'''
if start in doc:
    doc = doc[: doc.index(start)] + block + doc[doc.index(end) + len(end) :]
else:
    doc = doc.rstrip() + "\n\n" + block + "\n"
doc_path.write_text(doc, encoding="utf-8")

print("NIGHT_MANUAL_WAVE2_OK", len(fetched), counts)
