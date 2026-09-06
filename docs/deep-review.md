# Catalog deep review

`audit-pr` compares the working catalog with a Git base without modifying either tree. It keeps fast deterministic checks separate from live network review.

## Local use

The default structural review reports added, modified, and removed IDs. Removals fail closed unless explicitly allowed.

```sh
make audit-pr BASE=main
```

Large addition-only audits can lock their expected boundary and compare the `## Accepted beatmapsets` table in a source-audit document with the exact added-ID set:

```sh
make audit-pr \
  BASE=main \
  AUDIT_DOC=docs/source-audit-example.md \
  EXPECTED_ADDITIONS=100 \
  FORBID_EXISTING_CHANGES=1
```

Optional live modes are selected with `MODE=provenance`, `MODE=live-osu`, or `MODE=all`. `SCOPE=changed` checks additions and modified rows; `SCOPE=added` limits network work to new rows. Live osu! review requires `OSU_CLIENT_ID` and `OSU_CLIENT_SECRET`.

## Review layers

- `structural` is local and deterministic. It validates both catalogs, compares their ID sets and fields, rejects unapproved removals, and optionally checks exact audit-document IDs and expected counts.
- `provenance` reuses the THBWiki and TouhouDB cross-checks for changed rows. Provider transport failures remain advisory, while actual red/ambiguous results and unsafe generic-source verification require review and fail this deep-review run.
- `live-osu` requires every selected catalog row to exactly match both osu! API v2 and the public beatmapset page for ID, artist, title, creator, source, status, modes, and osu! last-updated timestamp.
- `all` runs the layers in that order and skips expensive network checks when an earlier hard gate fails.

An evidence item matching `provenance:*-multi-original` is an explicit component-level claim. Such a row must be `mixed` and retain at least two original themes. Multiple themes without that explicit claim remain valid for arrangement lineages such as Night of Knights.

## GitHub Actions

The `Deep review` workflow automatically runs the structural layer on relevant pull requests. Its manual `workflow_dispatch` entry exposes all four modes plus base, target ref, scope, audit-document, and expected-addition controls.

The workflow is deliberately read-only. It never pushes a commit or updates a pull request, so its result does not depend on recursive workflow triggering. Manual deep review also requires the selected base to be an ancestor of the target ref; update stale review branches before spending network calls.

The live mode executes code from the selected repository ref with repository secrets. Only dispatch it for trusted branches in this repository; pull-request-triggered runs never select a live mode.
