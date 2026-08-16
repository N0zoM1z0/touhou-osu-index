# Official Touhou theme-pack audit — 2026-08 wave 1

This audit records the first follow-up source batch after the tournament-coverage expansion.
Only two official osu! Theme packs are added here; artist/album packs remain out of scope for this PR.

## Trust decision

- `T54` — **Bad Apple!! Pack - Seductive Temptation**: official osu! Theme pack centered on `Bad Apple!!`, the Touhou 4 / Lotus Land Story composition and its arrangements/parodies/mashups.
- `T96` — **The Embodiment of Scarlet Devil Pack**: official osu! Theme pack explicitly centered on Touhou 6 / The Embodiment of Scarlet Devil music and arrangements.
- Both use the repository's existing `official_pack:<tag>` evidence path, which is verified evidence under the current confidence policy.
- Both currently contain exactly 15 unique beatmapsets; `minimum_entries` is therefore pinned to 15 so a truncated or structurally changed source fails closed.

Official source URLs:

- https://osu.ppy.sh/beatmaps/packs/T54
- https://osu.ppy.sh/beatmaps/packs/T96

## Measured catalog intersection

| Pack | Imported | Existing | Missing | Candidate/probable → verified |
| --- | ---: | ---: | ---: | ---: |
| T54 | 15 | 14 | 1 | 9 |
| T96 | 15 | 15 | 0 | 12 |

### Exact IDs

#### T54 — Bad Apple!! Pack - Seductive Temptation

- Promotion IDs: `10353, 19679, 24838, 25356, 28479, 38106, 44300, 150112, 302411`
- Missing IDs: `32003`

#### T96 — The Embodiment of Scarlet Devil Pack

- Promotion IDs: `11264, 11775, 21678, 54674, 107565, 140618, 237116, 325048, 363033, 624572, 683123, 798509`
- Missing IDs: `none`

## Reproduction / checks

The verification branch imported both live osu! pack pages, checked unique beatmapset IDs and the 15-entry safety floors, rejected any overlap with canonical `excluded` entries, ran `make check` and `make build`, audited every configured live source, and simulated the complete `import-seeds` merge without writing `data/catalog.json`.

As with the previous source-only PR, canonical catalog mutations are intentionally not hand-edited here; the new provenance is reproducible through the normal import pipeline.
