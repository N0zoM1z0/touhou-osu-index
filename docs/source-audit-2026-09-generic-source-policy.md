# Generic-source classifier correction (2026-09)

This change follows the manual review of weekly discovery PR #31, which demonstrated that exact generic osu! `source` labels such as `Touhou` / `Touhou Project` / `東方Project` are useful discovery signals but are not sufficient composition provenance.

Policy after this change:

- a recognized concrete Touhou game title in osu! `source` remains an automatic `verified` signal;
- an exact generic Touhou label may still contribute the existing `osu_source` evidence marker for compatibility, but no longer automatically verifies the row;
- generic source plus mapper Touhou tags, a known Touhou artist, and curated collection evidence may reach `probable`;
- manual exclusions/candidate guards and audited official/tournament evidence keep their existing precedence;
- existing verified catalog rows are not mass-demoted by catalog merging, but newly discovered generic-source rows can no longer be promoted solely by the generic source field;
- the evidence vocabulary is intentionally not split into new generic/game markers, avoiding a one-time catalog backfill that would consume the weekly meaningful-change cap.

External composition databases are added as an advisory review layer. TouhouDB and THBWiki are queried with strict title/artist matching where possible. Their results are recorded as positive relations, red flags, ambiguity, or provider errors; no single external database automatically changes catalog confidence.

Weekly discovery now snapshots its base catalog, audits changed rows, uploads a JSON provenance artifact, and hard-fails only if a newly verified generic-source row appears without independent trusted evidence. External provider outages remain non-gating warnings.
