# 竹取飛翔 ～ Lunatic Princess systematic search audit

Date: 2026-08-21

## Goal

Build a reproducible, conservative search corpus for osu! beatmaps derived from ZUN's `竹取飛翔 ～ Lunatic Princess`, then use the corpus only for discovery. A search hit is **not** acceptance: every missing beatmapset must be direct-refetched and matched back to a documented arrangement title/artist (or explicit original-theme metadata) before catalog inclusion.

## Ground truth

- Touhou Arrangement Chronicle original-song index: https://touhou.arrangement-chronicle.com/original_song/%E6%9D%B1%E6%96%B9%E6%B0%B8%E5%A4%9C%E6%8A%84/%E7%AB%B9%E5%8F%96%E9%A3%9B%E7%BF%94%E3%80%80%EF%BD%9E%20Lunatic%20Princess — currently reports 1,758 arrangement rows across 693 circles / 1,494 albums and explicitly ties each listed row to this original theme.
- Official Touhou Danmaku Kagura archive: https://danmaku.jp/archive/music/m032/ — explicitly identifies `Help me, ERINNNNNN!!` as an arrangement of `竹取飛翔 ～ Lunatic Princess`, with ZUN as original composer.
- DTXFiles.nmk official album page: https://miomiohosina.wixsite.com/dtxf-nmk/nmk-toho-best — explicitly identifies `竹取飛翔 ～ Lunatic Princess(Hardstyle)`, `split second`, and `sola` as arrangements of this original. This is especially important for the collision-prone title `sola`.

The corpus below is a **high-value searchable subset**, not a claim that the 1,758-entry arrangement universe has been exhaustively enumerated. Generic titles are always artist/circle-guarded in the osu! filtering step.

## Search corpus (103 title/artist tuples)

### Direct/original-title variants (10)

| Title | Artist/circle guard |
| --- | --- |
| `竹取飛翔 ～ Lunatic Princess` | `none; title itself is distinctive/direct` |
| `竹取飛翔` | `none; title itself is distinctive/direct` |
| `竹取飛翔 ～ the Lunatic Princess` | `dBu music` |
| `竹取飛翔 ～ lunatic princess` | `UI-70` |
| `竹取飛翔～lunatic princess` | `UI-70` |
| `竹取飛翔 ～ Lunatic Princess<Eternal Change>` | `efs` |
| `竹取飛翔 MIYABI Mix` | `Colorful Cube` |
| `竹取演舞` | `SOUND HOLIC` |
| `竹取飛翔 ～ Lunatic Princess(Hardstyle)` | `nmk` |
| `ちょっとおしゃれな竹取飛翔` | `RoundLoudness` |

### Alstroemeria Records (6)

| Title | Artist/circle guard |
| --- | --- |
| `Lunatic Princess` | `Alstroemeria Records` |
| `Lunatic Princess(alstroemeria remix)` | `Alstroemeria Records` |
| `Lunatic Princess feat.ayaka*` | `Alstroemeria Records` |
| `Moonlit Night` | `Alstroemeria Records` |
| `seashore on the moon` | `Alstroemeria Records` |
| `Deeper Than Your Eyes, Farther Than Platinum Moon` | `Alstroemeria Records` |

### Help me, ERINNNNNN!! family (22)

| Title | Artist/circle guard |
| --- | --- |
| `Help me, ERINNNNNN!!` | `none; title itself is distinctive/direct` |
| `Help me,ERINNNNNN!!` | `none; title itself is distinctive/direct` |
| `Help me ERINNNNNN!!` | `none; title itself is distinctive/direct` |
| `Help me, ERINNNNNN!! (SPEEDCORE MIX)` | `Cis-Trance` |
| `Help me, ERINNNNNN!!（NU STYLE MIX）` | `Cis-Trance` |
| `Help me, ERINNNNNN!! -SH Style-` | `KONAMI` |
| `Help me, ERINNNNNN!! (TOS Remix)` | `魂音泉` |
| `Help me, ERINNNNNN!! 森羅万象ver.` | `COOL&CREATE` |
| `Help me, ERINNNNNN!! 豚乙女ver.` | `COOL&CREATE` |
| `Help me, ERINNNNNN!!（Tsukasa Hyper Rave Remix）` | `COOL&CREATE` |
| `Help me, ERINNNNNN!!（ARMにぎにぎREMIX）` | `COOL&CREATE` |
| `Help me, ERINNNNNN!!～翔～` | `COOL&CREATE` |
| `Help me, ERINNNNNN!!（Eurobeat Mix）` | `COOL&CREATE` |
| `Help me, ERINNNNNN!! - ASAP` | `COOL&CREATE` |
| `Help me, ERINNNNNN!!（ALR Remix）` | `COOL&CREATE` |
| `Help me, ERINNNNNN!!（TUMENECO ver.）` | `COOL&CREATE` |
| `Help me, ERINNNNNN!! 少女理論観測所ver.` | `COOL&CREATE` |
| `Help me, ERINNNNNN!!（Cranky Remix 2018）` | `COOL&CREATE` |
| `Help me, ERINNNNNN!!（feat. ｙｔｒ）- TOS Remix` | `COOL&CREATE` |
| `まりおさんに贈るHelp me, ERINNNNNN!!` | `COOL&CREATE` |
| `Help me, ERINNNNNN!!（English ver.）` | `COOL&CREATE` |
| `Help me, あーりん！` | `イロドリミドリ` |

### Silver Forest / つるぺったん family (7)

| Title | Artist/circle guard |
| --- | --- |
| `つるぺったん` | `Silver Forest` |
| `つるぺったん sun3 Remix` | `Silver Forest` |
| `つるぺったん。` | `Silver Forest` |
| `初音ミクでつるぺったん` | `Silver Forest` |
| `Lunatic Beat` | `Silver Forest` |
| `Lunatic EURO` | `Silver Forest` |
| `フィーバーフィーバー` | `Silver Forest` |

### A-One (2)

| Title | Artist/circle guard |
| --- | --- |
| `BAMBOO DANCE` | `A-One` |
| `悠久の守人` | `A-One` |

### SOUND HOLIC (6)

| Title | Artist/circle guard |
| --- | --- |
| `Psy-Phone` | `SOUND HOLIC` |
| `Psy-Phone(REDALiCE Remix)` | `SOUND HOLIC` |
| `TSUKI NO KAKERA` | `SOUND HOLIC` |
| `blue moon Jazz～蒼月～` | `SOUND HOLIC` |
| `Lunatic Concerto～The Battle of Eternity～` | `SOUND HOLIC` |
| `逆襲のプリンセス` | `SOUND HOLIC` |

### EastNewSound (6)

| Title | Artist/circle guard |
| --- | --- |
| `Soaring princess` | `EastNewSound` |
| `きゅんきゅんたまらんいなばたん。` | `EastNewSound` |
| `stillness～死が二人を分かつまで～` | `EastNewSound` |
| `lunareclpse` | `EastNewSound` |
| `card format` | `EastNewSound` |
| `split second` | `EastNewSound` |

### FELT (3)

| Title | Artist/circle guard |
| --- | --- |
| `Sign` | `FELT` |
| `SINK` | `FELT` |
| `Under cloud` | `FELT` |

### Halozy (4)

| Title | Artist/circle guard |
| --- | --- |
| `Take to LIH is you` | `Halozy` |
| `T.R.Y Revolution` | `Halozy` |
| `It is so beautiful` | `Halozy` |
| `Kill DJ` | `Halozy` |

### nmk / DTXFiles.nmk (1)

| Title | Artist/circle guard |
| --- | --- |
| `sola` | `nmk` |

### Amateras Records (4)

| Title | Artist/circle guard |
| --- | --- |
| `無限のInnocence` | `Amateras Records` |
| `曖昧Never Ending` | `Amateras Records` |
| `Crazy Diamond` | `Amateras Records` |
| `Entrance to Moon` | `Amateras Records` |

### 豚乙女 (3)

| Title | Artist/circle guard |
| --- | --- |
| `囲い無き世は一期の月影` | `豚乙女` |
| `ふわ☆きら` | `豚乙女` |
| `狂人日記` | `豚乙女` |

### 凋叶棕 (6)

| Title | Artist/circle guard |
| --- | --- |
| `Grate Escapers` | `凋叶棕` |
| `devastator` | `凋叶棕` |
| `永遠なるサウンドスケープ` | `凋叶棕` |
| `until do us part` | `凋叶棕` |
| `永夜 「Imperishable Challengers」` | `凋叶棕` |
| `そして遙に至る` | `凋叶棕` |

### Other corroborated arrangements (23)

| Title | Artist/circle guard |
| --- | --- |
| `永遠と瞬息の放浪者` | `Yonder Voice` |
| `月まで何マイル` | `Liz Triangle` |
| `KilLove Fireproof!` | `暁Records` |
| `HOW DOES IF FEEL TO BE ALIVE?` | `CROW'SCLAW` |
| `触れられない物語` | `魂音泉` |
| `触れられない物語(Over the "MOON" Remix)` | `魂音泉` |
| `深読みレゾナンス` | `幽閉サテライト` |
| `千華繚乱` | `幽閉サテライト` |
| `満月の下で踊る` | `蒼天の雪` |
| `行列のできるえーりん診療所` | `IOSYS` |
| `きっともうはたらかない` | `IOSYS` |
| `2Dive into Shadow` | `LiLA'c Records` |
| `Dreaming Moon` | `DiGiTAL WiNG` |
| `Moonlit refrain` | `CielArc` |
| `Moon Paradise` | `ダシマキレコード` |
| `Flying Night` | `Under Reverse` |
| `Immortal Luna` | `White Wonderful Records` |
| `夢乃鳥症候群` | `SuganoMusic` |
| `MOON PHASE` | `IRON ATTACK!` |
| `Night after night` | `IRON ATTACK!` |
| `What's Your Deep Wish?` | `C-CLAYS` |
| `TLiNKLE` | `<echo>PROJECT` |
| `月夜物語` | `K2E†Cradle` |

## Filtering rules

1. Search all corpus tuples through osu! API v2 and record the query provenance for every returned beatmapset.
2. Normalize punctuation/case/whitespace for matching, but do not use fuzzy semantic guessing. Generic titles (`sola`, `Sign`, `SINK`, `Lunatic Princess`, etc.) require the documented artist/circle guard or equivalent explicit osu! source metadata.
3. Compare numeric beatmapset IDs against the current catalog before review; existing entries are coverage statistics, not new additions.
4. Direct-refetch every missing candidate from `/api/v2/beatmapsets/{id}`. Reject deleted/unresolvable sets and title/artist mismatches.
5. For acceptance, require either (a) explicit current osu! metadata tying the set to Touhou/Imperishable Night plus a corpus title match, or (b) exact documented arrangement-title + artist/circle correspondence to a reliable source above. Search-query membership alone is never verification.
6. Mixed/medley titles may be accepted only when the source document explicitly lists `竹取飛翔 ～ Lunatic Princess` among their originals and the osu! set matches the documented work.
7. Record false positives and ambiguous collisions in this audit instead of silently dropping them, so repeated searches do not re-litigate the same names.
