# Coverage audit: 200+ absent explicit-source Touhou beatmapsets (2026-09)

## Scope

This pass searches every configured osu! API discovery query against the current canonical catalog, but only inserts beatmapsets that were absent from `main` and that independently satisfy the repository's existing automatic `verified` rule through current explicit osu! `source` metadata.

No `manual:verified` override, artist-only inference, mapper-tag-only inference, tournament blanket trust, or collection-only promotion is used in this batch.

## Search breadth

- configured discovery queries: **89**
- cursor pages requested per query: up to **8**
- unique beatmapsets seen across all queries: **5272**
- unique search hits absent from the base catalog: **2887**
- absent hits already classifiable as explicit-source `verified`: **466**
- base catalog cardinality: **3993**

## Verification pipeline

Every retained beatmapset passed all of these checks:

1. numeric `beatmapset_id` is absent from the base catalog;
2. rediscovered through one or more configured osu! API queries, retaining the exact `discovery_query:*` evidence;
3. search-result metadata classifies as `verified` because current osu! `source` is an exact accepted Touhou alias or a recognized official Touhou game source;
4. direct `/api/v2/beatmapsets/{id}` refetch returns the same ID / artist / title / creator / source / status and still classifies as explicit-source `verified`;
5. the public `https://osu.ppy.sh/beatmapsets/{id}` page is fetched separately and its embedded canonical beatmapset JSON matches the direct API identity/source/status and still classifies as explicit-source `verified`;
6. the final write adds only new IDs and uses `Catalog.save()` for deterministic shard placement and sorting.

Direct API refetch: **466 accepted / 0 rejected** from the search-verified absent pool.

Public-page refetch of the diversified preselection: **265 accepted / 55 rejected**.

## Accepted result

- new beatmapsets added: **239**
- final catalog cardinality: **4232**
- source specificity: **212 recognized game-source rows**, **27 exact generic Touhou-source rows**
- status distribution: ranked=239
- mode presence: catch=21, mania=34, osu=136, taiko=52
- discovery corroboration: 2 queries=29, 3 queries=100, 4 queries=81, 5 queries=27, 6 queries=1, 7 queries=1

Selection is round-robin across normalized source strings, with recognized game sources and current ranked/loved material preferred before generic `Touhou` source rows. This avoids simply taking the first IDs returned by a broad keyword search.

### Source distribution

- `東方風神録　～ Mountain of Faith.` — 32
- `東方妖々夢　～ Perfect Cherry Blossom.` — 31
- `東方紅魔郷　～ the Embodiment of Scarlet Devil.` — 30
- `東方地霊殿　～ Subterranean Animism.` — 29
- `東方永夜抄　～ Imperishable Night.` — 29
- `東方花映塚　～ Phantasmagoria of Flower View.` — 28
- `東方Project` — 27
- `東方星蓮船　～ Undefined Fantastic Object.` — 16
- `東方神霊廟　～ Ten Desires.` — 16
- `東方錦上京 〜 Fossilized Wonders.` — 1

### Accepted beatmapset IDs

- `2280680`, `1849213`, `1919687`, `2156450`, `2185163`, `2205023`, `2120472`, `2253507`, `2454428`, `1446247`, `2328066`, `1989147`, `1945081`, `2064233`, `1927811`, `2055714`, `2257913`, `2267663`, `1873233`, `1284535`
- `2025551`, `2301090`, `2086046`, `2011565`, `2173216`, `2303547`, `2271678`, `2198377`, `1348852`, `2102240`, `2308571`, `2266581`, `2020128`, `2235405`, `2320547`, `2412257`, `2273085`, `1461736`, `2114955`, `1960735`
- `2480698`, `2128889`, `2288990`, `2013277`, `2463988`, `2397704`, `1499636`, `2120349`, `2049284`, `2524315`, `2240721`, `2324476`, `2013928`, `2474975`, `1382136`, `1878367`, `2138161`, `2132719`, `2389626`, `1927927`
- `2025539`, `2258024`, `2272466`, `1889476`, `2397276`, `2275606`, `2051546`, `2011555`, `2066498`, `1961523`, `2444840`, `2084799`, `2047786`, `2115856`, `2306433`, `2462140`, `1976303`, `2074627`, `2477983`, `2528001`
- `2321881`, `2063410`, `2193011`, `2434263`, `2023965`, `2119924`, `1241563`, `2533832`, `2473158`, `2550161`, `2111234`, `2124429`, `1267528`, `1936480`, `2346142`, `2129313`, `2299734`, `2483592`, `2557046`, `2182821`
- `2136127`, `1360248`, `2429034`, `2148164`, `2202176`, `2236173`, `2151953`, `1992653`, `2476206`, `2217940`, `2320727`, `2177908`, `2239880`, `2237545`, `2190658`, `1437794`, `2512437`, `2350118`, `2389297`, `2254017`
- `2302143`, `2292081`, `2211447`, `1556887`, `2076628`, `2459983`, `2274433`, `2351192`, `2453058`, `2254112`, `1565933`, `2095104`, `1849967`, `2474510`, `2499259`, `2466317`, `2490353`, `2259588`, `2128728`, `1856797`
- `2557613`, `2521633`, `2307224`, `2489023`, `177908`, `1648038`, `2148241`, `1862313`, `1915805`, `2553532`, `328117`, `2281545`, `1762719`, `2167421`, `1914040`, `1941687`, `2052920`, `2304999`, `1772154`, `2171520`
- `1949019`, `1999204`, `2072347`, `2314842`, `1894970`, `2176171`, `2024106`, `2051619`, `2098448`, `2011128`, `2364061`, `1909974`, `2180270`, `2039585`, `2107618`, `2024061`, `2372053`, `1915183`, `2195327`, `2057639`
- `2529930`, `2186687`, `2087883`, `2419751`, `1927992`, `2210397`, `2066221`, `2535184`, `2293757`, `2089093`, `2445629`, `1962897`, `2271602`, `2080874`, `2549679`, `2306814`, `2524382`, `1964631`, `2313285`, `2153229`
- `2550684`, `2376812`, `2097924`, `2524683`, `1999580`, `2318139`, `2205623`, `2586507`, `2455952`, `2101141`, `2536961`, `2023974`, `2323094`, `2469450`, `2037983`, `2337322`, `2365832`, `2069637`, `2531939`, `2132288`
- `625519`, `2046139`, `2478777`, `2433072`, `2186014`, `2532082`, `2184864`, `1151507`, `2498268`, `2471841`, `2190615`, `2550836`, `1205704`, `2559362`, `2586381`, `2250094`, `2556827`, `1275058`, `2106026`

## Negative / failure boundary

### Post-review composition exclusion

- `2096026` — **Knife - Story** — removed during the 2026-09-03 merge review. Although current osu! metadata says `source = 東方Project`, independent release/live documentation identifies `Story` as a **秘封倶楽部 image original song**, explicitly distinguishing it from an arrangement. That is outside this repository's composition-centered Touhou arrangement/original boundary, so generic osu! source metadata is not sufficient to publish it. Evidence: https://touhougarakuta.com/article/20_neopop_live_report01/ and https://www.suruga-ya.jp/product/detail/186144253 .

Search hits that were absent but did not classify as explicit-source `verified` were not inserted. Search-stage rejection summary: `{'confidence:candidate': 2421}`.

Direct API failures/mismatches (first 40, if any):

- none

Public-page failures/mismatches (first 40, if any):

- `1368759` — fetch:HTTP 429 from https://osu.ppy.sh/beatmapsets/1368759
- `1550437` — fetch:HTTP 429 from https://osu.ppy.sh/beatmapsets/1550437
- `1588466` — fetch:HTTP 429 from https://osu.ppy.sh/beatmapsets/1588466
- `1635625` — fetch:HTTP 429 from https://osu.ppy.sh/beatmapsets/1635625
- `1771472` — fetch:HTTP 429 from https://osu.ppy.sh/beatmapsets/1771472
- `1840481` — fetch:HTTP 429 from https://osu.ppy.sh/beatmapsets/1840481
- `1892797` — fetch:HTTP 429 from https://osu.ppy.sh/beatmapsets/1892797
- `1909936` — fetch:HTTP 429 from https://osu.ppy.sh/beatmapsets/1909936
- `1913796` — fetch:HTTP 429 from https://osu.ppy.sh/beatmapsets/1913796
- `1921061` — fetch:HTTP 429 from https://osu.ppy.sh/beatmapsets/1921061
- `1928250` — fetch:HTTP 429 from https://osu.ppy.sh/beatmapsets/1928250
- `1941763` — fetch:HTTP 429 from https://osu.ppy.sh/beatmapsets/1941763
- `1990973` — fetch:HTTP 429 from https://osu.ppy.sh/beatmapsets/1990973
- `1999914` — fetch:HTTP 429 from https://osu.ppy.sh/beatmapsets/1999914
- `2018806` — fetch:HTTP 429 from https://osu.ppy.sh/beatmapsets/2018806
- `2042736` — fetch:HTTP 429 from https://osu.ppy.sh/beatmapsets/2042736
- `2056650` — fetch:HTTP 429 from https://osu.ppy.sh/beatmapsets/2056650
- `2066130` — fetch:HTTP 429 from https://osu.ppy.sh/beatmapsets/2066130
- `2086554` — fetch:HTTP 429 from https://osu.ppy.sh/beatmapsets/2086554
- `2092851` — fetch:HTTP 429 from https://osu.ppy.sh/beatmapsets/2092851
- `2120912` — fetch:HTTP 429 from https://osu.ppy.sh/beatmapsets/2120912
- `2121057` — fetch:HTTP 429 from https://osu.ppy.sh/beatmapsets/2121057
- `2135628` — fetch:HTTP 429 from https://osu.ppy.sh/beatmapsets/2135628
- `2150616` — fetch:HTTP 429 from https://osu.ppy.sh/beatmapsets/2150616
- `2174924` — fetch:HTTP 429 from https://osu.ppy.sh/beatmapsets/2174924
- `2197940` — fetch:HTTP 429 from https://osu.ppy.sh/beatmapsets/2197940
- `2227686` — fetch:HTTP 429 from https://osu.ppy.sh/beatmapsets/2227686
- `2231358` — fetch:HTTP 429 from https://osu.ppy.sh/beatmapsets/2231358
- `2237688` — fetch:HTTP 429 from https://osu.ppy.sh/beatmapsets/2237688
- `2245252` — fetch:HTTP 429 from https://osu.ppy.sh/beatmapsets/2245252
- `2248177` — fetch:HTTP 429 from https://osu.ppy.sh/beatmapsets/2248177
- `2261894` — fetch:HTTP 429 from https://osu.ppy.sh/beatmapsets/2261894
- `2271637` — fetch:HTTP 429 from https://osu.ppy.sh/beatmapsets/2271637
- `2279370` — fetch:HTTP 429 from https://osu.ppy.sh/beatmapsets/2279370
- `2282096` — fetch:HTTP 429 from https://osu.ppy.sh/beatmapsets/2282096
- `2282117` — fetch:HTTP 429 from https://osu.ppy.sh/beatmapsets/2282117
- `2305050` — fetch:HTTP 429 from https://osu.ppy.sh/beatmapsets/2305050
- `2308851` — fetch:HTTP 429 from https://osu.ppy.sh/beatmapsets/2308851
- `2313682` — fetch:HTTP 429 from https://osu.ppy.sh/beatmapsets/2313682
- `2324756` — fetch:HTTP 429 from https://osu.ppy.sh/beatmapsets/2324756

These rows remain outside this batch rather than being guessed or promoted from weaker signals.

## Validation contract

The companion workflow runs `make check`, `make build`, and `git diff --check` after the write, and asserts that catalog cardinality increases by exactly the accepted-ID count.
