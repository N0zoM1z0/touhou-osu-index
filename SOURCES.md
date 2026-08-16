# Source inventory

The catalog is built from reproducible public sources declared in
[`config/seeds.json`](config/seeds.json). Run `make audit-sources` to query all
of them, verify their safety floors, and print their current record counts and
URLs. Use `python -m touhou_osu audit-sources --json` for automation.

The latest full audit on 2026-08-16 returned **6,596 source records** from
**30 sources**, representing **3,019 unique beatmapsets** before catalog
classification and deduplication. The August 2026 coverage expansion adds two
reproducible Google Sheet tournament pools and one candidate-first qualifier
collection; see [`docs/source-audit-2026-08.md`](docs/source-audit-2026-08.md)
for the evidence, catalog intersections, and exclusion decisions. Counts below
are upstream snapshots, not promises that every record is accepted into the
public index.

## Historical collections

| Collection | ID | Records | Initial trust |
| --- | ---: | ---: | --- |
| CardinalWolf 2hu 0–2.99 star (pt.1) | 1402 | 1,112 | candidate |
| CardinalWolf 2hu 3–4.49 star (pt.2) | 1405 | 1,240 | candidate |
| CardinalWolf 2hu 4.5 star plus (pt.3) | 1407 | 1,211 | candidate |
| 10S Touhou | 6907 | 1,015 | candidate |
| 4-Touhou Main | 14845 | 11 | probable/original |
| [5 Digit Touhou Cup 1 Qualifiers](https://osu.ppy.sh/community/forums/topics/1766738) | 12493 | 11 | candidate |

These snapshots are discovery evidence, not blanket verification. The importer
uses the osu!Collector API endpoint encoded by each collection ID. 5 Digit
Touhou Cup 1 is deliberately candidate-first because its official rules permit
non-Touhou substitutions and an `OTH` category even though the event is
primarily Touhou-themed.

## Official osu! packs

Whole-pack Touhou/theme packs use `official_pack:<tag>` and remain verified membership evidence. Mixed Featured Artist packs are different: they are imported only through an explicit, reviewed `verified_ids` allowlist and receive `official_pack_item:<tag>` evidence. The importer also checks the live raw pack size and fails closed if an audited ID disappears, so later upstream additions are never silently trusted.

| Pack | Canonical tag | Raw records | Audited verified records |
| --- | --- | ---: | ---: |
| [Touhou Chart](https://osu.ppy.sh/beatmaps/packs/R29) | R29 | 21 | whole pack |
| [Bad Apple!! Pack - Seductive Temptation](https://osu.ppy.sh/beatmaps/packs/T54) | T54 | 15 | whole pack |
| [Touhou Music Pack](https://osu.ppy.sh/beatmaps/packs/T65) | T65 | 20 | whole pack |
| [The Embodiment of Scarlet Devil Pack](https://osu.ppy.sh/beatmaps/packs/T96) | T96 | 15 | whole pack |
| [Touhou Pack](https://osu.ppy.sh/beatmaps/packs/T106) | T106 | 8 | whole pack |
| [Stan Touhou Music Pack](https://osu.ppy.sh/beatmaps/packs/FQ55) | FQ55 | 7 | whole pack |
| [UNDEAD CORPORATION Touhou pack](https://osu.ppy.sh/beatmaps/packs/FQ35) | FQ35 | 8 | whole pack |
| [Rin Pack](https://osu.ppy.sh/beatmaps/packs/A51) | A51 | 13 | 13 |
| [Demetori Pack](https://osu.ppy.sh/beatmaps/packs/A18) | A18 | 23 | 23 |
| [FELT Pack](https://osu.ppy.sh/beatmaps/packs/A33) | A33 | 11 | 9 |
| [Halozy Pack](https://osu.ppy.sh/beatmaps/packs/A32) | A32 | 11 | 10 |
| [Yuuhei Satellite Pack](https://osu.ppy.sh/beatmaps/packs/A16) | A16 | 34 | 34 |
| [Yuuhei Satellite & Catharsis Pack 2](https://osu.ppy.sh/beatmaps/packs/A85) | A85 | 22 | 15 |
| [Yuuhei Satellite & Catharsis Pack 3](https://osu.ppy.sh/beatmaps/packs/A86) | A86 | 22 | 16 |
| [Yuuhei Satellite & Catharsis Pack 4](https://osu.ppy.sh/beatmaps/packs/A87) | A87 | 22 | 20 |
| [Silver Forest Pack](https://osu.ppy.sh/beatmaps/packs/A23) | A23 | 30 | 30 |

The nine audited artist packs contain 188 memberships in total. Exactly 170 were individually verified as Touhou compositions; 18 original, Kantai Collection, or Seihou memberships are deliberately withheld. See [`docs/source-audit-2026-08-artist-packs-wave2.md`](docs/source-audit-2026-08-artist-packs-wave2.md) for the item-level decisions and provenance.

## Tournament pools

### osu!Collector tournament snapshots

| Tournament source | osu!Collector ID | Records | Policy |
| --- | ---: | ---: | --- |
| [Touhou Project Mania Cup 1st](https://osu.ppy.sh/community/forums/topics/1143215) | 466 | 84 | verified |
| [Touhou Project Mania Cup 2nd](https://osu.ppy.sh/community/forums/topics/1481811) | 467 | 68 | verified |
| [Touhou Project Mania Cup 3rd](https://osu.ppy.sh/community/forums/topics/1751979) | 748 | 69 | verified |
| [Touhou Project Mania Cup 4th](https://osu.ppy.sh/community/forums/topics/2015815) | 1661 | 103 | verified |
| [Touhou Tournament 2](https://osu.ppy.sh/community/forums/topics/1024816) | 1432 | 98 | verified |
| [Touhou Tournament 3](https://osu.ppy.sh/community/forums/topics/1740437) | 828 | 113 | verified |
| [Austrian Touhou Cup](https://osu.ppy.sh/community/forums/topics/1907498) | 1865 | 88 | verified |
| [5 Digit Touhou Cup 2](https://osu.ppy.sh/community/forums/topics/1976975) | 1793 | 102 | verified |
| [5 Digit Touhou Cup 3](https://osu.ppy.sh/community/forums/topics/2162098) | 2163 | 102 | verified |
| [Scarlet's Touhou Tournament](https://osu.ppy.sh/community/forums/topics/1323843) | 526 | 131 | candidate-first |
| [Scarlet's Touhou Tournament Season 2](https://osu.ppy.sh/community/forums/topics/1407029) | 829 | 140 | candidate-first |
| [Scarlet's Touhou Tournament 3rd Season](https://osu.ppy.sh/community/forums/topics/1759334) | 731 | 111 | candidate-first |

Touhou Project Mania Cup 1st–4th are also imported from their authoritative
osu! wiki pages (86, 72, 74, and 109 records respectively). The independent
wiki and osu!Collector paths preserve redundant provenance and make upstream
drift visible.

Scarlet's tournament description explicitly permits some non-Touhou maps, so
those three complete pools are intentionally imported as candidates. Entries
are promoted only when their own osu! metadata or other independent evidence
satisfies the classifier.

### Public Google Sheet tournament pools

Some older or smaller Touhou-only tournaments have authoritative public sheets
but no complete osu!Collector tournament snapshot. `google_sheet_tournaments`
exports those sheets as XLSX and reads only explicitly configured pool tabs.
The parser follows workbook relationships, shared strings, inline/formula text
and hyperlink relationship targets, then deduplicates numeric beatmapset IDs.
It does not scrape rendered Google HTML and requires no Google API key.

| Tournament source | Selected worksheets | Audited unique sets | Policy |
| --- | --- | ---: | --- |
| [Osu! Gensokyo Cup (2025 JP)](https://osu.ppy.sh/community/forums/topics/2089185) | exact `Mappools` | 40 | verified |
| [-Gensokyo Cup 2](https://osu.ppy.sh/community/forums/topics/1076292) | prefix `Mappool` | 148 | verified |

Both official forum posts explicitly describe their complete pools as Touhou
related/themed, so membership is trusted tournament evidence. Each source also
has a conservative `minimum_entries` floor to fail closed if the public sheet
is replaced, emptied, made private, or structurally changed.

The 2024 Austrian Touhou Cup was re-checked during this audit and is already
covered by osu!Collector tournament `1865`; it is not duplicated as a Google
Sheet source.

## Community queue and API discovery

The [`sd_touhou` BN queue](https://osu.ppy.sh/community/forums/topics/1881813)
is followed across every public forum page using the last post ID as the next
cursor. The 2026-08-16 audit found 194 unique beatmapsets. A queue link is kept
as a candidate until `make hydrate` or the monthly API reconciliation resolves
its artist/title metadata; unresolved and deleted links never enter the public
index.

Weekly osu! API discovery searches generic Touhou terms plus every English and
Japanese Touhou game-title alias already recognized by the deterministic
classifier. This closes a recall gap where a beatmap's `source` names only a
specific game (for example `Imperishable Night` or `東方永夜抄`) and contains no
generic `Touhou`/`東方Project` marker.

A conservative set of established Touhou circle names is also queried to find
maps whose metadata omits Touhou/game-title terms. Circle-name hits enter as
**candidates**; a circle match by itself is never verification. Discovery uses
cursor pagination and limits each automated PR to 50 meaningful catalog
changes. Search results remain candidates unless the classifier finds explicit
Touhou source metadata or sufficient independent signals.

A free-form song-title alias corpus is intentionally not added here. Song-title
aliases need a maintained theme-to-alias provenance dataset to avoid collisions
and false promotion; see the August 2026 source audit for the boundary.

## Reproduction and safety

```sh
make audit-sources
make import-seeds
make hydrate
make check
make build
```

- `audit-sources` performs a read-only live query and enforces every configured
  `minimum_entries` floor.
- `import-seeds` deduplicates by numeric beatmapset ID and unions provenance.
- `hydrate` resolves partial forum/tournament records from public beatmapset
  pages without OAuth. Its intentionally low concurrency avoids rate limits.
- `discover` and `reconcile` use osu! API v2 OAuth credentials; CI supplies
  those only through GitHub Actions secrets.
- No command downloads or stores `.osz`, audio, backgrounds, or other map
  assets.
