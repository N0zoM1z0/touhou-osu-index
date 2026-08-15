# Source inventory

The catalog is built from reproducible public sources declared in
[`config/seeds.json`](config/seeds.json). Run `make audit-sources` to query all
of them, verify their safety floors, and print their current record counts and
URLs. Use `python -m touhou_osu audit-sources --json` for automation.

The latest full audit on 2026-08-15 returned **6,397 source records** from
**27 sources**, representing **2,992 unique beatmapsets** before catalog
classification and deduplication. Counts below are upstream snapshots, not
promises that every record is accepted into the public index.

## Historical collections

| Collection | ID | Records | Initial trust |
| --- | ---: | ---: | --- |
| CardinalWolf 2hu 0–2.99 star (pt.1) | 1402 | 1,112 | candidate |
| CardinalWolf 2hu 3–4.49 star (pt.2) | 1405 | 1,240 | candidate |
| CardinalWolf 2hu 4.5 star plus (pt.3) | 1407 | 1,211 | candidate |
| 10S Touhou | 6907 | 1,015 | candidate |
| 4-Touhou Main | 14845 | 11 | probable/original |

These large snapshots are discovery evidence, not blanket verification. The
importer uses the osu!Collector API endpoint encoded by each collection ID.

## Official osu! packs

| Pack | Canonical tag | Records |
| --- | --- | ---: |
| [Touhou Chart](https://osu.ppy.sh/beatmaps/packs/R29) | R29 | 21 |
| [Touhou Music Pack](https://osu.ppy.sh/beatmaps/packs/T65) | T65 | 20 |
| [Touhou Pack](https://osu.ppy.sh/beatmaps/packs/T106) | T106 | 8 |
| [Stan Touhou Music Pack](https://osu.ppy.sh/beatmaps/packs/FQ55) | FQ55 | 7 |
| [UNDEAD CORPORATION Touhou pack](https://osu.ppy.sh/beatmaps/packs/FQ35) | FQ35 | 8 |

Official pack membership is verified evidence. `R29` is the current canonical
tag for the historical Touhou Chart pack.

## Tournament pools

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

## Community queue and API discovery

The [`sd_touhou` BN queue](https://osu.ppy.sh/community/forums/topics/1881813)
is followed across every public forum page using the last post ID as the next
cursor. The 2026-08-15 audit found 194 unique beatmapsets. A queue link is kept
as a candidate until `make hydrate` or the monthly API reconciliation resolves
its artist/title metadata; unresolved and deleted links never enter the public
index.

Weekly osu! API discovery searches the configured source aliases, Japanese and
English Touhou terms, Team Shanghai Alice, ZUN, and related metadata. It uses
cursor pagination and limits each automated PR to 50 meaningful catalog
changes. Search results remain candidates unless the classifier finds explicit
Touhou source metadata or sufficient independent signals.

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
