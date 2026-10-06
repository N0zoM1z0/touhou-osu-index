# Legacy generic-source confidence audit — 2026-10

## Scope

This pass removes a historical confidence grandfathering rule after the monthly
reconciliation hardening in PR #44.

Baseline: `main@88b8a7e9645d2343f73a57fc7d82755e7514608b`.

A row is in scope when all of the following are true:

1. `confidence` is `verified`;
2. the current osu! source is only an exact generic Touhou alias
   (`Touhou`, `Touhou Project`, `東方`, `東方Project`, or
   `東方プロジェクト`);
3. the row has no independent reviewed verification evidence.

Independent reviewed verification means at least one of:

- `manual:verified`;
- an `audit:` or `provenance:` review marker;
- `official_pack:` or `official_pack_item:`;
- a trusted `tournament:` or `tmc:` source.

Candidate-first tournament evidence (`tournament_candidate:`), historical
osu!Collector membership, mapper tags, circle-name matches, discovery queries,
and the generic osu! source itself are not sufficient for `verified`.

## Result

The baseline contained **217** legacy generic-source verified rows without
independent reviewed verification.

- **12** retain enough independent weak signals to become `probable`.
- **205** return to `candidate`.
- **0** rows with manual/audit/provenance, official-pack, or trusted-tournament
  verification are demoted.

Every migrated row receives
`review:legacy-generic-confidence-2026-10` so the confidence change remains
auditable without making the decision sticky.

The `probable` subset is limited to rows whose stored evidence already
represents the current multi-signal rule: known Touhou metadata derived from a
mapper Touhou tag + known Touhou artist + historical collection membership.
All other generic-only verified rows become candidates pending stronger
composition provenance.

## Representative boundaries

- `344295` — `Unknown`, blank title, generic `東方Project` source and
  historical collection evidence only: `verified -> candidate`.
- `3589` — IOSYS / `Hakurei Jinja`, generic source but existing
  multi-signal Touhou metadata evidence: `verified -> probable`.
- Rows with a recognized concrete game source remain verified under the normal
  classifier.
- Rows reviewed by prior systematic audits (for example the Night of Knights
  audit) are outside this migration even when their osu! source is generic.

Metadata completeness is not the primary boundary here. For example, a row
with a blank artist but a concrete recognized game source or explicit reviewed
audit can remain verified; this pass is specifically about unsupported generic
source verification.

## Guardrail

Provenance-mode deep review now checks **the full current catalog**, not only
newly verified rows, for generic-source `verified` entries lacking independent
reviewed evidence. In addition, the repository unit suite loads the canonical
catalog and asserts this debt set stays empty on every `make check`.

The provenance policy also treats `audit:` and `provenance:` markers as
independent reviewed verification alongside manual verification, official packs
and trusted tournament sources.

## Review checklist

Before merge:

- run the full unit test suite and catalog validation;
- build the accepted/review exports;
- run PR deep review and confirm zero generic verification policy violations;
- verify the catalog diff contains confidence/evidence changes only for the
  intended 217 rows;
- do not merge as part of this audit preparation.
