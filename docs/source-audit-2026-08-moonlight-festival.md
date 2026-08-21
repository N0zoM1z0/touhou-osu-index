# Touhou Moonlight Festival source audit — 2026-08-21

## Decision

Add Touhou Moonlight Festival as a **partially trusted, explicitly audited Google Sheet tournament source** rather than trusting the whole mappool wholesale.

The final allowlist contains **94 exact beatmap → beatmapset mappings**:

- 65 mappings point to beatmapsets that were already `verified` before this audit; they receive only the new Moonlight Festival provenance token.
- 29 mappings add previously missing beatmapsets as `verified`.
- 40 other tournament members that were already catalogued as non-verified candidates are deliberately **not** promoted and do not receive trusted Moonlight evidence.
- 1 spreadsheet beatmap is currently unresolved by the official osu! API and is withheld.
- 2 additional resolved beatmapsets are conservatively withheld after item-level review.

This deliberately favors precision over complete tournament coverage.

## Primary provenance

- Official osu! forum topic: <https://osu.ppy.sh/community/forums/topics/2029871>
- Official public spreadsheet linked from that topic: <https://docs.google.com/spreadsheets/d/1nqD85CClkgNIHxMU2KVGfcs2i5QphzIEupGxuiqlf04/edit>
- Selected worksheet: exact tab `Маппул`

The forum introduction describes Touhou Moonlight Festival as a 2v2 tournament dedicated to the **Touhou Project** universe with a thematic mappool. The spreadsheet contains the actual round pools from Grand Finals through qualifiers.

## Spreadsheet format and fail-closed import

This sheet does **not** store modern `/beatmapsets/<id>` links. Its mappool rows use legacy difficulty links of the form:

```text
https://osu.ppy.sh/b/<beatmap_id>
```

Treating those numbers as beatmapset IDs would be incorrect. The importer therefore keeps beatmap IDs and beatmapset IDs as separate types of evidence:

1. `fetch_google_sheet_beatmap_ids` reads only `/b/<id>` or `/beatmaps/<id>` links from the configured worksheet.
2. The reviewed config stores an explicit `audited_beatmaps` mapping of `beatmap_id` → `beatmapset_id`.
3. Every source import re-checks that every audited beatmap ID is still present in the exact `Маппул` worksheet.
4. `minimum_source_beatmaps: 137` fails closed if the public mappool is truncated or structurally replaced.
5. The source is marked `trusted: false`; only the explicit audited subset receives `tournament:google_sheet:tmf-2025:audited` verified evidence.

This preserves the existing semantics of other Google Sheet tournament sources while making legacy `/b/` sheets reproducible without ever confusing difficulty IDs with set IDs.

## Live audit counts

The 2026-08-21 audit against the post-#24 catalog produced:

| Check | Count |
| --- | ---: |
| Unique `/b/` beatmap IDs in exact `Маппул` tab | 137 |
| Beatmap IDs resolvable through official osu! API | 136 |
| Unique resolved beatmapsets | 136 |
| Already in catalog | 105 |
| Already `verified` | 65 |
| Already non-verified candidate | 40 |
| Missing from catalog | 31 |
| New accepted after item-level audit | 29 |
| New withheld after item-level audit | 2 |
| Final audited mappings | 94 |

The one currently unresolved spreadsheet difficulty is beatmap ID **3362650**. `/api/v2/beatmaps/3362650` returned HTTP 404 during repeated audits, so no beatmapset ID was guessed from its displayed song text.

## New beatmapsets accepted

The 29 newly added beatmapsets are:

```text
1559
1785
131070
697230
889029
1084161
1092488
1183572
1524066
1556672
1668647
1678329
1857465
1876059
1880545
1881398
1988714
2040705
2087326
2088927
2112194
2127697
2182178
2183932
2189223
2191004
2215054
2315202
2347215
```

Twenty-two of these had current osu! `source` metadata that independently matched the repository's explicit Touhou source rules. Seven had weaker osu! source metadata and were admitted only after separate composition-level corroboration.

### Seven weak-metadata additions independently corroborated

| Beatmapset | Catalog title / identity | Independent corroboration |
| ---: | --- | --- |
| 1559 | Silver Forest — `Tsurupettan` | Silver Forest discography references identify `つるぺったん` as an arrangement of `竹取飛翔 ～ Lunatic Princess` from `東方永夜抄`: <https://w.atwiki.jp/toho/pages/6944.html> |
| 1785 | Nico Nico Douga — `U.N. Owen Was Her?` | Touhou Wiki identifies `U.N. Owen Was Her?` as composed by ZUN for *Embodiment of Scarlet Devil*: <https://en.touhouwiki.net/index.php?title=U.N._Owen_Was_Her%3F> |
| 889029 | BUTAOTOME — `Warp On` | BUTAOTOME song index lists `Warp on` with original theme `Yoru ga Oritekuru ~ Evening Star`: <https://tiramisucowboy.com/list-of-songs/> |
| 1092488 | FELT — `Last Wind` | Touhou Arrangement Chronicle lists `Last Wind` with original `風神少女`: <https://touhou.arrangement-chronicle.com/circle/FELT/arrange_songs> |
| 1876059 | LULICO vs LOLIPO — `We hate Touhou` | KINZOK ON's album page lists the track's original as `妖怪寺へようこそ` and credits the originals to ZUN: <https://kinzoku.xxxxxxxx.jp/kzon011.html> |
| 2182178 | 25-ji, Nightcord de. x Hatsune Miku — `Bad Apple!! feat.SEKAI` | SEGA's Project SEKAI announcement explicitly calls it a Touhou Project collaboration track and credits composition to ZUN: <https://prtimes.jp/main/html/rd/p/000005748.000005397.html> |
| 2191004 | TatshMusicCircle feat. Tsukiko — `Floating Darkness...` | Touhou arrange indexes identify its original as `平安のエイリアン`: <https://thwiki.cc/index.php?setlang=ja&title=%E6%AD%8C%E8%AF%8D%3AFloating_Darkness...> |

These items still receive tournament provenance rather than fabricated `manual:verified` evidence; the corroboration above documents why they were safe to include in the audited subset despite weak current osu! source strings.

## Conservative exclusions

### Beatmapset 1263067

Current osu! metadata is damaged/insufficient (`rnako`, blank title/source in the live audit), and the audit did not find reliable independent evidence that uniquely identifies the underlying composition. It is withheld rather than inferred from neighboring pool context.

### Beatmapset 2205921

The current source points to `东方祈华梦 ～ Elegant Impermanence of Sakura`, and `Quenching Rain of Mystical Skies` is documented as that fangame's own Extra Stage theme. The game's music page describes the composer providing tracks *in the style of* original Touhou works rather than identifying this track as a ZUN composition or arrangement: <https://en.touhouwiki.net/wiki/Elegant_Impermanence_of_Sakura/Music>

Because this repository is being conservative about distinguishing Touhou Project compositions/arrangements from original music written for Touhou fangames, this set is withheld from the audited verified subset.

### Beatmap ID 3362650

The spreadsheet entry remains visible, but the official osu! API currently returns 404 for this difficulty. No beatmapset mapping is stored until an authoritative osu! endpoint can resolve it again.

## Final verification

A final read-only audit was run against the exact PR data and current upstream sources. It verified all of the following:

- Base catalog: 3,594 entries; PR catalog: 3,623 entries.
- Exactly 29 new beatmapsets were added.
- Exactly 65 pre-existing records changed, and their only substantive change was adding `tournament:google_sheet:tmf-2025:audited` evidence; existing metadata and confidence were unchanged.
- The 40 pre-existing non-verified Moonlight members were untouched.
- All 94 configured beatmap IDs still existed in the live `Маппул` worksheet.
- All 94 beatmap → beatmapset mappings were re-resolved through the official osu! API with **0 mismatches**.
- All 29 new beatmapsets were directly re-fetched with **0 artist/title/creator/source/status/mode mismatches**.
- Beatmapsets 1263067 and 2205921 remained absent.
- Beatmap 3362650 still failed official API resolution and remained absent.
- Full test suite: **55 tests passed**.
- Catalog validation and `git diff --check` passed.

The result is intentionally narrower than the complete tournament pool: only entries with a reproducible mapping and sufficiently strong item-level provenance are published as verified coverage.
