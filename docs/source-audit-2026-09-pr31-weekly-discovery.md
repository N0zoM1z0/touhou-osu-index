# PR #31 weekly discovery review (2026-09)

This document records the manual review of the 2026-08-31 GitHub Actions weekly-discovery PR.

The original automation proposed 50 meaningful metadata changes, including 29 `candidate -> verified` promotions. Fresh osu! API and public beatmapset-page checks confirmed all 50 identities and metadata, but later provenance review found that the classifier was treating generic `Touhou` / `Touhou Project` / `東方` source strings as sufficient proof of composition provenance.

Under the stricter provenance standard established after the generic-source false-positive boundary was discovered, 19 generic-source promotions are not safe for automatic verification. They remain `candidate` and carry `manual:candidate` until independent composition provenance is reviewed:

- `16484`, `17154`, `17306`, `18382`, `18958`, `19491`, `19837`, `21202`, `23377`, `24448`
- `25174`, `25463`, `27152`, `27914`, `28441`, `29307`, `29904`, `32889`, `33888`

Ten proposed promotions are retained as `verified` because they have stronger independent evidence or meet the specific-game-source Class-A standard (concrete Touhou game source, multiple discovery-query hits, and current Touhou/ZUN mapper-tag signal):

- `16371`, `19679`, `21233`, `21863`, `25338`, `29044`, `31343`, `34030`, `34308`, `34459`

The remaining 21 of the 50 changes were already `verified`; only their current osu! metadata/evidence is refreshed.

Review results on the original PR head:

- semantic replay: exactly 50 meaningful changes, no additions/removals, no semantic conflicts with then-current main;
- live identity: 50/50 osu! API exact and 50/50 public-page canonical JSON exact;
- provenance: all 43 configured sources re-imported (6,977 records), 0 external request errors; 19 generic-source promotions withheld after manual review.

The generic-source automatic-verification rule is a generator-level issue and should be corrected separately so future weekly discovery PRs do not need this manual guard.
