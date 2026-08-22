# ボーダーオブライフ / Border of Life systematic search audit

Date: 2026-08-22

## Scope

This audit targets ZUN's `ボーダーオブライフ`, the Stage 6 boss second theme from `東方妖々夢 ～ Perfect Cherry Blossom.`. It deliberately distinguishes that composition from the separate Stage 6 theme `幽雅に咲かせ、墨染の桜 ～ Border of Life`, even though osu! titles and English-language discographies often shorten either work to `Border of Life`.

Search-title similarity is discovery evidence only. A set is accepted into this audit only after its current public osu! beatmapset identity is resolved and its recording can be tied to the target composition by explicit game/source metadata or composition-level discography evidence.

## Composition ground truth

The main arrangement corpus is Touhou Arrangement Chronicle's original-song page for `ボーダーオブライフ`:

- https://touhou.arrangement-chronicle.com/original_song/%E6%9D%B1%E6%96%B9%E5%A6%96%E3%80%85%E5%A4%A2/%E3%83%9C%E3%83%BC%E3%83%80%E3%83%BC%E3%82%AA%E3%83%96%E3%83%A9%E3%82%A4%E3%83%95

The page identifies the original game as Perfect Cherry Blossom and exposes a large arrangement corpus. Its live arrangement / circle / album counts are volatile and are not used as an acceptance criterion; the page is used as a discovery and composition-chain reference, not as proof that every search hit is in scope.

Important cross-checks used for ambiguous recordings:

- `SYNC.ART'S - ボーダーオブライフ` from `Secret Seven` is explicitly listed as a **mixed arrangement** of both `幽雅に咲かせ、墨染の桜 ～ Border of Life` and `ボーダーオブライフ` on the Arrangement Chronicle target page.
- `IOSYS - Border of extacy` and its karaoke version are explicitly listed there as **mixed arrangements** of `ボーダーオブライフ` and `ネクロファンタジア`.
- `Rin - Ayakashi set 12 Another ～ ボーダーオブライフ` is documented by Touhou Wiki as an arrangement of `ボーダーオブライフ`: https://en.touhouwiki.net/wiki/House_set_of_%22Perfect_Cherry_Blossom%22
- `GET IN THE RING - Phosphor` is documented as a mixed arrangement of `ボーダーオブライフ` and `ゴーストリード`: https://en.touhouwiki.net/wiki/Lyrics%3A_Phosphor and https://touhou.arrangement-chronicle.com/circle/GET%20IN%20THE%20RING/arrange_songs
- `nazz-can - ボーダーオブライフ` is explicitly mapped to the target composition in `桜華幻奏`: https://thwiki.cc/%E6%A1%9C%E8%8F%AF%E5%B9%BB%E5%A5%8F

## Applied catalog changes

The implementation re-fetches every accepted beatmapset from its public osu! beatmapset page immediately before writing. The audit adds **4 previously absent beatmapsets**:

| Beatmapset | Recording | Classification | Structured originals |
| ---: | --- | --- | --- |
| `14408` | Nazz-can - Border of Life | arrangement | `ボーダーオブライフ` |
| `1248505` | GET IN THE RING - Phosphor | mixed | `ボーダーオブライフ`; `ゴーストリード` |
| `2258223` | ZUN - Border of Life | original | `ボーダーオブライフ` |
| `2443688` | ZUN - Border of Life | original | `ボーダーオブライフ` |

`1248505` has a blank osu! source, so its verified judgment is sticky (`manual:verified`) and rests on the independent composition-level sources above. The other three current osu! pages carry explicit Touhou / Perfect Cherry Blossom source metadata.

The audit also enriches **8 existing catalog rows** with structured composition provenance and refreshes their current public metadata:

| Beatmapset | Recording | Classification | Structured originals |
| ---: | --- | --- | --- |
| `3573` | Gojou Kai - Border of Life | mixed | `幽雅に咲かせ、墨染の桜 ～ Border of Life`; `ボーダーオブライフ` |
| `7932` | IOSYS - Border of Extacy | mixed | `ボーダーオブライフ`; `ネクロファンタジア` |
| `28891` | Gojou Kai - Border of Life | mixed | same Secret Seven recording / originals as `3573` |
| `732190` | IOSYS - Border of extacy (Karaoke Ver) | mixed | `ボーダーオブライフ`; `ネクロファンタジア` |
| `819351` | IOSYS - Border of extacy (Karaoke Ver) | mixed | `ボーダーオブライフ`; `ネクロファンタジア` |
| `1001360` | Rin - Ayakashi set 12 Another ~ Border of Life | arrangement | `ボーダーオブライフ` |
| `1235944` | Rin - Ayakashi set 12 Another ~ Border of Life | arrangement | `ボーダーオブライフ` |
| `1953606` | ZUN - Border of Life | original | `ボーダーオブライフ` |

The earlier audit draft had held `732190` and `1235944` because their wrapper identity could not be directly re-verified at that time. Both public osu! beatmapset pages resolve on 2026-08-22, so that temporary identity boundary no longer applies. Their existing confidence/provenance is preserved; this audit only refreshes public metadata and adds composition structure.

## Explicit false-positive boundary

The following title-family hits were reviewed but are **not** target-composition additions:

- `1168786` — BLANKFIELD - Border Of Life
- `2249236` — SOUND HOLIC - Border of Life
- `388424` — Aojiru - Border of Life
- `12508` — Silver Forest - Sakase * Sakase
- `17628` — SYNC.ART'S feat. Sakaue Nachi - Forever Cherryblossom

These resolve to `幽雅に咲かせ、墨染の桜 ～ Border of Life` or otherwise fail the target-composition chain. In particular, the Arrangement Chronicle page for the Sumizome theme separately lists `Forever cherryblossom`, demonstrating why English `Border of Life` tokens cannot be treated as an exact composition key:

- https://touhou.arrangement-chronicle.com/original_song/%E6%9D%B1%E6%96%B9%E5%A6%96%E3%80%85%E5%A4%A2/%E5%B9%BD%E9%9B%85%E3%81%AB%E5%92%B2%E3%81%8B%E3%81%9B%E3%80%81%E5%A2%A8%E6%9F%93%E3%81%AE%E6%A1%9C%E3%80%80%EF%BD%9E%20Border%20of%20Life

A historical OCL Fall 2024 pool reference to `ZUN - Border of Life (perchance) [Final Stage]` remains documentation-only because the audit still has no direct numeric beatmapset identity to merge. A textual pool label is not enough to invent an ID.

## Reproducibility and write boundary

1. Start from the documented target composition, not from the ambiguous English display title.
2. Search exact/direct aliases plus arrangement-title/artist tuples obtained from composition-level sources.
3. Compare numeric beatmapset IDs against the catalog before review.
4. Direct-refetch each retained ID from its current public osu! beatmapset page.
5. Require explicit source metadata or an independently documented composition chain before verification.
6. Record mixed works with all supported Touhou originals instead of forcing them into a single-theme arrangement bucket.
7. Preserve false positives and unresolved identities in the audit rather than silently accepting or guessing them.
8. Save through `Catalog.save(data/catalog)` so numeric ordering, shard placement, and recursive shard limits remain deterministic.
9. Run `make check`, `make build`, and `git diff --check` before committing the shard changes.

## Implementation validation

The completed shard migration was exercised in GitHub Actions `Validate` run **#217** on 2026-08-22. The migration direct-refetched all 12 retained beatmapsets, applied the remaining six enrichments and two additions on top of the four records already staged earlier in the branch, and saved through the canonical `Catalog.save(data/catalog)` path.

The validated post-audit catalog contains **3,993 beatmapsets** (`candidate=1641`, `excluded=2`, `probable=29`, `verified=2321`) with **2,350 accepted** records. `make check` ran **63 tests**, all passing; `make build` produced 2,350 accepted beatmapsets; and `git diff --check` passed before the validated data tree was committed. The one-shot migration helper removed itself and restored `.github/workflows/validate.yml` to the normal read-only workflow before pushing. The resulting tree was then squashed into the PR's final history and separately passed the normal pull-request validation workflow, so no migration machinery remains in the final PR diff.
