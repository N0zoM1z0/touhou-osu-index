# Touhou source coverage audit — 2026-08

This audit records the evidence behind the August 2026 source-coverage expansion. The goal is to improve recall without weakening the catalog's provenance rules: Touhou-only tournament pools may be trusted, while mixed pools and broad artist/circle searches remain candidate-first.

## Confirmed additions

### Osu! Gensokyo Cup (2025 JP)

- Official forum: https://osu.ppy.sh/community/forums/topics/2089185
- Main Sheet: https://docs.google.com/spreadsheets/d/1RSBgpsQgySPZLs9PY6ZarAubviObqA3WW544yErx7Cg/edit?gid=0
- Rule evidence: the official forum states that all maps are related to Touhou Project.
- Reproduction: export the public workbook as XLSX and inspect the `Mappools` worksheet.
- Audited result: **40 unique beatmapset IDs**.
- Policy: **trusted / verified** tournament evidence.
- Config safety floor: 35 records.

### -Gensokyo Cup 2 (2020)

- Official forum: https://osu.ppy.sh/community/forums/topics/1076292
- Main Sheet: https://docs.google.com/spreadsheets/d/18uHc21MYRDZgyNwvP7WBOJXJH3jbXtehQEb4OXZ913g/edit?usp=sharing
- Rule evidence: the official forum explicitly says all maps are chosen with a Touhou theme.
- Reproduction: export the public workbook as XLSX and inspect every worksheet whose name starts with `Mappool` (the current workbook uses Human/Yokai pool tabs across stages).
- Audited result: **148 unique beatmapset IDs**.
- Policy: **trusted / verified** tournament evidence.
- Config safety floor: 140 records.

### 5 Digit Touhou Cup 1 qualifiers (2023)

- Official forum: https://osu.ppy.sh/community/forums/topics/1766738
- Preserved osu!Collector qualifiers collection: https://osucollector.com/collections/12493/5-Digit-Touhou-Cup-Qualifiers
- The tournament description says it features Touhou-only pools, **but also explicitly permits swapping categories to non-Touhou maps if necessary and allows an OTH (other) category**.
- Therefore the complete tournament must not be blanket-trusted.
- The preserved qualifiers collection contains 11 maps at audit time and is imported as **candidate discovery evidence only**.
- Config safety floor: 10 records.

## Live catalog intersection results

A branch-only GitHub Actions verification run on 2026-08-16 re-imported all three new sources from their live upstream data and compared them against the checked-in canonical catalog before opening the PR.

| Source | Imported | Already in catalog | Missing from catalog | Current candidates promoted by this source | Already accepted and reinforced |
| --- | ---: | ---: | ---: | ---: | ---: |
| Osu! Gensokyo Cup 2025 JP | 40 | 30 | 10 | **6** | 24 |
| -Gensokyo Cup 2 | 148 | 133 | 15 | **63** | 70 |
| 5 Digit Touhou Cup 1 qualifiers | 11 | 9 | 2 | **0** | 6 |

The trusted tournament sources therefore add strong evidence for **69 existing candidate beatmapsets** and expose **25 beatmapsets not currently in the catalog**. The 5DTC1 qualifier source intentionally promotes none on its own.

The same live run audited every configured source and returned **6,596 source records from 30 sources, representing 3,019 unique beatmapsets before catalog classification and deduplication**. All configured `minimum_entries` floors passed.

## Checked but not added as a new trusted source

### Austrian Touhou Cup 2024

This was initially suspected to be missing, but it is already represented by osu!Collector tournament ID `1865` and forum topic `1907498`. No duplicate seed is added.

### Touhou Tournament (2019)

The osu! tournament forum index confirms the original 2019 `Touhou Tournament` existed, before the already-covered Touhou Tournament 2 and 3. During this audit no stable, complete public mappool source suitable for deterministic re-import was recovered. It is therefore documented as a known coverage gap rather than represented by an incomplete or guessed seed.

### Touhou Star Cup

Broad searches did not recover a sufficiently authoritative, stable and reproducible pool source that met this repository's source requirements. No canonical seed is added. A future contribution should include both an authoritative tournament description and a complete reproducible pool before promoting it.

## Google Sheets importer safety

The new Google Sheets importer deliberately uses only the Python standard library:

1. Download the public workbook through Google's XLSX export endpoint.
2. Read workbook relationships to resolve actual worksheet XML files.
3. Select only configured exact worksheet names and/or prefixes.
4. Extract osu! beatmapset IDs from inline cell/formula text, shared-string cells and external hyperlink relationship targets.
5. Deduplicate by numeric beatmapset ID while preserving first-seen order.
6. Fail closed when requested worksheets do not exist or the workbook is malformed.
7. Continue to enforce the repository-wide `minimum_entries` safety floor.

This is intentionally narrower than scraping rendered Google Sheets HTML and does not require a Google API key or a new dependency.

Trusted Google Sheet tournament entries may initially contain only a numeric beatmapset ID when the set was not already present in the catalog. `hydrate` therefore treats `tournament:google_sheet:` evidence as a partial-record source and resolves missing artist/title/source/status metadata through the public osu! beatmapset page while preserving the trusted tournament confidence.

## Discovery / alias expansion

The classifier already recognizes the English and Japanese titles of the Touhou games from the PC-98 era through the current mainline/spin-off set. The previous discovery config, however, searched only a small generic set such as `Touhou`, `東方`, Team Shanghai Alice and ZUN.

This audit adds `source=<game title>` searches for **every game-title alias already trusted by the classifier**, so exact osu! `source` metadata can be found even when neither `Touhou` nor `東方` appears elsewhere in the beatmap metadata.

A conservative circle-name sweep is also added for the circles already represented in the classifier's known-artist set (for example IOSYS, A-One, Alstroemeria Records, C-CLAYS, Diao ye zong, Halozy, ShibayanRecords and Syrufit). These broad artist/circle search hits still enter discovery as candidates and are not accepted merely because the circle name matched.

This PR does **not** add a free-form song-title alias corpus. Song-title aliases have substantially higher collision and maintenance risk; they should be introduced only with a maintained provenance dataset mapping aliases to original Touhou themes, rather than a hand-written list that silently turns fuzzy title matches into acceptance evidence.

## Verification checklist

Before opening the PR, the branch is checked in GitHub Actions with:

```sh
make check
make build
python -m touhou_osu audit-sources --json
```

The branch-only verification additionally imports the three new sources independently and compares them against the canonical catalog to expose confidence buckets, candidate promotions, and missing IDs. Two consecutive verification runs passed before PR creation; the second persisted the machine-readable source/intersection results as an Actions artifact for manual review.

## Trust boundary summary

| Source | Reproducible pool | Whole-pool Touhou guarantee | Import policy |
| --- | --- | --- | --- |
| Osu! Gensokyo Cup 2025 JP | yes, public Google Sheet | yes, official rules | verified |
| -Gensokyo Cup 2 | yes, public Google Sheet | yes, official rules | verified |
| 5 Digit Touhou Cup 1 qualifiers | yes, osu!Collector snapshot | no, tournament permits exceptions | candidate |
| Austrian Touhou Cup 2024 | already seeded | covered by existing evidence | no duplicate |
| Touhou Tournament 2019 | no stable complete pool recovered | historical event confirmed | documented gap |
| Touhou Star Cup | insufficient reproducible evidence recovered | unconfirmed | not added |
