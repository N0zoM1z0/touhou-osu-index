# Systematic theme audit workflow

This workflow is for composition-centered completeness passes such as `Night of Knights`, `竹取飛翔 ～ Lunatic Princess`, or `ボーダーオブライフ`. It complements source ingestion: source imports answer “what does this curated source contain?”, while a theme audit asks “which osu! beatmapsets use this specific composition or a documented derivative of it?”.

## 1. Lock the composition boundary first

Write down the canonical original title, source game, and any collision-prone aliases before searching osu!. Do not let an English display title silently broaden the target. If two Touhou originals share words in translated titles, treat them as separate composition keys.

For derivative targets, document the parent chain as well. A remix of a famous arrangement is not automatically equivalent to every arrangement of the same ZUN original.

## 2. Build an evidence-backed search corpus

Prefer composition-level sources that expose title, artist/circle, and original-song metadata. Useful sources include official artist/circle pages, release tracklists, official game/song pages, Touhou Arrangement Chronicle, and well-maintained Touhou discography wikis.

Record search tuples rather than bare keywords whenever a title is generic:

```text
(title, artist-or-circle guard, documented original composition)
```

Direct Japanese titles and distinctive aliases may be searched without an artist guard. Generic English titles should normally require one.

## 3. Search broadly; accept narrowly

Search results are candidates, not verification. Use controlled aliases, punctuation variants, and status buckets when default ranking can hide older graveyard material. De-duplicate by numeric beatmapset ID before review.

For every retained candidate:

1. compare the numeric ID against the current catalog;
2. direct-refetch the current public osu! beatmapset page or API object;
3. require the fetched ID, artist, and title to match the reviewed candidate;
4. verify the composition through current osu! source metadata or an independent composition-level source;
5. keep unresolved/deleted identities out of automatic promotion.

Do not infer a beatmapset ID from a tournament label, screenshot, mapper name, or title alone.

## 4. Classify structured provenance

Use `touhou_kind` to describe the recording represented by the beatmapset:

- `original`: the ZUN/original-game recording of the target composition;
- `arrangement`: a recording derived from one or more Touhou originals with no supported non-Touhou ingredient;
- `mixed`: a mashup/medley/recording with multiple supported originals where representing only one would be misleading;
- `unknown`: keep this only when the composition relationship itself is not sufficiently established.

Fill `origin_games` and `original_themes` with every supported Touhou source used by the recording. Do not guess extra themes from character association, album concept, mapper tags, or similar-title collisions.

Use `manual:verified` only when the catalog judgment depends on reviewed composition evidence that an automated refresh cannot reconstruct from current osu! metadata. Existing sticky manual boundaries must not be overwritten casually.

## 5. Preserve the negative boundary

A useful audit records why plausible hits were not accepted. Keep explicit sections for:

- same-title but different-composition collisions;
- independent arrangements of a nearby theme;
- unresolved/deleted beatmapset identities;
- weak mapper-tag or search-token matches;
- mixed works whose target ingredient is plausible but not independently sourced.

This prevents future searches from re-litigating the same false positives and keeps “coverage” from drifting into keyword matching.

## 6. Write through the canonical catalog API

`data/catalog/` is the canonical store. Let `Catalog.save()` choose and rewrite shards rather than hand-maintaining range boundaries. The save path guarantees numeric ordering and recursively partitions populated 100,000-ID base ranges so every shard remains at or below the repository record limit.

A theme audit should make the smallest semantic change possible: add genuinely absent beatmapsets, enrich already-known target rows, and leave unrelated records untouched.

## 7. Validate before review

Run the repository checks after the final write:

```sh
make check
make build
git diff --check
```

Inspect the resulting diff as an audit artifact. Confirm that:

- only expected shards changed;
- newly added IDs are in the correct ranges and sorted;
- existing rows changed only in intended metadata/provenance fields;
- catalog cardinality increased by exactly the expected number of new IDs;
- no generated aggregate was accidentally committed under `data/`;
- the audit document names accepted, excluded, and unresolved boundaries.

For large passes, include counts and accepted-ID groups in the audit document so another contributor can reproduce the decision boundary without re-running the entire discovery process.
