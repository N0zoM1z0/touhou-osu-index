# Status-depth wave 2 verification — 2026-09-14

This record captures the completed verification and three-pass review for `docs/source-audit-2026-09-status-depth-wave2.md` and the corresponding addition-only catalog diff.

## Discovery and preselection

- base catalog: **5,044** beatmapsets
- final catalog: **5,294** beatmapsets
- concrete Touhou game-source queries: **66**
- status/query buckets: **198** across `graveyard`, `wip`, and `pending`
- official osu! search pages fetched: **302**
- unique absent verified hits outside the open PR #42 collision range: **4,287**
- diversified direct-refetch shortlist: **500**
- beatmapsets accepted after direct osu! API refetch: **380**
- direct-refetch failures/drift: **0**
- THBWiki/TouhouDB rows audited before final selection: **380**
- red/ambiguous provenance rows withheld before insertion: **2**
- final tracked additions: **250**
- initial external provenance verdicts: **155 supported / 95 unknown**
- provider transport/errors among the final 250: **0**

An `unknown` external-provenance result is not treated as positive evidence. Every initially accepted row independently had to retain a concrete recognized Touhou game source in current osu! metadata on a fresh direct beatmapset refetch; external contradictions or ambiguity were excluded.

## Review pass 1 — structural integrity

The first independent review re-checked the PR against current `main` and the still-open weekly PR #42.

Result: **passed**.

- semantic catalog diff: **+250 / ~0 / -0**
- audit-document IDs exactly equal the 250 additions
- no pre-existing catalog row changed
- no removal
- no changed-file overlap with #42's `0500000-0599999.json` / `0600000-0699999.json` shards
- temporary generation files are absent from the final PR diff

## Review pass 2 — source/composition provenance

The second independent review treated all **95** external-provenance `unknown` rows as the manual review population and prioritized non-obvious artists/titles, fan-game-looking source strings, covers/memes, and prior review-history rows.

Three sticky boundary corrections were required:

- `2606790` — `Everyone from the Red Cucumber thread — Kappa-sama no Iu Toori ~ One-way Accelerator`: `verified → excluded` with `manual:excluded`; `Subterranean Hatred` is an unofficial fan-made Phantasm-stage project and the row could not be treated as a ZUN/Touhou official composition chain.
- `2473015` — `Matsubame Frame — The Waltz of the Night`: `verified → candidate` with `manual:candidate`; current osu! identity is stable, but independent Touhou composition provenance could not be established.
- `2612960` — `7_7 — Bitch Gun`: `verified → candidate` with `manual:candidate`; exact-title/artist searches reproduced the track/map but did not establish a credible Touhou composition relation.

Post-review confidence among this PR's 250 new rows is therefore **247 verified / 2 candidate / 1 excluded**. The questionable rows remain tracked and sticky so an automated refresh cannot silently promote them again.

The corrected tree was then revalidated:

- `git diff --check`: passed
- `make check`: **96 tests passed**
- `make build`: **3,716 accepted beatmapsets built**
- final catalog validation: **5,294 total** (`3,687 verified`, `29 probable`, `1,575 candidate`, `3 excluded`)
- provenance re-check: **250 checked / 155 supported / 0 review flags / 0 provider errors**

## Review pass 3 — throttled live osu! identity

A first post-correction all-in-one live review encountered a burst of public-page failures after the first 150 rows while structural and provenance layers remained clean. Because the failure pattern was consistent with public-page rate limiting rather than simultaneous metadata drift, it was not accepted as a pass.

The live identity layer was rerun separately with conservative public-page throttling (`workers=2`, minimum public-page interval `2.0s`, rate-limit backoff `60s`).

Result: **passed**.

- live osu! identity: **250 checked / 0 failures / 0 errors**
- progress checkpoints: `50/250`, `100/250`, `150/250`, `200/250`, and `250/250` all reported zero failures
- required equality: stored catalog row = fresh osu! API v2 object = public beatmapset-page object
- structural review on the same corrected tree: **+250 / ~0 / -0**
- provenance review on the same corrected tree: **250 checked / 155 supported / 0 review flags / 0 provider errors**

The correction helper/workflow deleted itself before the permanent correction commit. The final PR diff contains only catalog shards and these permanent audit records.
