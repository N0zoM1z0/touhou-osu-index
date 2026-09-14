# Status-depth wave 2 verification — 2026-09-14

This record captures the completed verification run for `docs/source-audit-2026-09-status-depth-wave2.md` and the corresponding addition-only catalog diff.

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
- red/ambiguous provenance rows withheld: **2**
- final additions: **250**
- final provenance verdicts before insertion: **155 supported / 95 unknown**
- provider transport/errors among the final 250: **0**

An `unknown` external-provenance result is not treated as positive evidence. Every accepted row independently had to retain a concrete recognized Touhou game source in current osu! metadata on a fresh direct beatmapset refetch; external contradictions or ambiguity were excluded.

## Repository validation

The generated tree passed:

- `git diff --check`
- `make check`: **96 tests passed**
- `make build`: **3,719 accepted beatmapsets built**
- catalog validation before manual pass-2 corrections: **5,294 total** (`3,690 verified`, `29 probable`, `1,573 candidate`, `2 excluded`)

## Deep Review

Deep Review ran with `mode=all`, `scope=added`, `EXPECTED_ADDITIONS=250`, `FORBID_EXISTING_CHANGES=1`, and `REQUIRE_BASE_ANCESTOR=1` against `origin/main`.

Result: **passed**.

- semantic catalog diff: **+250 / ~0 / -0**
- provenance re-check: **250 checked / 155 supported / 0 review flags / 0 provider errors**
- live osu! identity re-check: **250 checked / 0 failures**
- live identity requirement: stored catalog row = fresh osu! API v2 object = public beatmapset-page object

The temporary generation workflow and helper script were deleted before the final data commit; they are not part of the pull-request diff.


## Manual source review correction run

The independent source-focused pass found one fan-game original false positive and two rows without enough corroboration for sticky verification. The catalog was corrected to `247 verified / 2 candidate / 1 excluded` among this PR's 250 new rows, using `manual:excluded` / `manual:candidate` so automated refreshes cannot undo the reviewed boundary. The corrected tree was then subjected to the same full validation and Deep Review contract again.
