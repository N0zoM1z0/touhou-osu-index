# External composition provenance

osu! `source` metadata is mapper-entered. A concrete Touhou game title is a strong automatic signal, but generic labels such as `Touhou`, `Touhou Project`, `東方`, or `東方Project` do not identify the underlying composition and are not sufficient for automatic `verified` confidence.

The repository therefore treats external music databases as **advisory cross-checks**, not authorities.

## Providers

### Touhou Music Database (TouhouDB)

The audit queries the public songs API with the osu! title, then requires an exact normalized title and compatible artist match before considering a row.

Useful signals:

- `originalVersionId` present: positive arrangement relation;
- `songType=Original` with ZUN as the matched artist: positive ZUN-original relation;
- `songType=Original` with a non-ZUN matched artist and no underlying original: review red flag.

A TouhouDB hit alone never promotes or excludes a catalog entry.

### THBWiki music data API

The audit uses the public `album.php` track-search (`st`) and track-detail (`gt`) endpoints. It first requires an exact normalized track title. The detail request retrieves `circle`, `artist`, `arrange`, `ogmusic`, and `ogwork`.

A THBWiki row is reported as a positive composition relation only when:

- `ogmusic` names one or more underlying originals; and
- the osu! artist is compatible with at least one THBWiki identity from `circle`, `artist`, or `arrange`.

This matters because osu! often stores the circle as the artist while THBWiki stores an individual arranger separately. For example, matching only `arrange` would miss tracks where the osu! artist is a circle name. Rows with an exact title but no usable identity metadata are not claimed as positive evidence. `ogwork` is included in the report as extra review context when available.

THBWiki results are advisory and never auto-promote a row.

## Weekly discovery policy

Weekly discovery runs the external audit only for rows actually changed by that run. The workflow:

1. snapshots the pre-discovery catalog;
2. runs normal osu! API discovery;
3. audits the changed rows against TouhouDB and THBWiki;
4. uploads the JSON report as `weekly-provenance-report`;
5. writes positive relations, red flags, ambiguity, and provider errors to the Actions job summary.

Provider outages or ambiguous database coverage are warnings rather than hard failures. The hard policy gate is deterministic and local: a **newly verified generic-source row without independent trusted evidence** (`manual:verified`, audited official pack, trusted tournament, or TMC evidence) fails the workflow.

This distinction is deliberate: a transient external outage must not break discovery, while a regression that again treats generic `Touhou` metadata as sufficient proof must fail closed.

## Manual use

Compare a modified catalog with a base snapshot:

```bash
python -m touhou_osu.provenance \
  --catalog data/catalog \
  --base-catalog /path/to/base/data/catalog \
  --scope changed \
  --output provenance.json \
  --fail-on-policy-violation
```

Audit generic-source rows without changing the catalog:

```bash
python -m touhou_osu.provenance --scope generic --limit 50
```

The report fields `supported`, `red_flag`, and `ambiguous` are review hints only. Acceptance should continue to use the repository's stronger provenance hierarchy and manual review for generic-source composition boundaries.
