# Source audit — 2026-09 wave 3 deep coverage

This pass follows the merged 200+ coverage waves and intentionally targets the long tail those ranked/loved-oriented sweeps miss: status-scoped Bad Apple derivatives plus exact ZUN-original graveyard identities.

## Acceptance policy

No row is accepted from a search keyword alone. Every accepted beatmapset is absent from the pre-write catalog and is freshly re-fetched from both osu! API v2 and the public beatmapset page; ID, artist, title, creator, source, status, and modes must agree.

### Bad Apple class

A row must match the Arrangement Chronicle Bad Apple corpus by normalized exact title and by circle/vocalist/arranger identity. It is then required to have at least one additional corroborating class: a recognized Touhou game source, a first-party Alstroemeria derivative/title relationship, a first-party parent-work identity, or THBWiki support. Explicit external contradictions or ambiguous provenance are withheld.

### ZUN-original class

A row must have current artist exactly `ZUN` after normalization and an exact normalized alias for one of seven controlled ZUN original themes. The theme must also still exist in Arrangement Chronicle's live original-song statistics. Search-result metadata is revalidated against both current osu! surfaces before insertion.

## Source corpus

- osu! API v2 `/beatmapsets/search` and `/beatmapsets/{id}`
- public `https://osu.ppy.sh/beatmapsets/{id}` canonical embedded metadata
- Alstroemeria Records first-party release pages: `https://alst.net/arcd0056/`, `https://alst.net/arcd0060/`, `https://alst.net/arcd0065/`
- Touhou Arrangement Chronicle Bad Apple corpus and original-song statistics
- THBWiki + TouhouDB as advisory contradiction/support providers for the Bad Apple composition class

## Search breadth

- base catalog before this pass: **4438** beatmapsets
- Bad Apple status/query buckets: **42**
- unique Bad Apple search results: **4596**
- live Arrangement Chronicle Bad Apple rows parsed: **472**
- absent exact-title + exact-identity Bad Apple candidates: **232**
- Bad Apple candidates after secondary corroboration/contradiction gate: **230**
- ZUN-original status/query buckets: **108**
- unique ZUN-theme search results: **17158**
- absent exact ZUN-original candidates before direct re-fetch: **126**
- final accepted after current API + public-page verification: **356**
- catalog after write: **4794**
- direct verification failures withheld: **0**

## Final batch summary

- audit classes: bad_apple=230, zun_original=126
- statuses: graveyard=352, ranked=1, wip=3
- modes: catch=10, mania=120, osu=215, taiko=27

### Evidence-rule counts

- `chronicle_exact_identity`: **230**
- `primary_parent_artist`: **207**
- `thbwiki_supported`: **130**
- `zun_exact_original`: **126**
- `primary_official_derivative`: **96**
- `explicit_game_source`: **38**

### Theme counts

- `Bad Apple!!`: **230**
- `U.N.オーエンは彼女なのか？`: **51**
- `月まで届け、不死の煙`: **18**
- `ネクロファンタジア`: **16**
- `ハルトマンの妖怪少女`: **15**
- `亡き王女の為のセプテット`: **14**
- `おてんば恋娘`: **6**
- `恋色マスタースパーク`: **6**
- `装飾戦 ～ Decoration Battle`: **1**
- `霊戦 ～ Perdition crisis`: **1**


### Mixed structured provenance correction

The pre-merge review found one accepted Bad Apple recording whose structured provenance was incomplete even though the beatmapset itself was correctly in scope. Beatmapset `2603026` — **IOSYS — Bad Apple & Good Orange** — is documented by the live Arrangement Chronicle corpus as using three Touhou originals: `Bad Apple!!`, `装飾戦 ～ Decoration Battle`, and `霊戦 ～ Perdition crisis`. All three originate from `東方幻想郷 ～ Lotus Land Story`, so `origin_games` remains one game while `touhou_kind` is corrected from `arrangement` to `mixed` and all three supported originals are retained.

A full reverse scan of all 230 accepted Bad Apple rows against the same live corpus found no other accepted row with more than one supported original, so this is the only structured-provenance correction required by the pre-merge review.

## Accepted beatmapsets

| ID | Class | Artist | Title | Status | Modes | Rules |
| ---: | --- | --- | --- | --- | --- | --- |
| 5860 | zun_original | ZUN | U.N. Owen was her? | graveyard | osu | zun_exact_original |
| 6252 | bad_apple | nomico | Bad Apple!! | ranked | osu | chronicle_exact_identity, primary_parent_artist |
| 6279 | bad_apple | Alstroemeria Records | Bad Apple!! (REDALICE Remix) | graveyard | osu | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 6805 | zun_original | ZUN | Necrofantasia | graveyard | osu | zun_exact_original |
| 6927 | zun_original | ZUN | Reach for the Moon, Immortal Smoke | graveyard | osu | zun_exact_original |
| 7211 | zun_original | ZUN | Septette for the Dead Princess | graveyard | osu | zun_exact_original |
| 10372 | bad_apple | Alstroemeria Records | Bad Apple!! feat. nomico | graveyard | osu | chronicle_exact_identity, primary_official_derivative, primary_parent_artist, thbwiki_supported |
| 10810 | bad_apple | Alstroemeria Records | Bad Apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 11063 | zun_original | ZUN | U.N. Owen was her? | graveyard | osu | zun_exact_original |
| 11103 | zun_original | ZUN | U.N Owen Was Her | graveyard | osu | zun_exact_original |
| 11289 | bad_apple | Alstroemeria Records | Bad Apple (REDALiCE Remix) | graveyard | taiko | chronicle_exact_identity, primary_parent_artist |
| 13851 | bad_apple | Masayoshi Minoshima ft. nomico | Bad Apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 19546 | bad_apple | Masayoshi Minoshima ft. nomico | Bad Apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 20185 | zun_original | ZUN | Beloved Tomboyish Girl | graveyard | osu | zun_exact_original |
| 21858 | zun_original | ZUN | Hartmann's Youkai Girl | graveyard | osu | zun_exact_original |
| 26479 | zun_original | ZUN | Necrofantasia | graveyard | osu | zun_exact_original |
| 29894 | bad_apple | Masayoshi Minoshimaft. Nomico | Bad Apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 30655 | bad_apple | Ryo Ohnuki ft. nomico | Bad Apple!! (Graph Tech Remix) | graveyard | osu | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 35246 | bad_apple | Touhou (masayoshi Minoshima ft.nomico) | Bad Apple!! | graveyard | osu,taiko | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 40987 | zun_original | ZUN | Beloved Tomboyish Girl | graveyard | osu,taiko | zun_exact_original |
| 42142 | bad_apple | Nomico | Bad Apple!! [Graph Tech Remix] | graveyard | osu | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 53627 | zun_original | ZUN | U.N. Owen Was Her? | graveyard | catch | zun_exact_original |
| 63596 | zun_original | ZUN | Hartmann's Youkai Girl | graveyard | osu | zun_exact_original |
| 65303 | zun_original | ZUN | Septette for the Dead Princess | graveyard | osu | zun_exact_original |
| 65884 | bad_apple | Masayoshi Minoshima | Bad Apple | graveyard | osu,taiko | chronicle_exact_identity, primary_parent_artist |
| 66300 | bad_apple | nomico | Bad Apple!! (Graph Tech Remix) | graveyard | taiko | chronicle_exact_identity, primary_parent_artist |
| 66369 | zun_original | zun | U.N. Owen was her | graveyard | osu | zun_exact_original |
| 68177 | bad_apple | Kiyoma | Bad Apple!! | graveyard | osu | chronicle_exact_identity, thbwiki_supported |
| 72472 | zun_original | ZUN | U.N. Owen Was Her? | graveyard | catch,osu | zun_exact_original |
| 91776 | bad_apple | Masayoshi Minoshima feat nomico | Bad Apple! | graveyard | taiko | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 103830 | bad_apple | Masayoshi Minoshima feat. nomico | bad apple! | graveyard | osu | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 105516 | bad_apple | Masayoshi Minoshima ft. nomico | Bad Apple!! | graveyard | mania | chronicle_exact_identity, primary_parent_artist |
| 110651 | bad_apple | Masayoshi Minoshima ft. nomico | Bad Apple!! | graveyard | mania,osu | chronicle_exact_identity, primary_parent_artist |
| 114386 | zun_original | ZUN | U.N Owen Was Her | graveyard | osu | zun_exact_original |
| 138871 | zun_original | ZUN | Necrofantasia | graveyard | osu | zun_exact_original |
| 141839 | zun_original | ZUN | U.N Owen was Her? | graveyard | osu | zun_exact_original |
| 152096 | bad_apple | Masayoshi Minoshima ft nomico | Bad Apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 152286 | bad_apple | Masayoshi Minoshima ft nomico | Bad Apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 164091 | zun_original | ZUN | Reach for the Moon, Immortal Smoke | graveyard | osu,taiko | zun_exact_original |
| 170160 | zun_original | ZUN | Necrofantasia | graveyard | osu | zun_exact_original |
| 172422 | zun_original | ZUN | U.N. Owen Was Her | graveyard | osu | zun_exact_original |
| 179934 | zun_original | zun | Necro Fantasia | graveyard | mania | zun_exact_original |
| 190512 | zun_original | ZUN | U.N Owen Was Her | graveyard | mania | zun_exact_original |
| 227666 | zun_original | ZUN | Hartmann's Youkai Girl | graveyard | osu | zun_exact_original |
| 229020 | zun_original | ZUN | U.N. Owen Was Her? | graveyard | osu | zun_exact_original |
| 237626 | bad_apple | Masayoshi Minoshima feat nomico | Bad Apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 254743 | zun_original | ZUN | U.N. Owen Was Her? | graveyard | catch | zun_exact_original |
| 289924 | zun_original | ZUN | Septette for the Dead Princess | graveyard | osu | zun_exact_original |
| 299542 | zun_original | ZUN | U.N. Owen was her? | graveyard | osu | zun_exact_original |
| 305025 | zun_original | ZUN | Reach for the moon Immortal smoke | graveyard | mania | zun_exact_original |
| 306191 | bad_apple | Masayoshi Minoshima ft nomico | Bad apple | graveyard | mania | chronicle_exact_identity, primary_parent_artist |
| 329951 | bad_apple | Masayoshi Minoshima feat. nomico | Bad Apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 330810 | bad_apple | Alstroemeria Records | Bad Apple | graveyard | osu | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 355643 | bad_apple | Nomico | Bad Apple!! REDALiCE Remix | graveyard | mania | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 361928 | bad_apple | Masayoshi Minashima feat. Nomico | Bad Apple | graveyard | taiko | chronicle_exact_identity, primary_parent_artist |
| 370570 | bad_apple | Masayoshi Minoshima feat.nomico | Bad Apple!! | graveyard | taiko | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 398161 | bad_apple | Masayoshi Minoshima Ft. Nomico | Bad Apple!! | graveyard | mania | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 402992 | zun_original | ZUN | U.N owen was her | graveyard | osu | zun_exact_original |
| 412602 | zun_original | ZUN | U.N Owen Was Her? | graveyard | osu | zun_exact_original |
| 416197 | bad_apple | nomico | Bad Apple!! | graveyard | mania | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 429847 | zun_original | ZUN | U.N. Owen Was Her? | graveyard | osu | zun_exact_original |
| 440313 | bad_apple | Masayoshi Minoshima feat. nomico | Bad Apple!! | graveyard | taiko | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 441798 | zun_original | ZUN | reach for the moon immortal smoke | graveyard | mania | zun_exact_original |
| 443307 | bad_apple | Masayoshi Minoshima feat. nomico | Bad Apple | graveyard | osu | chronicle_exact_identity, primary_parent_artist |
| 447852 | bad_apple | Masayoshi Minoshima feat. nomico | Bad Apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 468906 | bad_apple | Masayoshi Minoshima feat. nomico | Bad Apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 469558 | bad_apple | Masayoshi Minoshima ft. nomico | Bad Apple !! | graveyard | mania | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 475175 | zun_original | ZUN | Necrofantasia | graveyard | mania | zun_exact_original |
| 478067 | bad_apple | Masayoshi Minoshima ft. nomico | Bad Apple!! | graveyard | mania | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 478636 | bad_apple | Masayoshi Minoshima ft. nomico | Bad Apple!!!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist |
| 487260 | bad_apple | Masayoshi Minoshima ft. nomico | Bad Apple !!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist |
| 491142 | zun_original | ZUN | Reach for the Moon ~ Immortal Smoke | graveyard | osu | zun_exact_original |
| 498491 | bad_apple | Nomico | Bad Apple | graveyard | osu | chronicle_exact_identity, primary_parent_artist |
| 501262 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat. nomico | graveyard | mania | chronicle_exact_identity, primary_official_derivative, primary_parent_artist, thbwiki_supported |
| 522127 | bad_apple | Masayoshi Minoshima ft. nomico | Bad Apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 552438 | bad_apple | Demetori | Bad Apple!!  Death of A Bad Apple | graveyard | osu | chronicle_exact_identity, thbwiki_supported |
| 554190 | bad_apple | Masayoshi Minoshima ft. nomico | Bad Apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 555037 | bad_apple | nomico | Bad Apple!! feat. nomico | graveyard | osu | chronicle_exact_identity, primary_official_derivative, primary_parent_artist, thbwiki_supported |
| 559299 | bad_apple | Masayoshi Minoshima ft. nomico | Bad Apple!! | graveyard | mania | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 561026 | bad_apple | Masayoshi Minoshima ft. nomico | Bad Apple!! | graveyard | mania | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 565540 | bad_apple | nomico | Bad apple! | graveyard | taiko | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 569583 | bad_apple | Nomico | Bad Apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 587241 | bad_apple | Alstroemeria Records | Bad Apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist |
| 590214 | zun_original | ZUN | U.N. Owen Was Her | graveyard | osu | zun_exact_original |
| 595350 | zun_original | ZUN | U.N. Owen Was Her | graveyard | osu | zun_exact_original |
| 600668 | zun_original | ZUN | U.N. Owen was her | graveyard | osu | zun_exact_original |
| 604321 | bad_apple | Alstroemeria Records | Bad Apple!! feat. nomico | graveyard | mania | chronicle_exact_identity, primary_official_derivative, primary_parent_artist, thbwiki_supported |
| 611128 | zun_original | ZUN | U.N. Owen was her | graveyard | osu | zun_exact_original |
| 613152 | bad_apple | Alstroemeria Records | Bad Apple!! | graveyard | mania | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 618078 | zun_original | Zun | Hartmanns youkai girl | graveyard | osu | zun_exact_original |
| 619359 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat.nomico (Nhato remix) | graveyard | taiko | chronicle_exact_identity, explicit_game_source, primary_official_derivative, primary_parent_artist, thbwiki_supported |
| 621337 | bad_apple | Alstroemeria Records | Bad Apple!! feat. nomico (Nhato Remix) | graveyard | osu | chronicle_exact_identity, primary_official_derivative, primary_parent_artist |
| 623651 | bad_apple | Masayoshi Minoshima / Vo.nomico | Bad Apple!! feat.nomico(2014 Refix) | graveyard | mania | chronicle_exact_identity, primary_official_derivative, primary_parent_artist, thbwiki_supported |
| 636656 | bad_apple | Alstroemeria Records | Bad Apple!! feat. nomico | graveyard | osu | chronicle_exact_identity, primary_official_derivative, primary_parent_artist, thbwiki_supported |
| 637002 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat.nomico (Nhato Remix) | graveyard | osu | chronicle_exact_identity, primary_official_derivative, primary_parent_artist, thbwiki_supported |
| 654935 | bad_apple | Nhato | Bad Apple!! feat.nomico (Nhato Remix) | graveyard | osu | chronicle_exact_identity, primary_official_derivative |
| 679879 | bad_apple | Masayoshi Minoshima | Bad Apple | graveyard | osu | chronicle_exact_identity, primary_parent_artist |
| 683560 | bad_apple | Masayoshi Minoshima feat. nomico | Bad Apple!! | graveyard | mania | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 688923 | bad_apple | Alstroemeria Records feat. REDALiCE | Bad Apple (REDALiCE Remix) | graveyard | mania | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 703321 | bad_apple | nomico (Nhato Remix) | Bad Apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 710015 | zun_original | Zun | U.N. Owen was her? | graveyard | osu | zun_exact_original |
| 711839 | zun_original | ZUN | Beloved Tomboyish Girl | graveyard | osu | zun_exact_original |
| 723526 | zun_original | ZUN | Hartmann's Youkai Girl | graveyard | mania | zun_exact_original |
| 727355 | zun_original | ZUN | U.N. Owen Was Her? | graveyard | osu | zun_exact_original |
| 727765 | bad_apple | Alstroemeria Records | Bad Apple!! feat. nomico | graveyard | mania | chronicle_exact_identity, explicit_game_source, primary_official_derivative, primary_parent_artist, thbwiki_supported |
| 727917 | zun_original | ZUN | Love-Coloured Master Spark | graveyard | osu | zun_exact_original |
| 731234 | bad_apple | Masayoshi Minoshima | Bad Apple | graveyard | osu | chronicle_exact_identity, primary_parent_artist |
| 740637 | bad_apple | Alstroemeria Records / Jubyphonic | Bad Apple | graveyard | osu | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 745314 | bad_apple | Nhato | Bad Apple!! feat.nomico (Nhato Remix) | graveyard | osu | chronicle_exact_identity, primary_official_derivative |
| 745426 | bad_apple | Nhato | Bad Apple!! feat.nomico (Nhato Remix) | graveyard | osu | chronicle_exact_identity, primary_official_derivative |
| 757565 | bad_apple | nomico | Bad Apple!! feat. nomico | graveyard | osu | chronicle_exact_identity, primary_official_derivative, primary_parent_artist, thbwiki_supported |
| 772068 | bad_apple | Nomico | Bad Apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 783667 | bad_apple | JubyPhonic / Masayoshi Minoshima | Bad Apple | graveyard | osu | chronicle_exact_identity, primary_parent_artist |
| 786909 | zun_original | ZUN | Reach for the Moon, Immortal Smoke | graveyard | osu | zun_exact_original |
| 794346 | zun_original | ZUN | Reach for the Moon, Immortal Smoke | graveyard | osu | zun_exact_original |
| 799135 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat.nomico (Camellia's "Bad Psy!!" Remix) | graveyard | osu | chronicle_exact_identity, primary_official_derivative, primary_parent_artist |
| 799327 | bad_apple | nomico | Bad Apple!! feat. nomico | graveyard | catch,osu | chronicle_exact_identity, primary_official_derivative, primary_parent_artist, thbwiki_supported |
| 804985 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat.nomico (Nhato Remix) | graveyard | osu | chronicle_exact_identity, explicit_game_source, primary_official_derivative, primary_parent_artist |
| 808710 | bad_apple | Nomico | Bad Apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist |
| 816663 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat.Nomico (Nhato Remix) | graveyard | osu | chronicle_exact_identity, primary_official_derivative, primary_parent_artist |
| 816853 | zun_original | ZUN | U.N. Owen was Her? | graveyard | catch,mania,osu,taiko | zun_exact_original |
| 817162 | zun_original | ZUN | U.N. Owen was her? | graveyard | mania | zun_exact_original |
| 821938 | zun_original | Zun | U.N Owen was Her? | graveyard | osu | zun_exact_original |
| 825805 | bad_apple | nomico | Bad Apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 826295 | bad_apple | Nhato Remix | Bad Apple!! feat.nomico (Nhato Remix) | graveyard | mania | chronicle_exact_identity, primary_official_derivative, thbwiki_supported |
| 846891 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat.nomico (Nhato Remix) | graveyard | osu | chronicle_exact_identity, primary_official_derivative, primary_parent_artist, thbwiki_supported |
| 847262 | bad_apple | Alstroemeria Records | Bad Apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist |
| 848623 | bad_apple | Masayoshi Minoshima feat. nomico | Bad Apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 859462 | bad_apple | Nhato | Bad Apple!! feat.nomico (Nhato Remix) | graveyard | osu | chronicle_exact_identity, explicit_game_source, primary_official_derivative |
| 859688 | zun_original | ZUN | U.N. Owen was her? | graveyard | osu | zun_exact_original |
| 860899 | bad_apple | Masayoshi Minoshima feat. nomico | Bad Apple | graveyard | osu | chronicle_exact_identity, primary_parent_artist |
| 864861 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat. nomico | graveyard | mania | chronicle_exact_identity, primary_official_derivative, primary_parent_artist, thbwiki_supported |
| 866839 | bad_apple | Nhato/nomico | Bad Apple!! feat.nomico(Nhato Remix) | graveyard | mania | chronicle_exact_identity, primary_official_derivative, primary_parent_artist |
| 898592 | bad_apple | ZUN, Camellia | Bad Apple!! feat.nomico (Camellia's "Bad Psy!!" Remix) | graveyard | mania | chronicle_exact_identity, primary_official_derivative |
| 918555 | bad_apple | Masayoshi Minoshima ft nomico | Bad apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist |
| 923433 | bad_apple | Masayoshi Minoshima ft. nomico | Bad Apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist |
| 928971 | zun_original | ZUN | Reach for the Moon, Immortal Smoke | graveyard | mania | zun_exact_original |
| 930094 | zun_original | ZUN | Septette for the Dead Princess | graveyard | mania | zun_exact_original |
| 930754 | zun_original | ZUN | Necrofantasia | graveyard | osu | zun_exact_original |
| 932601 | bad_apple | Camellia | Bad Apple!! feat.nomico (Camellia's "Bad Psy!!" Remix) | graveyard | mania | chronicle_exact_identity, primary_official_derivative |
| 940413 | bad_apple | Camellia | Bad Apple!! feat.nomico  (Camellia's "Bad Psy!!" Remix) | graveyard | mania | chronicle_exact_identity, primary_official_derivative |
| 941896 | zun_original | ZUN | U.N OWEN WAS HER ? | graveyard | osu | zun_exact_original |
| 943649 | zun_original | ZUN | U.N. Owen was Her ? | graveyard | taiko | zun_exact_original |
| 956136 | zun_original | ZUN | U.N. Owen Was her? | graveyard | osu | zun_exact_original |
| 972327 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat.nomico (Nhato Remix) | graveyard | osu | chronicle_exact_identity, primary_official_derivative, primary_parent_artist, thbwiki_supported |
| 983661 | zun_original | ZUN | U.N. Owen Was Her? | graveyard | mania | zun_exact_original |
| 988838 | bad_apple | Masayoshi Minoshima | BAD APPLE !! | graveyard | mania | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 989742 | zun_original | ZUN | Necrofantasia | graveyard | osu | zun_exact_original |
| 997699 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat.nomico | graveyard | osu | chronicle_exact_identity, primary_official_derivative, primary_parent_artist, thbwiki_supported |
| 1003204 | bad_apple | Bad Apple!! feat.nomico (Camellias Bad Psy!! Remix) | Bad Apple!! feat.nomico (Camellias Bad Psy!! Remix) | graveyard | mania | chronicle_exact_identity, primary_official_derivative, primary_parent_artist |
| 1014756 | zun_original | Zun | Hartmann's Youkai Girl | graveyard | taiko | zun_exact_original |
| 1023925 | zun_original | Zun | Hartmann's Youkai Girl | graveyard | mania | zun_exact_original |
| 1030573 | zun_original | Zun | U.N Owen was her? | graveyard | mania | zun_exact_original |
| 1037541 | bad_apple | Masayoshi Minoshima | Bad Apple!!  feat. nomico | graveyard | mania | chronicle_exact_identity, primary_official_derivative, primary_parent_artist, thbwiki_supported |
| 1044698 | zun_original | ZUN | Necrofantasia | graveyard | osu | zun_exact_original |
| 1048437 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat. nomico (Camellia's "Bad Psy!!" Remix) | graveyard | taiko | chronicle_exact_identity, explicit_game_source, primary_official_derivative, primary_parent_artist |
| 1050248 | zun_original | ZUN | Love-colored Master Spark | graveyard | taiko | zun_exact_original |
| 1066025 | bad_apple | Camellia | Bad Apple!! feat.nomico Camellias Bad Psy!! Remix | graveyard | mania | chronicle_exact_identity, primary_official_derivative |
| 1079337 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat. nomico (Nardis Remix) | graveyard | osu | chronicle_exact_identity, primary_official_derivative, primary_parent_artist |
| 1083873 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat. nomico | graveyard | osu | chronicle_exact_identity, explicit_game_source, primary_official_derivative, primary_parent_artist, thbwiki_supported |
| 1123330 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat.nomico (Nhato Remix) | graveyard | osu | chronicle_exact_identity, explicit_game_source, primary_official_derivative, primary_parent_artist |
| 1125891 | zun_original | ZUN | Septette for the Dead Princess | graveyard | mania | zun_exact_original |
| 1128463 | bad_apple | nomico | Bad apple!! (Nardis Remix) | graveyard | osu | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 1132992 | bad_apple | ZUN / Alstroemeria Records ft. Nomico (Un3h remix) | Bad Apple | graveyard | mania | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 1135425 | bad_apple | Nomico | Bad Apple!!!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist |
| 1136618 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat.nomico (Nhato Remix) | graveyard | mania | chronicle_exact_identity, primary_official_derivative, primary_parent_artist, thbwiki_supported |
| 1138647 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat.nomico (Camellia's "Bad Psy!!" Remix) | graveyard | mania | chronicle_exact_identity, explicit_game_source, primary_official_derivative, primary_parent_artist |
| 1139896 | zun_original | ZUN | U.N. Owen was her? | graveyard | osu | zun_exact_original |
| 1161808 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat. nomico | graveyard | osu | chronicle_exact_identity, primary_official_derivative, primary_parent_artist, thbwiki_supported |
| 1164730 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat. nomico | graveyard | osu | chronicle_exact_identity, primary_official_derivative, primary_parent_artist, thbwiki_supported |
| 1190660 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat. nomico | graveyard | osu | chronicle_exact_identity, primary_official_derivative, primary_parent_artist, thbwiki_supported |
| 1214473 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat.nomico (Nhato Remix) | graveyard | taiko | chronicle_exact_identity, explicit_game_source, primary_official_derivative, primary_parent_artist |
| 1214681 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat.nomico (Camellia's "Bad Psy!!" Remix) | graveyard | mania | chronicle_exact_identity, primary_official_derivative, primary_parent_artist |
| 1229163 | zun_original | ZUN | Reach for the Moon, Immortal Smoke | graveyard | osu | zun_exact_original |
| 1231407 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat.nomico (Camellia's "Bad Psy!!" Remix) | graveyard | osu | chronicle_exact_identity, primary_official_derivative, primary_parent_artist |
| 1233534 | bad_apple | Masayoshi Minoshima | Bad apple | graveyard | osu | chronicle_exact_identity, primary_parent_artist |
| 1236532 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat.nomico (Nhato Remix) | graveyard | osu | chronicle_exact_identity, explicit_game_source, primary_official_derivative, primary_parent_artist, thbwiki_supported |
| 1242842 | bad_apple | Camellia | Bad Apple!! feat.nomico (Camellias Bad Psy!! Remix) | graveyard | mania | chronicle_exact_identity, primary_official_derivative |
| 1244759 | bad_apple | Alstroemeria Records | Bad Apple!! (REDALiCE REMIX) | graveyard | mania | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 1245883 | zun_original | ZUN | Septette for the Dead Princess | graveyard | osu | zun_exact_original |
| 1248503 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat. nomico | graveyard | osu | chronicle_exact_identity, primary_official_derivative, primary_parent_artist, thbwiki_supported |
| 1252274 | bad_apple | Masayoshi Minoshima feat. nomico | Bad Apple!! | graveyard | mania | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 1263121 | bad_apple | Nomico | Bad Apple!! | graveyard | mania | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 1282864 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat.nomico (Camellia's "Bad Psy!!" Remix) | graveyard | osu | chronicle_exact_identity, explicit_game_source, primary_official_derivative, primary_parent_artist |
| 1297851 | zun_original | ZUN | Septette for the Dead Princess | graveyard | mania | zun_exact_original |
| 1305653 | zun_original | ZUN | Necrofantasia | graveyard | osu | zun_exact_original |
| 1311982 | bad_apple | Masayoshi Minoshima ft. nomico | Bad Apple | graveyard | osu | chronicle_exact_identity, primary_parent_artist |
| 1321227 | bad_apple | Alstroemeria Records | Bad Apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 1337630 | zun_original | ZUN | U.N. Owen was Her | graveyard | osu | zun_exact_original |
| 1338852 | bad_apple | Alstroemeria Records | Bad Apple!! feat. nomico | graveyard | osu | chronicle_exact_identity, primary_official_derivative, primary_parent_artist, thbwiki_supported |
| 1350010 | bad_apple | nomico | Bad Apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist |
| 1356909 | bad_apple | Masayoshi Minoshima ft. nomico | Bad Apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 1361362 | zun_original | ZUN | Reach for the Moon, Immortal Smoke | graveyard | osu | zun_exact_original |
| 1365640 | bad_apple | nomico | Bad Apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist |
| 1368517 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat.nomico (Camellia's "Bad Psy!!" Remix) | graveyard | mania | chronicle_exact_identity, primary_official_derivative, primary_parent_artist |
| 1372911 | bad_apple | Alstroemeria Records feat. nomico | Bad Apple!! | graveyard | mania | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 1393666 | bad_apple | Masayoshi Minoshima Ft. Nomico | BAD APPLE! ! | graveyard | osu | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 1409063 | bad_apple | Nomico (Camellia) | Bad apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist |
| 1415249 | bad_apple | Masayoshi Minoshima ft. nomico | Bad Apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 1416900 | bad_apple | Masayoshi Minoshima ft. nomico | Bad Apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 1423567 | bad_apple | Masayoshi Minoshima ft. nomico | Bad Apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 1431249 | bad_apple | nomico | Bad Apple | graveyard | osu | chronicle_exact_identity, primary_parent_artist |
| 1433256 | bad_apple | Alstroemeria Records | Bad Apple!! feat. nomico | graveyard | osu | chronicle_exact_identity, primary_official_derivative, primary_parent_artist, thbwiki_supported |
| 1434426 | zun_original | Zun | U.N. Owen Was Her? | graveyard | mania | zun_exact_original |
| 1437454 | bad_apple | Masayoshi Minoshima ft nomico | Bad Apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist |
| 1440119 | bad_apple | Alstroemeria | Bad Apple!! | graveyard | osu | chronicle_exact_identity, thbwiki_supported |
| 1441305 | bad_apple | Alstroemeria Records feat. nomico | Bad Apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 1441352 | bad_apple | nomico | Bad Apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist |
| 1445939 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat. nomico | graveyard | osu | chronicle_exact_identity, primary_official_derivative, primary_parent_artist, thbwiki_supported |
| 1456013 | bad_apple | Camellia | Bad Apple!! feat.nomico (Camellias Bad Psy!! Remix) | graveyard | mania | chronicle_exact_identity, primary_official_derivative |
| 1456721 | bad_apple | Masayoshi Minoshima ft. nomico | Bad Apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 1462518 | bad_apple | Nomico | Bad Apple | graveyard | osu | chronicle_exact_identity, primary_parent_artist |
| 1478246 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat. nomico | graveyard | osu | chronicle_exact_identity, explicit_game_source, primary_official_derivative, primary_parent_artist, thbwiki_supported |
| 1487818 | zun_original | ZUN | Hartmann's Youkai Girl | graveyard | osu | zun_exact_original |
| 1489682 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat. nomico (Camellia's "Bad Psy!!" Remix) | graveyard | mania,osu | chronicle_exact_identity, primary_official_derivative, primary_parent_artist |
| 1522278 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat. nomico | graveyard | mania | chronicle_exact_identity, primary_official_derivative, primary_parent_artist, thbwiki_supported |
| 1524126 | zun_original | ZUN | Reach for the Moon, Immortal Smoke | graveyard | mania | zun_exact_original |
| 1549988 | bad_apple | Nomico | Bad Apple!! feat.nomico (Camellias Bad Psy!! Remix) | graveyard | mania | chronicle_exact_identity, primary_official_derivative, primary_parent_artist |
| 1560057 | bad_apple | Masayoshi Minoshima ft. nomico | Bad Apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 1566803 | bad_apple | Nhato | Bad Apple!! feat.nomico (Nhato Remix) | graveyard | osu | chronicle_exact_identity, primary_official_derivative, thbwiki_supported |
| 1567934 | bad_apple | Masayoshi Minoshima ft nomico | Bad Apple!! | graveyard | mania | chronicle_exact_identity, primary_parent_artist |
| 1574689 | zun_original | Zun | Reach for the moon, immortal smoke | graveyard | mania | zun_exact_original |
| 1575656 | zun_original | ZUN | Septette for the Dead Princess | graveyard | osu | zun_exact_original |
| 1575821 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat. nomico (Camellia's "Bad Psy!!" Remix) | graveyard | osu | chronicle_exact_identity, explicit_game_source, primary_official_derivative, primary_parent_artist |
| 1576827 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat.nomico | graveyard | osu | chronicle_exact_identity, explicit_game_source, primary_official_derivative, primary_parent_artist |
| 1582298 | bad_apple | Alstroemeria Records | Bad Apple!! feat.nomico (Camellia's "Bad Psy" Remix) | graveyard | mania | chronicle_exact_identity, primary_official_derivative, primary_parent_artist, thbwiki_supported |
| 1585029 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat.nomico | graveyard | catch | chronicle_exact_identity, explicit_game_source, primary_official_derivative, primary_parent_artist, thbwiki_supported |
| 1653200 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat.nomico (Camellias Bad Psy!! Remix) | graveyard | osu | chronicle_exact_identity, explicit_game_source, primary_official_derivative, primary_parent_artist |
| 1672812 | bad_apple | masayoshi minoshima ft.nomico | bad apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 1691133 | bad_apple | Alstroemeria Records // nomico | Bad Apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist |
| 1729425 | bad_apple | Masayoshi Minoshima ft. nomico & Rodri's Trash Can | Bad Apple!! | graveyard | mania | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 1744498 | bad_apple | Masayaoshi Minoshima feat. nomico | Bad Apple | graveyard | osu | chronicle_exact_identity, primary_parent_artist |
| 1774663 | zun_original | ZUN | Septette for the Dead Princess | graveyard | taiko | zun_exact_original |
| 1787398 | zun_original | ZUN | Reach for the Moon, Immortal Smoke | graveyard | osu | zun_exact_original |
| 1788507 | bad_apple | Masayoshi Minoshima | Bad apple | graveyard | osu | chronicle_exact_identity, primary_parent_artist |
| 1792878 | zun_original | ZUN | Beloved Tomboyish Girl | graveyard | mania | zun_exact_original |
| 1805208 | bad_apple | Masayoshi Minoshima feat. nomico | Bad Apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 1805456 | zun_original | ZUN | U.N. Owen was Her? | graveyard | mania | zun_exact_original |
| 1806916 | zun_original | ZUN | U.N. Owen was Her? | graveyard | mania | zun_exact_original |
| 1819800 | zun_original | ZUN | U.N Owen was her? | graveyard | mania | zun_exact_original |
| 1820913 | bad_apple | Masayoshi minoshima feat. nomico | Bad Apple!! | graveyard | mania | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 1841883 | bad_apple | Masayoshi Minoshima | Bad Apple | graveyard | osu | chronicle_exact_identity, primary_parent_artist |
| 1842339 | bad_apple | Masayoshi Minoshima ft. nomico | Bad Apple!! | graveyard | mania | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 1843051 | bad_apple | Masayoshi Minoshima feat. nomico | Bad Apple!! | graveyard | osu | chronicle_exact_identity, explicit_game_source, primary_parent_artist, thbwiki_supported |
| 1853636 | zun_original | ZUN | U.N Owen Was Her | graveyard | osu | zun_exact_original |
| 1858024 | zun_original | ZUN | U.N. Owen was Her? | graveyard | catch,taiko | zun_exact_original |
| 1862037 | zun_original | ZUN | love colored master spark | graveyard | osu | zun_exact_original |
| 1869107 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat. nomico | graveyard | mania | chronicle_exact_identity, primary_official_derivative, primary_parent_artist, thbwiki_supported |
| 1871071 | bad_apple | Masayoshi Minoshima feat. nomico | Bad Apple! | graveyard | osu | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 1874077 | bad_apple | Masayoshi Minoshima ft. nomico | Bad Apple!! | graveyard | mania | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 1890039 | bad_apple | Masayoshi Minoshima feat. nomico | Bad Apple!! | graveyard | osu | chronicle_exact_identity, explicit_game_source, primary_parent_artist, thbwiki_supported |
| 1910893 | zun_original | ZUN | Septette for the Dead Princess | graveyard | osu | zun_exact_original |
| 1919371 | bad_apple | Masayoshi | Bad Apple! | graveyard | osu | chronicle_exact_identity, thbwiki_supported |
| 1931620 | zun_original | Zun | U.N. Owen Was Her? | graveyard | mania | zun_exact_original |
| 1931658 | bad_apple | Masayoshi Minoshima ft. nomico | Bad Apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 1934577 | bad_apple | Masayoshi Minoshima ft. nomico | Bad Apple!! | graveyard | osu | chronicle_exact_identity, explicit_game_source, primary_parent_artist, thbwiki_supported |
| 1936290 | bad_apple | Camellia | Bad Apple!! feat.nomico (Camellias Bad Psy!! Remix) | graveyard | mania | chronicle_exact_identity, explicit_game_source, primary_official_derivative |
| 1939010 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat. nomico | graveyard | osu | chronicle_exact_identity, primary_official_derivative, primary_parent_artist, thbwiki_supported |
| 1945278 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat. nomico (Camellia's "Bad Psy!!" Remix) | graveyard | taiko | chronicle_exact_identity, explicit_game_source, primary_official_derivative, primary_parent_artist |
| 1949284 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat. Nomico | graveyard | osu | chronicle_exact_identity, primary_official_derivative, primary_parent_artist, thbwiki_supported |
| 1951674 | zun_original | ZUN | Septette for the Dead Princess | graveyard | osu | zun_exact_original |
| 1959500 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat. nomico | graveyard | osu | chronicle_exact_identity, explicit_game_source, primary_official_derivative, primary_parent_artist, thbwiki_supported |
| 1961021 | zun_original | ZUN | Reach for the Moon ~ Immortal Smoke | graveyard | osu | zun_exact_original |
| 1962992 | bad_apple | Camellia | Bad Apple!! feat.nomico (Camellia's Bad Psy!! Remix) | graveyard | mania | chronicle_exact_identity, primary_official_derivative |
| 1971047 | zun_original | ZUN | Septette for the Dead Princess | graveyard | osu | zun_exact_original |
| 1973556 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat. nomico | graveyard | mania | chronicle_exact_identity, explicit_game_source, primary_official_derivative, primary_parent_artist, thbwiki_supported |
| 1983467 | bad_apple | nomico | Bad Apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 1987443 | bad_apple | Alstroemeria Records feat.nomico | Bad Apple!! | graveyard | mania | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 1991727 | bad_apple | Camellia | Bad Apple! feat. nomico (Camellia's Bad Psy!! Remix) | graveyard | mania | chronicle_exact_identity, primary_official_derivative |
| 1994571 | zun_original | ZUN | Hartmann's Youkai Girl | graveyard | osu | zun_exact_original |
| 1996118 | zun_original | ZUN | Septette for the Dead Princess | graveyard | osu | zun_exact_original |
| 1997997 | zun_original | ZUN | Necrofantasia | graveyard | osu | zun_exact_original |
| 2004446 | bad_apple | Alstroemeria Records feat. nomico | Bad Apple!! | graveyard | taiko | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 2009755 | zun_original | ZUN | Necrofantasia | graveyard | osu | zun_exact_original |
| 2011173 | zun_original | ZUN | Reach for the Moon, Immortal Smoke | graveyard | mania,osu | zun_exact_original |
| 2034469 | zun_original | ZUN | U.N Owen Was Her? | graveyard | osu | zun_exact_original |
| 2039842 | zun_original | ZUN | Hartmann's Youkai Girl | graveyard | mania | zun_exact_original |
| 2040542 | zun_original | ZUN | U.N. Owen Was Her? | graveyard | osu | zun_exact_original |
| 2045764 | bad_apple | Alstroemeria Records | Bad Apple!! | graveyard | mania | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 2046473 | bad_apple | Camellia | Bad Apple!! feat.nomico (Camellia's "Bad Psy" Remix) | graveyard | osu | chronicle_exact_identity, primary_official_derivative |
| 2057485 | bad_apple | Masayoshi Minoshima | Bad Apple! | graveyard | mania | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 2064738 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat.nomico (Camellias Bad Psy!! Remix) | graveyard | mania | chronicle_exact_identity, explicit_game_source, primary_official_derivative, primary_parent_artist |
| 2070023 | zun_original | ZUN | Necrofantasia | graveyard | osu | zun_exact_original |
| 2076587 | bad_apple | Demetori | Bad Apple!! ~ Death of A Bad Apple | graveyard | mania | chronicle_exact_identity, thbwiki_supported |
| 2108390 | bad_apple | Masayoshi Minoshima feat. nomico | Bad Apple!! | graveyard | osu | chronicle_exact_identity, explicit_game_source, primary_parent_artist, thbwiki_supported |
| 2113820 | bad_apple | Masayoshi Minoshima ft. nomico | Bad Apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist |
| 2128387 | zun_original | ZUN | Beloved Tomboyish Girl | graveyard | osu | zun_exact_original |
| 2133636 | zun_original | ZUN | Hartmann's Youkai Girl | graveyard | osu | zun_exact_original |
| 2139642 | zun_original | ZUN | U.N.owen was her? | graveyard | mania | zun_exact_original |
| 2160315 | zun_original | ZUN | Reach for the Moon, Immortal Smoke | graveyard | mania | zun_exact_original |
| 2175640 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat.nomico (Camellia's Bad Psy Remix) | graveyard | mania | chronicle_exact_identity, explicit_game_source, primary_official_derivative, primary_parent_artist |
| 2189581 | zun_original | ZUN | UN Owen Was Her | graveyard | mania | zun_exact_original |
| 2193054 | bad_apple | Alstroemerla Records/nomico | Bad apple!! | graveyard | mania | chronicle_exact_identity, primary_parent_artist |
| 2207358 | bad_apple | Masayoshi Minoshima feat. nomico | Bad Apple!! | graveyard | osu | chronicle_exact_identity, explicit_game_source, primary_parent_artist, thbwiki_supported |
| 2219245 | bad_apple | Camellia/nomico | Bad Apple!! feat.nomico (Camellia's "Bad Psy" Remix) | graveyard | mania | chronicle_exact_identity, primary_official_derivative, primary_parent_artist |
| 2220410 | zun_original | ZUN | Reach for the Moon, Immortal Smoke | graveyard | osu | zun_exact_original |
| 2222379 | bad_apple | Alstroemeria Records | Bad Apple!! feat. nomico (Camellia's "Bad Psy" Remix) | graveyard | mania | chronicle_exact_identity, primary_official_derivative, primary_parent_artist, thbwiki_supported |
| 2244341 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat. nomico | graveyard | osu | chronicle_exact_identity, explicit_game_source, primary_official_derivative, primary_parent_artist, thbwiki_supported |
| 2253850 | bad_apple | Masayoshi Minoshima feat. nomico | Bad Apple!! | graveyard | catch,mania,osu,taiko | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 2259816 | zun_original | ZUN | Necrofantasia | graveyard | mania | zun_exact_original |
| 2263312 | bad_apple | Masayoshi Minoshima ft. nomico | Bad Apple!! | graveyard | mania | chronicle_exact_identity, explicit_game_source, primary_parent_artist, thbwiki_supported |
| 2273119 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat.nomico (Camellia's "Bad Psy" Remix) | graveyard | mania | chronicle_exact_identity, primary_official_derivative, primary_parent_artist |
| 2277319 | zun_original | ZUN | Necrofantasia | graveyard | osu | zun_exact_original |
| 2287618 | zun_original | ZUN | Love-Colored Master Spark | graveyard | osu | zun_exact_original |
| 2290368 | zun_original | ZUN | Septette for the Dead Princess | graveyard | mania | zun_exact_original |
| 2297194 | zun_original | ZUN | U.N Owen Was Her? | graveyard | mania | zun_exact_original |
| 2300382 | bad_apple | Alstroemeria Records (feat.nomico) | BAD APPLE !! | graveyard | mania | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 2302726 | zun_original | ZUN | Beloved Tomboyish Girl | graveyard | mania | zun_exact_original |
| 2314565 | bad_apple | nomico | Bad Apple!! feat.nomico | graveyard | taiko | chronicle_exact_identity, primary_official_derivative, primary_parent_artist, thbwiki_supported |
| 2317303 | bad_apple | Masayoshi Minoshima | Bad Apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 2322401 | zun_original | ZUN | U.N. Owen Was Her? | graveyard | catch | zun_exact_original |
| 2329358 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat. nomico | graveyard | osu | chronicle_exact_identity, primary_official_derivative, primary_parent_artist, thbwiki_supported |
| 2339284 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat. nomico | graveyard | taiko | chronicle_exact_identity, primary_official_derivative, primary_parent_artist, thbwiki_supported |
| 2343980 | zun_original | Zun | U.N. owen was her? | graveyard | mania | zun_exact_original |
| 2355084 | bad_apple | Nomico | Bad Apple | graveyard | osu | chronicle_exact_identity, primary_parent_artist |
| 2356121 | zun_original | ZUN | Love-coloured Master Spark | graveyard | mania | zun_exact_original |
| 2362284 | zun_original | ZUN | Hartmann's Youkai Girl | graveyard | osu | zun_exact_original |
| 2384381 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat. nomico (Camellia's "Bad Psy!!" Remix) | graveyard | osu | chronicle_exact_identity, explicit_game_source, primary_official_derivative, primary_parent_artist |
| 2386391 | zun_original | ZUN | Hartmann's Youkai Girl | graveyard | mania | zun_exact_original |
| 2389261 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat. nomico (Camellia's "Bad Psy!!" Remix) | graveyard | catch | chronicle_exact_identity, explicit_game_source, primary_official_derivative, primary_parent_artist |
| 2399320 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat. nomico (Camellia's "Bad Psy!!" Remix) | graveyard | mania | chronicle_exact_identity, explicit_game_source, primary_official_derivative, primary_parent_artist |
| 2409030 | zun_original | ZUN | U.N. Owen Was Her? | graveyard | mania | zun_exact_original |
| 2419995 | zun_original | ZUN | Hartmann's Youkai Girl | graveyard | mania | zun_exact_original |
| 2423076 | bad_apple | Masayoshi Minoshima ft. nomico | Bad Apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 2426104 | bad_apple | Alstroemeria Records | Bad Apple!! | graveyard | mania | chronicle_exact_identity, primary_parent_artist |
| 2436793 | bad_apple | Masayoshi Minoshima ft. nomico | Bad Apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 2441474 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat. nomico (Camellia's "Bad Psy!!" Remix) | graveyard | mania | chronicle_exact_identity, explicit_game_source, primary_official_derivative, primary_parent_artist |
| 2451006 | bad_apple | Masayoshi Minoshima feat. Nomico | Bad Apple!! | graveyard | mania | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 2451719 | zun_original | ZUN | Hartmann's Youkai Girl | graveyard | osu | zun_exact_original |
| 2454880 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat.nomico (Camellia's "Bad Psy" Remix) | graveyard | mania | chronicle_exact_identity, explicit_game_source, primary_official_derivative, primary_parent_artist |
| 2462410 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat.nomico (Nhato Remix) | graveyard | mania | chronicle_exact_identity, primary_official_derivative, primary_parent_artist |
| 2471285 | zun_original | Zun | U.N. Owen was her? | graveyard | mania | zun_exact_original |
| 2472936 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat.nomico (Camellias Bad Psy!! Remix) | graveyard | taiko | chronicle_exact_identity, primary_official_derivative, primary_parent_artist |
| 2477639 | zun_original | ZUN | Reach for the moon Immortal smoke | graveyard | mania | zun_exact_original |
| 2482867 | zun_original | ZUN | U.N. Owen Was Her? | graveyard | osu | zun_exact_original |
| 2483636 | bad_apple | Masayoshi Minoshima feat. nomico | Bad Apple!! | graveyard | osu | chronicle_exact_identity, explicit_game_source, primary_parent_artist, thbwiki_supported |
| 2486299 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat. nomico | graveyard | taiko | chronicle_exact_identity, explicit_game_source, primary_official_derivative, primary_parent_artist, thbwiki_supported |
| 2491598 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat. nomico | graveyard | mania | chronicle_exact_identity, primary_official_derivative, primary_parent_artist, thbwiki_supported |
| 2494037 | zun_original | ZUN | Love-Colored Master Spark | graveyard | mania | zun_exact_original |
| 2500470 | bad_apple | nomico | Bad apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist |
| 2515393 | bad_apple | nomico/Nardis | Bad Apple!! feat.nomico(Nardis Remix) | graveyard | mania | chronicle_exact_identity, primary_official_derivative, primary_parent_artist |
| 2519010 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat. nomico (Camellia's "Bad Psy" Remix) | graveyard | mania | chronicle_exact_identity, primary_official_derivative, primary_parent_artist |
| 2536501 | bad_apple | Masayoshi Minoshima ft. nomico | Bad Apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist |
| 2541225 | bad_apple | ZUN, Camellia | Bad Apple!! feat.nomico (Camellia's "Bad Psy!!" Remix) | graveyard | mania | chronicle_exact_identity, primary_official_derivative |
| 2561623 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat.nomico(Camellia's "Bad Psy!!" Remix) | graveyard | mania | chronicle_exact_identity, primary_official_derivative, primary_parent_artist |
| 2563414 | bad_apple | Alstroemeria Records | Bad Apple!! feat.nomico (Nhato Remix) | graveyard | mania | chronicle_exact_identity, primary_official_derivative, primary_parent_artist |
| 2565117 | bad_apple | Masayoshi Minoshima | Bad Apple!! feat.nomico (Nhato Remix) | graveyard | osu | chronicle_exact_identity, explicit_game_source, primary_official_derivative, primary_parent_artist |
| 2573288 | bad_apple | Masayoshi Minoshima ft. nomico | Bad Apple!! | graveyard | mania | chronicle_exact_identity, primary_parent_artist |
| 2577835 | bad_apple | Masayoshi Minoshima ft. nomico | Bad Apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist |
| 2578129 | bad_apple | Masayoshi Minoshima feat. nomico | Bad Apple!! | graveyard | osu | chronicle_exact_identity, primary_parent_artist, thbwiki_supported |
| 2586468 | zun_original | ZUN | Necrofantasia | graveyard | mania | zun_exact_original |
| 2594168 | zun_original | ZUN | U.N. Owen Was Her? | graveyard | osu | zun_exact_original |
| 2594460 | bad_apple | Alstroemeria Records feat. | Bad Apple!! | graveyard | mania | chronicle_exact_identity, primary_parent_artist |
| 2600289 | bad_apple | Masayoshi Minoshima feat. nomico | Bad Apple!! | wip | osu | chronicle_exact_identity, primary_parent_artist |
| 2603026 | bad_apple | IOSYS | Bad Apple & Good Orange | wip | osu | chronicle_exact_identity, explicit_game_source |
| 2610365 | bad_apple | Alstroemeria Records | Bad Apple!! | wip | osu | chronicle_exact_identity, primary_parent_artist |

## Withheld boundary

- Bad Apple exact-composition candidates withheld by contradiction/secondary-evidence gate: **2**
  - `48319` — golden city factory - bad apple: `no_secondary_corroboration`
  - `20268` — IOSYS - Bad Apple & Good Orange: `no_secondary_corroboration`
- direct API/public-page failures withheld: **0**

Parent-artist-only Bad Apple search hits without an exact Arrangement Chronicle identity are intentionally excluded even when the artist is strongly associated with the work. This avoids admitting memes, unrelated edits, or loosely named mashups from artist identity alone.

## Integrity checks

- exact written new-ID set equals the **356** accepted IDs above;
- all **4438** pre-existing rows are field-for-field unchanged;
- every inserted row has `manual:verified`, a current `last_checked`, and source-backed Touhou kind/theme/game metadata;
- shard placement/order is delegated to `Catalog.save()`;
- the workflow runs `make check`, `make build`, and `git diff --check` before committing.
