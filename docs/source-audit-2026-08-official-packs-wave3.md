# Official pack audit — 2026-08 wave 3

This wave extends the per-item official-pack policy to an older album pack,
Featured Artist mini-packs and modern Beatmap Spotlights. Spotlight membership
alone is **not** treated as Touhou evidence; every emitted ID is frozen in an
explicit allowlist and retains the evidence tag of the exact canonical pack it
came from.

## Discovery scope

A read-only osu! API scan enumerated 154 Featured packs and 342 chart (`R`)
packs. The Spotlight pass reviewed all 56 chart packs dated 2020 or later.
Potential rows were first intersected with the canonical catalog, explicit
Touhou source metadata and known Touhou artists, then individually narrowed.

The final proposal contains **42 canonical pack pages**, **91 audited pack
memberships**, and **84 unique beatmapsets**. Against the pre-wave live source
universe (6,796 source records / 41 sources / 3,022 unique beatmapsets):

- **47** IDs were absent from every configured live source and from the
  canonical catalog;
- **21** existing candidate/probable IDs gain audited official-pack evidence;
- **16** existing verified IDs gain redundant official provenance.

## Album / Featured Artist decisions

- `A2` Secret Seven: **6/7**. SYNC.ART'S official discography identifies
  `I will -Short-` as the album's original composition and the remaining six
  tracks as Touhou arrangements. Beatmapset `4135` is therefore not trusted;
  this audit also corrects its existing false-positive `osu_source` status with
  `manual:excluded`.
- `FQ70` BLANKFIELD: **4/4** audited Touhou items.
- `FQ66` A-One: **6/6** audited Touhou items; all six were missing from the
  prior source universe.
- `FQ40` LeaF: **1/3**. Only `Arianrhod` (`1128939`, EoSD) is included;
  `Mopemope` and `I` are not Touhou works.

Primary/canonical references include:

- https://syncarts.jp/cd/etclist.htm
- https://osu.ppy.sh/beatmaps/artists/148
- https://osu.ppy.sh/beatmaps/artists/28
- https://osu.ppy.sh/beatmaps/packs/A2
- https://osu.ppy.sh/beatmaps/packs/FQ70
- https://osu.ppy.sh/beatmaps/packs/FQ66
- https://osu.ppy.sh/beatmaps/packs/FQ40

## Modern Spotlight allowlists

Only per-item reviewed Touhou rows are emitted; no Spotlight pack is trusted as
a whole. Specific recognized Touhou game sources follow the repository's
existing exact-source rule. Generic `Touhou` source rows were separately
cross-checked because A2 demonstrates that mapper-entered source metadata can
be wrong. Representative checks include FELT `BRIGHTEST WAY`, Halozy
`Genryuu Kaiko` / `Paranoid Lost`, LeaF `Calamity Fortune`, tsunamix
`Period.`, Kurokotei `Galaxy Collapse`, 3L `Amoritachite Kami to Miyu`, FELT
`Goldrop`, IOSYS `Endless Tewi-ma Park`, Chata `Remind`, and Meramipop
`Rakujitsu Romance` against artist/album provenance.

| Pack | Name | Raw | Audited Touhou | Frozen beatmapset IDs |
| --- | --- | ---: | ---: | --- |
| `A2` | Gojou Kai - Secret Seven | 7 | 6 | `3573, 3847, 3862, 3875, 4077, 4134` |
| `FQ70` | BLANKFIELD high tempo mini-pack | 4 | 4 | `1171995, 1175382, 1185325, 1201974` |
| `FQ66` | A-One Pack | 6 | 6 | `1474048, 1480185, 1499636, 1543564, 1633053, 1644488` |
| `FQ40` | LeaF mini-pack | 3 | 1 | `1128939` |
| `R341` | Beatmap Spotlights: Winter 2026 (osu!catch) | 27 | 2 | `1980463, 2020128` |
| `R340` | Beatmap Spotlights: Winter 2026 (osu!taiko) | 27 | 1 | `2159203` |
| `R339` | Beatmap Spotlights: Winter 2026 (osu!) | 27 | 3 | `304022, 462878, 1924253` |
| `R338` | Beatmap Spotlights: Summer 2025 (osu!mania) | 27 | 1 | `2288990` |
| `R337` | Beatmap Spotlights: Summer 2025 (osu!catch) | 27 | 4 | `1220848, 1531490, 2221973, 2281583` |
| `R336` | Beatmap Spotlights: Summer 2025 (osu!taiko) | 27 | 1 | `2049581` |
| `R335` | Beatmap Spotlights: Summer 2025 (osu!) | 27 | 1 | `2282492` |
| `R334` | Beatmap Spotlights: Spring 2025 (osu!mania) | 27 | 1 | `2141740` |
| `R333` | Beatmap Spotlights: Spring 2025 (osu!catch) | 27 | 3 | `2000358, 2019552, 2151953` |
| `R332` | Beatmap Spotlights: Spring 2025 (osu!taiko) | 27 | 2 | `1919687, 2220709` |
| `R331` | Beatmap Spotlights: Spring 2025 (osu!) | 27 | 3 | `1842664, 1942555, 2239541` |
| `R328` | Beatmap Spotlights: Autumn 2023 (osu!taiko) | 26 | 1 | `1590156` |
| `R327` | Beatmap Spotlights: Autumn 2023 (osu!) | 27 | 1 | `1381715` |
| `R326` | Beatmap Spotlights: Spring 2023 (osu!mania) | 27 | 1 | `572338` |
| `R325` | Beatmap Spotlights: Spring 2023 (osu!catch) | 27 | 3 | `253969, 307818, 1872426` |
| `R324` | Beatmap Spotlights: Spring 2023 (osu!taiko) | 27 | 1 | `96103` |
| `R323` | Beatmap Spotlights: Spring 2023 (osu!) | 27 | 4 | `29044, 41974, 1638844, 1898383` |
| `R322` | Beatmap Spotlights: Winter 2023 (osu!mania) | 21 | 2 | `1324800, 1670404` |
| `R319` | Beatmap Spotlights: Winter 2023 (osu!) | 27 | 2 | `1024028, 1575475` |
| `R318` | Beatmap Spotlights: Summer 2022 (osu!mania) | 27 | 1 | `166146` |
| `R317` | Beatmap Spotlights: Summer 2022 (osu!catch) | 27 | 2 | `114741, 1110955` |
| `R316` | Beatmap Spotlights: Summer 2022 (osu!taiko) | 27 | 3 | `1155202, 1630732, 1762719` |
| `R315` | Beatmap Spotlights: Summer 2022 (osu!) | 27 | 2 | `1742131, 1774999` |
| `R314` | Beatmap Spotlights: Spring 2022 (osu!mania) | 27 | 2 | `400078, 1656541` |
| `R312` | Beatmap Spotlights: Spring 2022 (osu!taiko) | 26 | 3 | `452051, 1506936, 1526077` |
| `R311` | Beatmap Spotlights: Spring 2022 (osu!) | 27 | 3 | `795140, 1004248, 1670776` |
| `R309` | Beatmap Spotlights: Winter 2022 (osu!catch) | 27 | 3 | `1023485, 1480185, 1644488` |
| `R308` | Beatmap Spotlights: Winter 2022 (osu!taiko) | 27 | 2 | `1013884, 1263550` |
| `R305` | Beatmap Spotlights: Spring 2021 (osu!catch) | 20 | 1 | `633255` |
| `R304` | Beatmap Spotlights: Spring 2021 (osu!taiko) | 20 | 1 | `405516` |
| `R303` | Beatmap Spotlights: Spring 2021 (osu!) | 20 | 2 | `198034, 1132649` |
| `R301` | Beatmap Spotlights: Winter 2021 (osu!catch) | 20 | 1 | `204927` |
| `R300` | Beatmap Spotlights: Winter 2021 (osu!taiko) | 20 | 2 | `96103, 812992` |
| `R297` | Beatmap Spotlights: Autumn 2020 (osu!catch) | 19 | 1 | `972764` |
| `R296` | Beatmap Spotlights: Autumn 2020 (osu!taiko) | 20 | 1 | `812992` |
| `R293` | Beatmap Spotlights: Summer 2020 (osu!catch) | 20 | 4 | `48874, 204927, 998578, 1023485` |
| `R291` | Beatmap Spotlights: Summer 2020 (osu!) | 20 | 2 | `37292, 145976` |
| `R288` | Seasonal Spotlights: Winter 2020 (osu!taiko) | 4 | 1 | `1013884` |

## Rate-limit and fail-closed design

The 42 pack pages are grouped under one `official_pack_batches` source. Nested
packs still use the existing `import_official_pack` safety checks: duplicate
allowlist IDs are rejected, the live raw pack must meet its
`minimum_source_entries` floor, and every frozen ID must still exist upstream.
The batch imports nested packs sequentially with a 1.05-second delay, merges
duplicate Spotlight memberships while unioning their per-pack evidence, and
fails its outer 84-entry floor if coverage shrinks.

`hydrate` also recognizes `official_pack:` and `official_pack_item:` evidence,
so newly discovered pack-only records can obtain public osu! source/status/mode
metadata without OAuth while keeping their audited verified evidence.

## Sticky Seihou boundary discovered during full merge

The complete seed-merge simulation exposed a pre-existing interaction that a
pack-only test would miss: beatmapset `495283` (`Zouka de Arou to Shita Mono`)
was correctly stored as a Seihou candidate in the canonical catalog, but the
trusted Gensokyo Cup 2 membership (`tournament:google_sheet:gensokyo-cup-2`)
promoted it back to verified during every full source refresh. The track is an
arrangement of `二色蓮花蝶 ～ Ancients` from Seihou / Shuusou Gyoku, so the
repository's existing Seihou rule says it must remain candidate.

This wave therefore adds a narrow `manual:candidate` sticky override. It keeps
all discovery/tournament provenance, remains reviewable, and outranks automatic
pack/tournament promotion without mislabeling the track as unrelated. Both the
classifier and catalog merge path have regression tests for this state.

## Reproduction

Before the PR is opened, the branch runs unit tests, `make check`, `make build`,
a live exact batch import, a full source audit, a complete `import-seeds`
simulation, and boundary checks for `4135`, `605290`, and `495283`. Temporary
scan/apply tooling is removed from the final diff.
