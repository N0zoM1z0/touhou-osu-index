# Contributing

The most valuable contribution is resolving ambiguity without discarding
provenance. Please keep changes small and evidence-backed.

## Review a candidate

1. Open the beatmapset on osu! and identify the underlying composition.
2. Prefer primary metadata: the artist/circle's official page, album scans, or
   an official upload. Touhou wikis are useful secondary references.
3. Set `confidence` to `verified`, `probable`, or `excluded`.
4. Add `manual:verified`, `manual:excluded`, or `manual:candidate` to
   `evidence` when making a sticky reviewed judgment.
5. Fill `touhou_kind`, `origin_games`, and `original_themes` only when supported
   by evidence. Do not guess from a character background.
6. Run `make check` and `make build`.

Manual evidence is sticky: automated refreshes update osu! metadata but do not
override `manual:verified`, `manual:excluded`, or a reviewed `manual:candidate`
boundary. Use `manual:candidate` when an item is relevant enough to retain for
review but repository scope intentionally prevents automatic acceptance (for
example a ZUN-composed Seihou track).

## Classification rules

- An exact Touhou Project alias or a recognized official Touhou game title in
  the source is verified.
- Longer unrecognized source names containing `Touhou` or `東方` stay
  candidates until reviewed. These words also occur in unrelated works, and
  fan album/game names need provenance before publication.
- Membership in an official Touhou pack or a Touhou-only tournament is
  verified.
- A Touhou mapper tag plus a known Touhou artist and independent historical
  Touhou collection membership is probable.
- A link from a curated Touhou-only queue becomes probable after its public
  osu! artist/title metadata resolves. Deleted or unresolved links stay
  candidates.
- A known Touhou circle alone is only a candidate because circles also release
  original and non-Touhou music.
- Historical collection membership is evidence for discovery, not automatic
  proof.
- Medleys, mashups, and mixed-source sets are in scope and follow the same
  evidence rules as other sets. The presence of non-Touhou material alone is
  not a reason to hold or exclude a set.

## Catalog editing

`data/catalog/` contains the canonical catalog. Start by rounding a numeric
`beatmapset_id` down to the nearest 100,000; ID `1151630`, for example, belongs
in the `1100000-1199999` base range. A populated base range may be recursively
split into smaller filename ranges to keep every file at 500 records or fewer;
choose the child range containing the ID. Records inside each shard must be
sorted by numeric ID. Evidence, modes, origin games, and themes must be unique
and sorted. Dates use ISO 8601. Do not add volatile star ratings, local file
paths, download mirrors, or asset URLs.

Run:

```sh
make check
```

The validator rejects misplaced or duplicate IDs across shards, oversized
shards, unknown enum values, malformed dates, missing evidence, and unsorted
data. Run `make assemble` when you need a single complete JSON file; generated
aggregates belong in `dist/`, not in the canonical `data/` directory.

## Adding a discovery source

Add declarative entries to `config/seeds.json` when the source is supported.
New source types need a parser plus fixture-based tests. A seed must have a
stable canonical URL, a clear curation rationale, and a conservative
`minimum_entries` floor. Mark a mixed or partially themed tournament
`"trusted": false`; its pool starts as candidates and only independently
verified Touhou entries enter the public index.

Use the reusable source commands before committing:

```sh
make audit-sources  # live URLs, record counts, and unique beatmapsets
make import-seeds   # merge configured sources
make hydrate        # fill incomplete records through public osu! pages
make check
make build
```

`python -m touhou_osu audit-sources --json` provides machine-readable output.
The audit and hydration commands do not require osu! OAuth credentials.

Network calls do not run in the unit test suite. Save a minimal, anonymized
fixture that exercises the response shape instead of recording credentials or
large upstream payloads.

## Copyright and privacy

Never commit `.osz`, `.osu`, audio, video, backgrounds, replay files, osu! OAuth
secrets, or private user data. Beatmapset IDs and public metadata are sufficient
for this index.
