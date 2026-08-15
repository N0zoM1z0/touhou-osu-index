# Contributing

The most valuable contribution is resolving ambiguity without discarding
provenance. Please keep changes small and evidence-backed.

## Review a candidate

1. Open the beatmapset on osu! and identify the underlying composition.
2. Prefer primary metadata: the artist/circle's official page, album scans, or
   an official upload. Touhou wikis are useful secondary references.
3. Set `confidence` to `verified`, `probable`, or `excluded`.
4. Add `manual:verified` or `manual:excluded` to `evidence` when making a
   definitive judgment.
5. Fill `touhou_kind`, `origin_games`, and `original_themes` only when supported
   by evidence. Do not guess from a character background.
6. Run `make check` and `make build`.

Manual evidence is sticky: automated refreshes update osu! metadata but do not
override a manual inclusion or exclusion.

## Classification rules

- An exact Touhou Project alias or a recognized official Touhou game title in
  the source is verified.
- Longer unrecognized source names containing `Touhou` or `東方` stay
  candidates until reviewed. These words also occur in unrelated works, and
  fan album/game names need provenance before publication.
- Membership in an official Touhou pack or a Touhou-only tournament is
  verified.
- A Touhou mapper tag plus matching known artist/game/theme metadata is
  probable.
- A known Touhou circle alone is only a candidate because circles also release
  original and non-Touhou music.
- Historical collection membership is evidence for discovery, not automatic
  proof.
- Medleys and mixed-source sets require manual review.

## Catalog editing

`data/catalog.json` must remain sorted by numeric `beatmapset_id`. Evidence,
modes, origin games, and themes must be unique and sorted. Dates use ISO 8601.
Do not add volatile star ratings, local file paths, download mirrors, or asset
URLs.

Run:

```sh
make check
```

The validator rejects duplicate IDs, unknown enum values, malformed dates,
missing evidence, and unsorted data.

## Adding a discovery source

Add declarative entries to `config/seeds.json` when the source is supported.
New source types need a parser plus fixture-based tests. A seed must have a
stable canonical URL and a clear curation rationale.

Network calls do not run in the unit test suite. Save a minimal, anonymized
fixture that exercises the response shape instead of recording credentials or
large upstream payloads.

## Copyright and privacy

Never commit `.osz`, `.osu`, audio, video, backgrounds, replay files, osu! OAuth
secrets, or private user data. Beatmapset IDs and public metadata are sufficient
for this index.
