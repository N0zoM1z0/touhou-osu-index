# Touhou coverage wave 2 — reviewed 206-set expansion (2026-09)

## Scope and trust boundary

This pass starts from the post-PR-#32 canonical `main` and deliberately separates two evidence classes. It never treats a generic `Touhou` / `東方Project` osu! source string as sufficient on its own, because the merge review of PR #32 proved that class can contain Touhou-associated image originals rather than arrangements.

- base catalog: **4232**
- Class A (specific official game source + >=2 discovery queries + current Touhou/ZUN tag signal + API/page exact): **193**
- Class B (quarantined metadata class + manually frozen independent composition provenance + API/page exact): **13**
- total new beatmapsets: **206**
- final catalog: **4438**

## Discovery and verification

- configured discovery queries: **89**
- cursor pages/query: up to **12**
- unique beatmapsets discovered: **6078**
- absent from the post-#32 catalog: **3343**
- live API exact verification: **206/206**
- separate public-page canonical JSON verification: **206/206**
- configured live source reports re-imported: **43** (6977 records)
- selected rows with additional configured-source overlap: **5**

All selected IDs were absent before writeback. The writer asserts every pre-existing catalog record remains field-for-field identical and uses `Catalog.save()` only after all live gates have passed.

## Final distribution

- statuses: `{'ranked': 202, 'loved': 4}`
- modes: `{'osu': 95, 'taiko': 58, 'catch': 19, 'mania': 37}`
- discovery-query corroboration: `{2: 48, 3: 77, 4: 57, 5: 16, 6: 7, 7: 1}`

### Source strings

- `東方紅魔郷　～ the Embodiment of Scarlet Devil.` — 83
- `東方地霊殿　～ Subterranean Animism.` — 42
- `東方妖々夢　～ Perfect Cherry Blossom.` — 22
- `東方永夜抄　～ Imperishable Night.` — 21
- `東方Project` — 12
- `東方花映塚　～ Phantasmagoria of Flower View.` — 10
- `東方神霊廟　～ Ten Desires.` — 6
- `東方星蓮船　～ Undefined Fantastic Object.` — 5
- `東方風神録　～ Mountain of Faith.` — 4
- `東方紅魔郷 ～ the Embodiment of Scarlet Devil.` — 1

## Class B — manually reviewed independent composition provenance

These rows are the only quarantined-source candidates promoted in this wave. Each was manually checked against a track/release source that explicitly names the underlying Touhou original(s). TouhouDB alone is not accepted as a final arbiter: it misclassifies the already-reviewed `Knife - Story` boundary, so the final B allowlist uses stronger release/track evidence.

| Beatmapset | Track | Independent relation | Source |
| ---: | --- | --- | --- |
| `386620` | ARM — Rhododendron | 月まで届け、不死の煙 | https://touhou.arrangement-chronicle.com/original_song/%E6%9D%B1%E6%96%B9%E6%B0%B8%E5%A4%9C%E6%8A%84/%E6%9C%88%E3%81%BE%E3%81%A7%E5%B1%8A%E3%81%91%E3%80%81%E4%B8%8D%E6%AD%BB%E3%81%AE%E7%85%99 |
| `399965` | shio — Qronostasis -GABBA vs. Speedcore mix- | 天空のグリニッジ; THBWiki track 3450769: arrange=shio, ogmusic=天空のグリニッジ | https://thwiki.cc/album.php |
| `1550437` | tsunamix_underground — Period. ~ Seishin no Kousoku to Jiyuu o Tsukamu Jouka | 天空のグリニッジ | https://touhou.arrangement-chronicle.com/original_song/%E5%A4%A7%E7%A9%BA%E9%AD%94%E8%A1%93/%E5%A4%A9%E7%A9%BA%E3%81%AE%E3%82%B0%E3%83%AA%E3%83%8B%E3%83%83%E3%82%B8 |
| `1635625` | SOUND HOLIC — PRESERVED VAMPIRE | 月時計 ～ ルナ・ダイアル; フラワリングナイト | https://sound-holic.booth.pm/items/3530545 |
| `1644488` | A-One feat. Shihori — Magic Girl !! | 魔法少女達の百年祭 | https://thwiki.cc/index.php?setlang=en&title=%E6%AD%8C%E8%AF%8D%3AMagic_Girl_%21%21 |
| `1928250` | Shibayan feat. Tsubaki Ichimatsu — GAZE IT | 天空のグリニッジ | https://booth.pm/en/items/1663468 |
| `1942214` | GET IN THE RING — Midnight Syndrome | 燕石博物誌が連れてきた闇; バー・オールドアダム; アウトサイダーカクテル; 旧世界の冒険酒場 | https://thwiki.cc/index.php?setlang=en&title=%E6%AD%8C%E8%AF%8D%3AMidnight_Syndrome |
| `2120912` | tsunamix — stella maris | ネクロファンタジア; 夜が降りてくる ～ Evening Star | https://touhou.arrangement-chronicle.com/circle/AGGRESSIVE%20BEAT%20CIRCLE/album/AGGRESSIVE%20GENERATION |
| `2149949` | GET IN THE RING — Midnight Syndrome | 燕石博物誌が連れてきた闇; バー・オールドアダム; アウトサイダーカクテル; 旧世界の冒険酒場 | https://thwiki.cc/index.php?setlang=en&title=%E6%AD%8C%E8%AF%8D%3AMidnight_Syndrome |
| `2320572` | TUMENECO feat. yukina & Mii — Itsuka Kimi to Mukaeru Yoake | 日本中の不思議を集めて | https://www.melonbooks.co.jp/detail/detail.php?product_id=2411052 |
| `2322699` | minimum electric design — miscalc | 童祭 ～ Innocent Treasures | https://touhou.arrangement-chronicle.com/circle/minimum%20electric%20design/album/TRAIL%20III%20DISC-1 |
| `2472186` | ryu5150 — Battle Warrior!! | 少女綺想曲; 東方妖恋談 | https://ryu-5150.jp/disc/%E3%82%B7%E3%83%B3%E3%83%95%E3%82%A9%E3%83%8B%E3%83%83%E3%82%AF%E6%9D%B1%E6%96%B9%E2%85%B4/ |
| `2530670` | tsunamix — stella maris | ネクロファンタジア; 夜が降りてくる ～ Evening Star | https://touhou.arrangement-chronicle.com/circle/AGGRESSIVE%20BEAT%20CIRCLE/album/AGGRESSIVE%20GENERATION |

## Additional configured-source overlaps

- `1128939` — `official_pack_item:FQ40`
- `1644488` — `official_pack_item:FQ66`, `official_pack_item:R309`
- `2141740` — `official_pack_item:R334`
- `2159203` — `official_pack_item:R340`
- `2220709` — `official_pack_item:R332`

## Accepted IDs

### Class A

- `69173`, `556969`, `579359`, `582888`, `1128939`, `1241481`, `1277845`, `1324962`, `1349838`, `1368759`, `1374425`, `1397832`, `1573417`, `1576656`, `1579075`, `1588466`, `1601650`, `1618365`, `1641141`, `1649093`
- `1704340`, `1715998`, `1716009`, `1752523`, `1763702`, `1765375`, `1780135`, `1784332`, `1811874`, `1817787`, `1832066`, `1837942`, `1840481`, `1852057`, `1857047`, `1861782`, `1878008`, `1892797`, `1896626`, `1901650`
- `1909936`, `1913078`, `1913796`, `1914658`, `1915327`, `1921061`, `1921815`, `1929270`, `1931429`, `1941763`, `1942061`, `1953513`, `1958464`, `1969255`, `1971670`, `1972745`, `1984348`, `1990973`, `1999914`, `2006619`
- `2006943`, `2012401`, `2014469`, `2018806`, `2020167`, `2022219`, `2030543`, `2030733`, `2033193`, `2034075`, `2035737`, `2039084`, `2042736`, `2048946`, `2056468`, `2056650`, `2060837`, `2064066`, `2065149`, `2066130`
- `2071645`, `2072440`, `2072915`, `2080690`, `2080925`, `2082657`, `2086554`, `2086616`, `2088280`, `2089306`, `2092851`, `2120920`, `2121057`, `2122307`, `2135628`, `2136154`, `2141740`, `2143839`, `2144555`, `2150144`
- `2150616`, `2155937`, `2159203`, `2159661`, `2166782`, `2170949`, `2174924`, `2176852`, `2192796`, `2194940`, `2197609`, `2197940`, `2198080`, `2217257`, `2220709`, `2223022`, `2226125`, `2227686`, `2231358`, `2239310`
- `2241785`, `2248177`, `2254348`, `2254629`, `2254847`, `2256857`, `2261894`, `2266294`, `2266612`, `2270937`, `2271637`, `2278914`, `2279370`, `2282096`, `2282117`, `2285652`, `2305050`, `2305505`, `2305788`, `2308851`
- `2313682`, `2315649`, `2316692`, `2317462`, `2322334`, `2324756`, `2331469`, `2336986`, `2345463`, `2352149`, `2354377`, `2358120`, `2362559`, `2364934`, `2365171`, `2389260`, `2392966`, `2398086`, `2407462`, `2410016`
- `2410294`, `2414966`, `2415448`, `2416218`, `2417668`, `2418853`, `2424250`, `2441875`, `2455224`, `2458692`, `2465439`, `2483766`, `2489824`, `2497259`, `2497564`, `2500223`, `2503577`, `2508608`, `2509002`, `2516975`
- `2522131`, `2524492`, `2525930`, `2525946`, `2534821`, `2538196`, `2551839`, `2555232`, `2559045`, `2559071`, `2564142`, `2564859`, `2608197`

### Class B

- `386620`, `399965`, `1550437`, `1635625`, `1644488`, `1928250`, `1942214`, `2120912`, `2149949`, `2320572`, `2322699`, `2472186`, `2530670`

## Explicit rejection boundary

### Quarantined rows not promoted

- `351574` — **t+pazolite & COMP - Sayonara Matane** — `generic` — withheld: no manually frozen independent release/original relation at the reviewed B-class standard
- `356543` — **Demetori - Higan Kikou ~ View of The River Styx** — `generic` — withheld: no manually frozen independent release/original relation at the reviewed B-class standard
- `381363` — **Kurenainagi Tabibito - Otenba Koimusume** — `game_no_tag` — withheld: no manually frozen independent release/original relation at the reviewed B-class standard
- `401354` — **Demetori - Youkai no Yama ~ Mysterious Mountain** — `generic` — withheld: no manually frozen independent release/original relation at the reviewed B-class standard
- `1342305` — **FELT - Songs Compilation** — `generic` — withheld: no manually frozen independent release/original relation at the reviewed B-class standard
- `1350314` — **dev - lovely freezing tomboy bath** — `generic` — dev - lovely freezing tomboy bath: exact-title THBWiki result names different arrangers (uno / 808sndmindbreak), so artist/composition identity is not safely resolved.
- `1771472` — **Kobaryo - Outer Occult Occupation** — `generic` — withheld: no manually frozen independent release/original relation at the reviewed B-class standard
- `2023362` — **ZYTOKINE - Dancing Dollz feat. cold kiss - REDALiCE Remix** — `generic` — withheld: no manually frozen independent release/original relation at the reviewed B-class standard
- `2049932` — **Knife - Negaigoto Liner 2020** — `generic` — withheld: no manually frozen independent release/original relation at the reviewed B-class standard
- `2096026` — **Knife - Story** — `generic` — Knife - Story: independent release/live documentation identifies it as a Hifuu image original, not an arrangement; retained as the PR #32 negative boundary.
- `2109511` — **Knife - Story** — `generic` — Knife - Story: same composition as the reviewed PR #32 false-positive; generic Touhou source / TouhouDB metadata is not sufficient.
- `2145065` — **GET IN THE RING - Hana wa Sakuragi, Hito wa Kaze** — `generic` — withheld: no manually frozen independent release/original relation at the reviewed B-class standard
- `2172715` — **TUMENECO VS. GET IN THE RING - Yumeuta - Tokubetsu na Futari no Uta** — `generic` — withheld: no manually frozen independent release/original relation at the reviewed B-class standard
- `2237688` — **IOSYS - Makudo wa Taihen na Mono o Tsukutte Ikimashita** — `generic` — withheld: no manually frozen independent release/original relation at the reviewed B-class standard
- `2245252` — **Foxtail-Grass Studio - Shade, Hat, and Wind Chimes** — `generic` — withheld: no manually frozen independent release/original relation at the reviewed B-class standard
- `2251577` — **TUMENECO VS. GET IN THE RING - Yumeuta - Tokubetsu na Futari no Uta** — `generic` — withheld: no manually frozen independent release/original relation at the reviewed B-class standard
- `2439565` — **Diao Ye Zong feat. Meramipop - Zettai-teki Ippou Tsuukou ~ Unreachable Message** — `generic` — withheld: no manually frozen independent release/original relation at the reviewed B-class standard
- `2523183` — **BUTAOTOME - Moonstone** — `generic` — withheld: no manually frozen independent release/original relation at the reviewed B-class standard

### Historical-source recovery checked but not used

The recovered Google Published Sheet link for the 2019 first Touhou Tournament was tested through its HTML, XLSX and CSV publication endpoints. All currently return HTTP 410 Gone, so the historical tournament remains a documented lead rather than a reproducible source and contributes no acceptance evidence here.

## Reproduction / validation contract

The temporary branch-only writer runs the full discovery, API/page verification, configured-source re-import, semantic old-row guard, then `make check`, `python -m touhou_osu validate`, `make build`, and `git diff --check`. Temporary writer/workflow files are removed before the PR is opened.
