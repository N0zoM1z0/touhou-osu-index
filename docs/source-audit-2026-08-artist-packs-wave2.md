# Official artist-pack audit — 2026-08 wave 2

This audit reviews every beatmapset membership in nine official osu! Featured Artist packs instead of trusting circle/artist identity as proof of Touhou provenance.

## Import policy

`verified_ids` is an explicit per-pack allowlist. For these mixed artist packs the importer:

- fetches the live canonical osu! pack page;
- requires the raw pack to meet `minimum_source_entries`;
- requires every audited ID to still be present;
- emits only the allowlisted IDs with `official_pack_item:<tag>` verified evidence;
- ignores future/unreviewed pack additions until a new audit updates the allowlist.

This preserves the repository rule that a known Touhou circle alone is not verification.

## Results

| Pack | Raw | Verified | Withheld | Current candidate → verified | Current missing verified IDs |
| --- | ---: | ---: | ---: | ---: | ---: |
| A51 Rin | 13 | 13 | 0 | 7 | 0 |
| A18 Demetori | 23 | 23 | 0 | 19 | 0 |
| A33 FELT | 11 | 9 | 2 | 5 | 0 |
| A32 Halozy | 11 | 10 | 1 | 8 | 0 |
| A16 Yuuhei Satellite | 34 | 34 | 0 | 32 | 0 |
| A85 Yuuhei Satellite & Catharsis 2 | 22 | 15 | 7 | 14 | 0 |
| A86 Yuuhei Satellite & Catharsis 3 | 22 | 16 | 6 | 12 | 0 |
| A87 Yuuhei Satellite & Catharsis 4 | 22 | 20 | 2 | 14 | 0 |
| A23 Silver Forest | 30 | 30 | 0 | 23 | 2 |
| **Total** | **188** | **170** | **18** | **134** | **2** |

The other 34 audited Touhou memberships are already verified in the current catalog. The two currently missing verified IDs are `1559` and `2626`, both Silver Forest - Tsurupettan.

## Withheld memberships

These are intentionally not emitted as trusted pack evidence:

- A33 FELT: `206284` **In my room** and `320155` **Clean** — original compositions.
- A32 Halozy: `352351` **Snow Changes to a Beat Again** — original composition by sumijun.
- A85: `154056`, `223048`, `234999`, `242360`, `250337`, `288997` — Kantai Collection; `247319` **Handle Nigitte** — original composition by kamase-tora.
- A86: `347460`, `349810`, `491057`, `562169`, `605290` — Kantai Collection; `495283` **Zouka de Arou to Shita Mono** — arrangement of `二色蓮花蝶 ～ Ancients` from Seihou/Shuusou Gyoku, so it stays candidate under the existing Seihou boundary instead of being promoted as Touhou.
- A87: `1463878` **Daichi ni Saku Senritsu** — original composition by Iceon; `1621390` **Yureru Koi wa Nami no Gotoku (Short Ver.)** — Kantai Collection.

Sixteen of these eighteen were absent from the current catalog and are kept out. `495283` remains candidate. `605290` was already verified only because of `tournament:1432`; this audit found it is actually the Kantai Collection carrier Wo-class image song **Zetsubou no Fuchi**, so this PR adds `manual:excluded` while retaining the old tournament provenance for transparency.

## Cross-check provenance

Primary/canonical pack pages:

- https://osu.ppy.sh/beatmaps/packs/A51
- https://osu.ppy.sh/beatmaps/packs/A18
- https://osu.ppy.sh/beatmaps/packs/A33
- https://osu.ppy.sh/beatmaps/packs/A32
- https://osu.ppy.sh/beatmaps/packs/A16
- https://osu.ppy.sh/beatmaps/packs/A85
- https://osu.ppy.sh/beatmaps/packs/A86
- https://osu.ppy.sh/beatmaps/packs/A87
- https://osu.ppy.sh/beatmaps/packs/A23

The live audit also fetched every one of the 188 public beatmapset pages and recorded its current `source` and tags. Clear Touhou game/source metadata was accepted directly; ambiguous entries were cross-checked against album/artist provenance rather than inferred from the circle name.

Selected ambiguity checks:

- FELT `Clean`: https://vgmdb.net/album/52671 (`Original Track`); `In my room`: https://www.suruga-ya.jp/product/detail/186124615 (`Original Track`).
- Halozy `Snow Changes to a Beat Again`: https://halozy.bandcamp.com/album/snow-melody plus album credits at https://thwiki.cc/Snow_Melody_Instrumental identify track 1 as a sumijun composition rather than a ZUN arrangement.
- Yuuhei/Katharsis originals and Kantai Collection songs were checked against the circle's own discography, including https://www.yuuhei-satellite.jp/2939, https://www.yuuhei-satellite.jp/5882, https://www.yuuhei-satellite.jp/720, and https://www.yuuhei-satellite.jp/5871.
- `Zouka de Arou to Shita Mono`: the circle's official page identifies `二色蓮花蝶 ～ Ancients` as its original: https://www.yuuhei-satellite.jp/5871. osu! metadata identifies this mapping with Seihou, and the repository already treats ZUN-composed Seihou material as candidate-only.
- Silver Forest ambiguity checks include `Tsurupettan` → `竹取飛翔 ～ Lunatic Princess`, `Eternally Unreachable Distance` → `月まで届け、不死の煙`, `1000 Phantasm` → `千年幻想郷`, `Marisa Spark` → `恋色マスタースパーク`, `Phantasm Brigade` → `ネクロファンタジア`, and `萃夢想歌` → `萃夢想`/`東方萃夢想`; see https://thwiki.cc/東方萃奏楽, https://thwiki.cc/東方蒼天歌, https://thwiki.cc/Silver_Forest_2006-2012_BESTⅠ, and https://thwiki.cc/歌词:萃夢想歌.

## Verification

Before the PR is opened, the branch runs fixture tests, `make check`, `make build`, imports each live audited pack and verifies its exact allowlist, audits every configured source and safety floor, and simulates a complete `import-seeds` merge. Temporary audit/apply workflows are removed from the final diff.
