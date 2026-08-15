# Touhou osu! Index

[![CI](https://github.com/N0zoM1z0/touhou-osu-index/actions/workflows/validate.yml/badge.svg)](https://github.com/N0zoM1z0/touhou-osu-index/actions/workflows/validate.yml)
[![Pages](https://github.com/N0zoM1z0/touhou-osu-index/actions/workflows/pages.yml/badge.svg)](https://github.com/N0zoM1z0/touhou-osu-index/actions/workflows/pages.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-ff66aa.svg)](LICENSE)

An open, reproducible index of Touhou Project music mapped in osu!. It combines
historical collections, official beatmap packs, Touhou-only tournament pools,
and osu! API discovery into one deduplicated catalog keyed by **beatmapset ID**.

**[Browse the index](https://n0zom1z0.github.io/touhou-osu-index/)** ·
[Download JSON](https://n0zom1z0.github.io/touhou-osu-index/catalog.json) ·
[Download CSV](https://n0zom1z0.github.io/touhou-osu-index/catalog.csv)

## Why this exists

Large Touhou collections already exist, but they are snapshots. This project
makes their provenance explicit, layers in current official and tournament
curation, and leaves ambiguous discoveries reviewable instead of pretending
that every search hit is Touhou.

The repository stores IDs and metadata only. It never redistributes `.osz`
files, songs, backgrounds, or other copyrighted assets.

## Confidence model

| State | Meaning |
| --- | --- |
| `verified` | Recognized Touhou Project/game source, official Touhou pack, Touhou-only tournament, or manual verification. |
| `probable` | Multiple independent signals agree, such as Touhou tags plus known Touhou metadata. |
| `candidate` | Historical collection membership or one weaker signal; needs review. |
| `excluded` | Manually confirmed false positive, retained to prevent rediscovery. |

The public site shows verified and probable sets by default. Candidates remain
available as a review queue; excluded sets are present only in the complete
machine-readable source catalog.

## Data

`data/catalog.json` is the canonical source. Each record looks like:

```json
{
  "beatmapset_id": 1151630,
  "artist": "Rin",
  "title": "Muenzuka set 09 ~ Hana wa Gensou no Mama ni",
  "creator": "eiri-",
  "source": "東方花映塚 ～ Phantasmagoria of Flower View.",
  "status": "ranked",
  "modes": ["taiko"],
  "touhou_kind": "arrangement",
  "origin_games": [],
  "original_themes": [],
  "evidence": ["official_pack:FQ55", "osu_source"],
  "confidence": "verified",
  "last_checked": "2026-08-15",
  "osu_last_updated": "2020-10-10T22:31:37Z"
}
```

Generated artifacts are written to `dist/`:

- `catalog.json` — accepted (`verified` + `probable`) records for consumers.
- `catalog.csv` — spreadsheet-friendly accepted records.
- `review.json` — candidates and explicit exclusions.
- `index.html` — searchable, filterable static site.

Volatile values such as star rating, play count, and difficulty names are not
maintained by hand. Consumers should refresh those through the osu! API when
needed.

## Reproducible pipeline

Requires Python 3.11+ and otherwise uses only the standard library.

```sh
make check          # schema validation and tests
make build          # generate site, JSON, and CSV
python -m touhou_osu import-seeds --write
```

Seed import currently understands:

- osu!Collector collections (including CardinalWolf's three `2hu` snapshots,
  10S's collection, and `4-Touhou Main`);
- official osu! Touhou beatmap packs;
- osu!Collector Touhou tournament pools;
- osu! wiki tournament pages, including Touhou Project Mania Cup 1st–4th.

The importer deduplicates everything by beatmapset ID and unions its evidence.
Source definitions live in [`config/seeds.json`](config/seeds.json).

## Automated discovery

The discovery job uses osu! API v2's Client Credentials Grant with the `public`
scope. Set these environment variables locally:

```sh
export OSU_CLIENT_ID=12345
export OSU_CLIENT_SECRET='your-secret'
python -m touhou_osu discover --write
```

On GitHub, add the same values as Actions secrets named `OSU_CLIENT_ID` and
`OSU_CLIENT_SECRET`. The weekly workflow searches the configured Touhou aliases
with cursor pagination and opens a review PR when the catalog changes. The
monthly workflow reconciles osu! metadata and statuses. Neither workflow merges
its own PR.

See [CONTRIBUTING.md](CONTRIBUTING.md) for manual review and correction rules.

## Sources and attribution

This project is independent and is not affiliated with osu!, Team Shanghai
Alice, or osu!Collector. osu! API usage follows the
[official API documentation](https://osu.ppy.sh/docs/). Source links and the
date each record was checked are retained for reproducibility.
