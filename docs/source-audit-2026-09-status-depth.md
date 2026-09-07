# Status-scoped Touhou discovery audit — 2026-09-07

## Decision

Add **250** beatmapsets missing from the current main catalog. Every row is addition-only and crossed the repository deterministic `verified` boundary from a concrete recognized Touhou game source in current osu! metadata.

## Why this pass exists

The normal weekly discovery searches the configured terms without an explicit status partition and caps meaningful changes. The previous wave-3 audit demonstrated that the long tail is overwhelmingly graveyard material. This pass therefore reuses the existing source/game queries but partitions the official osu! search by `graveyard`, `wip`, and `pending`, then paginates each bucket much deeper.

## Search breadth

- base catalog: **4794** beatmapsets
- strong configured queries: **76**
- status buckets: **3** (graveyard, wip, pending)
- query/status buckets attempted: **228**
- official osu! search pages fetched: **597**
- unique absent verified search hits: **7275**
- direct `/api/v2/beatmapsets/<id>` refetches attempted: **600**
- accepted after direct refetch: **600**
- provisional rows sent to THBWiki/TouhouDB provenance: **400**
- final rows after red/ambiguous/policy filtering: **250**
- positive external composition relations among final rows: **186**
- prior live-review identity mismatch explicitly withheld: **2473015**
- status distribution: **{"graveyard": 101, "pending": 94, "wip": 55}**
- mode coverage: **{"catch": 12, "mania": 51, "osu": 152, "taiko": 49}**

Search keyword membership was never sufficient. Search results were first classified from their current API object, then every shortlisted ID was fetched again from the direct beatmapset endpoint. External provenance contradictions/ambiguity were removed before the final set was locked. The following step runs the repository Deep Review, including a second API fetch plus the public beatmapset page for exact identity agreement.

## Accepted beatmapsets

| Beatmapset ID | Artist | Title | Source | Status | Modes | Provenance verdict |
| ---: | --- | --- | --- | --- | --- | --- |
| 100704 | ZUN | Boushitsu no Emotion | 東方心綺楼　～ Hopeless Masquerade. | graveyard | osu,taiko | supported |
| 103003 | Shibayan feat. yana | Fall in the Dark | 東方紅魔郷　～ the Embodiment of Scarlet Devil. | pending | taiko | supported |
| 108749 | ShibayanRecords feat. yana | Fall in the Dark | 東方紅魔郷　～ the Embodiment of Scarlet Devil. | graveyard | osu | supported |
| 126743 | senya | Kachou Fuugetsu | 東方花映塚　～ Phantasmagoria of Flower View | graveyard | osu | supported |
| 135378 | ZUN | Peaceful | 東方幻想郷　～ Lotus Land Story | graveyard | osu | supported |
| 176348 | ZUN | Eien no Mikkatenka | 弾幕アマノジャク　～ Impossible Spell Card. | graveyard | catch | supported |
| 358195 | COOL&CREATE | Saishuu Kichiku Imouto Flandre-S | 東方紅魔郷　～ the Embodiment of Scarlet Devil. | pending | taiko | unknown |
| 394576 | Akatsuki Records | WARNINGxWARNINGxWARNING | 東方紺珠伝 ～ Legacy of Lunatic Kingdom. | graveyard | osu | supported |
| 450895 | ZUN | The Rabbit Has Landed | Touhou 15 - Legacy of Lunatic Kingdom | graveyard | osu | supported |
| 500380 | Tama | Saigetsu (Midnight Moon Walker Remix) | 東方萃夢想 ～ Immaterial and Missing Power. | graveyard | osu | supported |
| 510620 | FELT | New World | 東方Project　～ Perfect Cherry Blossom | graveyard | osu | supported |
| 544875 | senya | Yoru no Hana ~Nagi~ | 東方花映塚　～ Phantasmagoria of Flower View. | graveyard | osu | supported |
| 563508 | Sakaue Nachi | Think of You | 東方幻想郷　～ Lotus Land Story | graveyard | taiko | supported |
| 612157 | Minase Mashiro | runaway(Halozy Mix) | 東方星蓮船　～ Undefined Fantastic Object. | graveyard | mania,osu,taiko | supported |
| 612299 | CROW'SCLAW | Legend Of The Great Gods | 東方神霊廟　～ Ten Desires. | graveyard | osu | supported |
| 637959 | Chata | Regression Memory | 東方星蓮船 ～ Undefined Fantastic Object | graveyard | mania | supported |
| 658921 | Kurokotei | Galaxy Collapse | 東方星蓮船　～ Undefined Fantastic Object. | graveyard | taiko | supported |
| 673287 | Nhato | Great Vengeance | 東方紺珠伝　～ Legacy of Lunatic Kingdom. | graveyard | osu | supported |
| 707602 | Pizuya's Cell | Nano Probe | 東方紺珠伝 〜 Legacy of Lunatic Kingdom. | graveyard | osu | supported |
| 708760 | ZUN | Hishin Matara ~ Hidden Star in All Seasons. | 東方天空璋　～ Hidden Star in Four Seasons. | graveyard | osu | supported |
| 716452 | Golden City Factory | Sleepless Night of the Eastern Country | 東方文花帖　～ Shoot the Bullet. | pending | osu | unknown |
| 725962 | Akiyama Uni | Touhou Hisouten | 東方緋想天　～ Scarlet Weather Rhapsody. | graveyard | taiko | supported |
| 765951 | ZUN | Eternal Spring Dream | 東方紺珠伝　～ Legacy of Lunatic Kingdom. | graveyard | mania | unknown |
| 769670 | wonder | bad strawberry | 東方幻想郷　～ Lotus Land Story, 東方夢時空　～ Phantasmagoria of Dim.Dream | graveyard | osu | supported |
| 781514 | MISTY RAIN | Gouon Catharsis | 東方星蓮船　～ Undefined Fantastic Object. | graveyard | taiko | supported |
| 784350 | Nanahira | Monosugoi Space Shuttle de Koishi ga Monosugoi Uta | 東方地霊殿　～ Subterranean Animism. | graveyard | osu | supported |
| 797830 | ZUN | Swordsman of a Distant Star | 東方靈異伝　～ Highly Responsive to Prayers | graveyard | osu | supported |
| 799002 | REDALiCE vs. aran | Sweet Requiem | 東方永夜抄　～ Imperishable Night. | graveyard | mania | supported |
| 830233 | Nanahira | Monosugoi Satori Gear de Reimu ga Monosugoi Uta | 東方地霊殿　～ Subterranean Animism. | graveyard | osu | supported |
| 842126 | Diao ye zong feat. Meramipop | Alice no Wasuremono | 東方怪綺談　～ Mystic Square. | graveyard | osu | supported |
| 850585 | Nanahira | Monosugoi Satori Gear de Reimu ga Monosugoi Uta | 東方地霊殿　～ Subterranean Animism. | graveyard | osu | supported |
| 857758 | FELT | crescent moon | 東方心綺楼 | graveyard | osu | supported |
| 859203 | IOSYS | DANZAI YAMAXANADU! | 東方花映塚　～ Phantasmagoria of Flower View. | graveyard | mania | supported |
| 869580 | ZUN | Yuumu ~ Inanimate Dream | 東方幻想郷　～ Lotus Land Story. | graveyard | osu | supported |
| 892168 | Diao Ye Zong feat. Meramipop | Downfalling Ideology | 東方輝針城　～ Double Dealing Character. | graveyard | osu | supported |
| 916554 | ZUN | Angel's Legend | Touhou - Highly Responsive to Prayers | graveyard | osu | supported |
| 924126 | RD-Sounds feat. Meramipop/nayuta | Shiten | 東方天空璋　～ Hidden Star in Four Seasons. | graveyard | osu | supported |
| 924440 | Ryu-5150 | Louder than steel | 東方夢時空　～ Phantasmagoria of Dim.Dream | graveyard | osu | supported |
| 937562 | Ranko | In the Black | 東方憑依華　～ Antinomy of Common Flowers. | graveyard | osu | supported |
| 970291 | Demetori | Bad Apple!! ~ Death of A Bad Apple | 東方幻想郷　～ Lotus Land Story. | graveyard | taiko | supported |
| 972171 | ZUN | Jelly Stone | 東方鬼形獣　～ Wily Beast and Weakest Creature. | graveyard | osu | supported |
| 973256 | DJ Technetium ft Ayumi Nomiya | Just the Death of Us | 東方花映塚～Phantasmagoria of Flower View | graveyard | mania | supported |
| 986613 | Diao Ye Zong feat. nayuta | Closed Rain | 東方紅魔郷　～ the Embodiment of Scarlet Devil. | graveyard | osu | supported |
| 993487 | UNDEAD CORPORATION | Flowering Night Fever | 東方花映塚　～ Phantasmagoria of Flower View. | graveyard | mania | supported |
| 995301 | ZUN | Eien No Shunmu | 東方紺珠伝　～ Legacy of Lunatic Kingdom. | graveyard | osu | supported |
| 997574 | ZUN | Nemureru Kyoufu ~ Sleeping Terror | 東方幻想郷　～ Lotus Land Story | graveyard | taiko | supported |
| 1016604 | Rin | Eientewi set 17 ~ Eastern Youkai Beauty | 東方永夜抄　～ Imperishable Night. | graveyard | osu | supported |
| 1019750 | ZUN | Jelly stone | 東方鬼形獣　～ Wily Beast and Weakest Creature. | graveyard | osu | supported |
| 1038745 | ZUN | Kamigami ga Koishita Gensoukyou | 東方風神録　～ Mountain of Faith. | graveyard | osu | supported |
| 1041793 | Akatsuki Records x Liz Triangle | who killed U.N.Owen | 東方紅魔郷　～ the Embodiment of Scarlet Devil. | graveyard | osu | supported |
| 1056083 | ZUN | Electric Heritage | 東方鬼形獣　～ Wily Beast and Weakest Creature. | graveyard | mania | supported |
| 1056654 | RichaadEB | Pierrot of the Star-Spangled Banner | 東方紺珠伝　～ Legacy of Lunatic Kingdom | graveyard | osu | supported |
| 1059154 | Ryu5150 | Beyond the Shine | 東方夢時空　～ Imperishable Night | graveyard | osu | supported |
| 1061413 | ZUN | Haru no Minato ni | 東方星蓮船　～ Undefined Fantastic Object. | graveyard | catch | supported |
| 1081118 | Shinra-Bansho /kaztora | Happiness Egoist | 東方花映塚　～ Phantasmagoria of Flower View | graveyard | osu | supported |
| 1082167 | Halozy | Heart of Night | 東方花映塚　～ Phantasmagoria of Flower View. | graveyard | taiko | supported |
| 1092965 | UNDEAD CORPORATION | Flowering Night Fever | 東方花映塚　～ Phantasmagoria of Flower View. | graveyard | osu,taiko | supported |
| 1097827 | ZUN | Kamigami ga koishita gensoukyou | 東方風神録　～ Mountain of Faith. | graveyard | mania | supported |
| 1100988 | REDALiCE & aran | Sweet Requiem | 東方永夜抄　～ Imperishable Night. | graveyard | osu | supported |
| 1104667 | Akatsuki Records | HANIPAGANDA | 東方鬼形獣　～ Wily Beast and Weakest Creature. | graveyard | taiko | supported |
| 1106327 | KISIDA KYODAN & THE AKEBOSI ROCKETS | YU-MU | 東方幻想郷　～ Lotus Land Story | wip | osu | supported |
| 1112441 | Diao ye zong feat. Meramipop | Shinkirou | 東方心綺楼 ～ Hopeless Masquerade. | graveyard | osu | supported |
| 1116436 | FELT | Lost My Way | 東方神霊廟　～ Ten Desires. | graveyard | osu | supported |
| 1119057 | Morimori Atsushi | Tits or get the fuck out!! | 東方神霊廟 〜 Ten Desires. | graveyard | taiko | supported |
| 1179555 | FELT | COLORS | 東方花映塚　～ Phantasmagoria of Flower View. | pending | osu | supported |
| 1182749 | Ayaponzu* | Justice Monster | 東方花映塚　～ Phantasmagoria of Flower View. | graveyard | osu | supported |
| 1226245 | UNDEAD CORPORATION | Ghost in Starlight | 東方神霊廟　～ Ten Desires. | wip | taiko | supported |
| 1264551 | Akiyama Uni | Touhou Hisouten | 東方緋想天　～ Scarlet Weather Rhapsody | graveyard | osu | supported |
| 1267723 | RD-Sounds feat. Meramipop | Sono Tadashiki Kotoba no Moto ni | 東方花映塚　～ Phantasmagoria of Flower View. | graveyard | taiko | supported |
| 1285175 | UNDEAD CORPORATION | Necromanticism | 東方妖々夢　～ Perfect Cherry Blossom. | graveyard | osu | supported |
| 1292138 | FELT | Dream in the Night | 東方星蓮船　～ Undefined Fantastic Object | graveyard | osu | supported |
| 1296248 | Thousand Leaves | Temptation | 東方怪綺談　～ Mystic Square | graveyard | osu | supported |
| 1314617 | FELT | crescent moon | 東方心綺楼　～ Hopeless Masquerade | graveyard | osu | supported |
| 1324886 | ZUN | Fall of Fall ~ Akimeku Taki | 東方風神録 ~ Mountain of Faith. | graveyard | osu | supported |
| 1390960 | Diao Ye Zong feat. Meramipop | Sono Tadashiki Kotoba no Moto ni | 東方花映塚　～ Phantasmagoria of Flower View. | graveyard | osu | supported |
| 1404046 | sun3 | Meikai Kikou | 東方花映塚　～ Phantasmagoria of Flower View. | graveyard | osu | supported |
| 1420908 | Akatsuki Records | HANIPAGANDA | 東方鬼形獣　〜 Wily Beast and Weakest Creature. | graveyard | mania | supported |
| 1455638 | ZUN | Sado no Futatsuiwa | 東方神霊廟　～ Ten Desires. | graveyard | taiko | supported |
| 1504220 | UNDEAD CORPORATION | Flowering Night Fever | 東方花映塚　～ Phantasmagoria of Flower View. | graveyard | mania | supported |
| 1521624 | AkatsukiRecords | Necromantic | 東方神霊廟　～ Ten Desires. | graveyard | mania | supported |
| 1529751 | xi | Shoujo Kisoukyoku ~ Speed Battle | 東方Project (東方永夜抄 ～ Imperishable Night.) | graveyard | mania | supported |
| 1531274 | Akatsuki Records | HELLOHELL | 東方紺珠伝　～ Legacy of Lunatic Kingdom | graveyard | osu | unknown |
| 1621910 | ZUN | Nemureru Kyoufu ~ Sleeping Terror | 東方幻想郷　～ Lotus Land Story | graveyard | osu | supported |
| 1627491 | A-One feat. Hanatan | Break The Hierarchie | 東方輝針城　～ Double Dealing Character. | pending | osu | supported |
| 1700628 | t=NODE | Four Seasons | 東方花映塚　～ Phantasmagoria of Flower View. | graveyard | mania | supported |
| 1708803 | ZUN | Hoshi no Utsuwa ~ Casket of Star | 東方幻想郷　～ Lotus Land Story | graveyard | osu | supported |
| 1779853 | Alstroemeria Records feat. nomico | The Last Judgement | 東方怪綺談　～ Mystic Square | graveyard | mania | supported |
| 1797402 | Vaguedge Dies For Dies Irae | Flowering Afterlife | 東方花映塚　～ Phantasmagoria of Flower View. | wip | osu | supported |
| 1834528 | Hanatan | KIRISAME MAGIC | 東方花映塚　～ Phantasmagoria of Flower View. | graveyard | mania | supported |
| 1861318 | ZUN | Mystic Oriental Dream ~ Ancient Temple | 東方妖々夢　～ Perfect Cherry Blossom | graveyard | mania | supported |
| 1870597 | BUTAOTOME | Tanoshii Sensou no Uta | 妖精大戦争　～ 東方三月精. | pending | osu | unknown |
| 1927531 | Diao Ye Zong feat. Meramipop | Saifu 'Kamiasobi no Uta' | 東方風神録　～ Mountain of Faith. | pending | catch | unknown |
| 1929732 | Demetori | Yuuga ni Sakase, Sumizome no Sakura ~ The Harm of Coming into Existence | 東方妖々夢　～ Perfect Cherry Blossom. | wip | osu | unknown |
| 1954411 | BUTAOTOME | Wai ~Y~ | 東方神霊廟 〜 Ten Desires. | wip | osu | unknown |
| 2008844 | Demetori | Yuuga ni Sakase, Sumizome no Sakura ~ Re:The Harm of Coming into Existence | 東方妖々夢　～ Perfect Cherry Blossom. | pending | osu | unknown |
| 2010758 | ayaponzu* feat. beatMARIO | INTERNET SURVIVOR | 東方紅魔郷　～ the Embodiment of Scarlet Devil. | graveyard | osu | supported |
| 2035376 | UNDEAD CORPORATION | Flowering Night Fever | 東方花映塚　～ Phantasmagoria of Flower View. | graveyard | mania | supported |
| 2044793 | ZUN | Kyuuketsukaijuu Chupacabra | 東方獣王園　〜 Unfinished Dream of All Living Ghost. | graveyard | osu | supported |
| 2051668 | IOSYS | Osaisen <3 Choudai - Nonstop NEW RICH shrine mix - | 東方幻想郷　～ Lotus Land Story | pending | osu,taiko | unknown |
| 2069033 | ZUN | Otogi no Kuni no Onigashima ~ Missing Power | 東方萃夢想　～ Immaterial and Missing Power. | graveyard | osu | supported |
| 2091805 | Mayumi Morinaga | Boutokuteki Sentaku no Alegria | 東方紅魔郷　～ the Embodiment of Scarlet Devil. | graveyard | osu | supported |
| 2115591 | Sakaue Nachi | Crazy Hot | 妖精大戦争　～ 東方三月精 | pending | osu | supported |
| 2145686 | Foreground Eclipse | Vermillion Halo | 東方花映塚　～ Phantasmagoria of Flower View. | pending | taiko | supported |
| 2153191 | Unlucky Morpheus x UNDEAD CORPORATION | You're Better Off Alive | 東方花映塚　～ Phantasmagoria of Flower View. | pending | mania | supported |
| 2158351 | Kurokotei | Galaxy Collapse | 東方星蓮船　～ Undefined Fantastic Object. | pending | mania | supported |
| 2193609 | beatMARIO | Help me, ERINNNNNN!! | 東方永夜抄　～ Imperishable Night. | graveyard | osu | supported |
| 2214938 | ZUN | Crimson Belvedere ~ Eastern Dream... | 東方紅魔郷　～ the Embodiment of Scarlet Devil. | graveyard | osu | supported |
| 2243210 | Foreground Eclipse | Fall Of Tears | 東方風神録　～ Mountain of Faith. | pending | osu | supported |
| 2245305 | beatMARIO x MARON | Chou Saishuu Kichiku Imouto Flandre S | 東方紅魔郷 〜 the Embodiment of Scarlet Devil. | graveyard | mania | supported |
| 2246796 | ZUN | Kokyou no Hoshi ga Utsuru Umi | 東方紺珠伝 ～ Legacy of Lunatic Kingdom | graveyard | osu | supported |
| 2267090 | FELT | IN THE RAIN | 東方花映塚　～ Phantasmagoria of Flower View. | graveyard | osu | supported |
| 2281495 | Halozy | Don't let you down | 東方神霊廟　～ Ten Desires. | wip | osu | supported |
| 2296737 | Rabbit House | Lunatic Nightmare | 東方永夜抄　～ Imperishable Night. | pending | taiko | supported |
| 2340115 | Iron Attack! | Remotely Combat | 東方地霊殿　～ Subterranean Animism. | wip | osu | supported |
| 2342569 | ShinRa-Bansho | Maid no Kokoro ha Ayatsuri Doll | 東方花映塚　～ Phantasmagoria of Flower View. | pending | osu | unknown |
| 2342585 | Halozy feat. Nanahira | Monosugoi Kuruttoru Flan-chan ga Monosugoi Uta | 東方紅魔郷　～ the Embodiment of Scarlet Devil | pending | osu | unknown |
| 2349137 | ZUN | Anata no Machi no Kaijiken | ダブルスポイラー　～ 東方文花帖 | graveyard | catch | supported |
| 2355444 | UNDEAD CORPORATION | The Empress | 東方紅魔郷　～ the Embodiment of Scarlet Devil. | pending | osu | supported |
| 2359604 | UNDEAD CORPORATION | Flowering Night Fever | 東方花映塚　～ Phantasmagoria of Flower View. | graveyard | mania | supported |
| 2360453 | xi-on | Solar Sect of Mystic Wisdom ~ Nuclear Fusion | 東方地霊殿　～ Subterranean Animism. | wip | osu,taiko | unknown |
| 2369358 | Sawawa | Warm and fluffy | 東方鬼形獣　～ Wily Beast and Weakest Creature. | pending | taiko | supported |
| 2381906 | Holmgang Ov Gensokyo | Forgo Thy Flesh (Feat. Ticafr) | 東方靈異伝　～ Highly Responsive to Prayers | pending | osu | unknown |
| 2392406 | Kurokotei | Galaxy Collapse | 東方星蓮船　～ Undefined Fantastic Object. | graveyard | osu | supported |
| 2416603 | Akatsuki Records | KAPPAYAPPA | 東方虹龍洞 ～ Unconnected Marketeers. | pending | osu | supported |
| 2425274 | FELT | Lost in the Abyss | 東方地霊殿　～ Subterranean Animism. | pending | taiko | supported |
| 2433674 | Akiyama Uni | Touhou Hisouten | 東方緋想天　～ Scarlet Weather Rhapsody. | graveyard | osu | supported |
| 2440791 | ShinRa-Bansho | Wish a Shooting Star | 東方永夜抄　～ Imperishable Night. | pending | osu | supported |
| 2449102 | Diao Ye Zong | Sabotage ni Tamashii o Kakete | 東方花映塚　～ Phantasmagoria of Flower View. | wip | osu | unknown |
| 2449939 | katikatiyama | Yokubou no Uta | 東方神霊廟　～ Ten Desires. | pending | osu | supported |
| 2458733 | ZUN | Hokkai no Hi | 東方星蓮船　～ Undefined Fantastic Object. | graveyard | osu | supported |
| 2464420 | Sawawa | Jet Fenrir | 東方風神録　～ Mountain of Faith. | pending | taiko | supported |
| 2478023 | Halozy | Paranoid Lost | 東方風神録　～ Mountain of Faith. | wip | osu | supported |
| 2483067 | Kurokotei | Galaxy Collapse | 東方星蓮船　～ Undefined Fantastic Object. | graveyard | mania,osu | supported |
| 2483808 | FELT | Sky Gate | 東方花映塚　～ Phantasmagoria of Flower View. | pending | osu | supported |
| 2487222 | ZUN | Civilization of Magic | 東方靈異伝　～ Highly Responsive to Prayers. | graveyard | osu | supported |
| 2489978 | UNDEAD CORPORATION | Embraced by the Flame | 東方地霊殿　～ Subterranean Animism. | pending | mania | unknown |
| 2493682 | sumijun feat. Minase Mashiro | runaway(Halozy Mix) | 東方星蓮船　～ Undefined Fantastic Object | pending | mania | supported |
| 2504209 | Demetori | Kagayaku Hari no Kobito-zoku ~ Counter-Attack of the Weak | 東方輝針城　～ Double Dealing Character. | pending | osu | unknown |
| 2507183 | Unlucky Morpheus | Danzai wa Amaneku Ningen no Moto ni | 東方風神録　～ Mountain of Faith. | wip | taiko | supported |
| 2511055 | Demetori | Crazy Backup Dancers ~ Orgy of the Dead | 東方天空璋　～ Hidden Star in Four Seasons. | pending | osu | unknown |
| 2512037 | Komiya Mao | (can you) understand me? (cut ver.) | 東方輝針城　～ Double Dealing Character. | pending | osu | unknown |
| 2517567 | ZUN | Yuuga Ni Sakase, Sumizome No Sakura ~ Border of Life & Border of Life | 東方妖々夢　～ Perfect Cherry Blossom. | wip | osu | unknown |
| 2519818 | Xi | Shoujo Kisoukyoku ~ Speed Battle | 東方永夜抄　～ Imperishable Night. | pending | mania | supported |
| 2526063 | ShinRa-Bansho | Itazura Sensation | 東方紅魔郷　～ the Embodiment of Scarlet Devil. | pending | osu | supported |
| 2526457 | ZUN | Illusionary Night ~ Ghostly Eyes | 東方永夜抄　～ Imperishable Night. | wip | osu | supported |
| 2529669 | FELT | Vagueness & JOURNEY | 東方緋想天　～ Scarlet Weather Rhapsody | pending | osu | unknown |
| 2530423 | Demetori | Peaceful Romancer ~ It's Better To Burn Out Than To Fade Away | 東方怪綺談　～ Mystic Square. | pending | mania | supported |
| 2536200 | Demetori | Crazy Backup Dancers ~ Orgy of the Dead | 東方天空璋　～ Hidden Star in Four Seasons. | pending | osu | unknown |
| 2537952 | BLANKFIELD | Flowering Game Night | 東方花映塚　～ Phantasmagoria of Flower View. | pending | osu | supported |
| 2539197 | Noah | Necrofantasia | 東方妖々夢　～ Perfect Cherry Blossom. | pending | osu | unknown |
| 2539457 | ShinRa-Bansho | Uchouten Dreamers | 東方緋想天　～ Scarlet Weather Rhapsody | wip | mania | supported |
| 2546089 | Reirou no Hydrangea | Izayoi, Toki o Tomete | 東方花映塚　～ Phantasmagoria of Flower View. | pending | taiko | unknown |
| 2546092 | Demetori | Shoujo ga Mita Nihon no Genfuukei ~ Dance of puNDarika | 東方風神録　～ Mountain of Faith. | wip | osu | unknown |
| 2546680 | Akiyama Uni | Touhou Hisouten | 東方緋想天　～ Scarlet Weather Rhapsody | graveyard | osu | supported |
| 2550054 | LeaF | Calamity Fortune | 東方風神録　～ Mountain of Faith. | pending | catch | supported |
| 2564212 | AQUAELIE | Rokujuu Nenme no Shinsoku Saiban ~ Rapidity is a justice | 東方花映塚　～ Phantasmagoria of Flower View. | pending | taiko | unknown |
| 2568837 | DJ Nanasaki | Unorthodox Red | 東方紅魔郷　～ the Embodiment of Scarlet Devil. | pending | taiko | supported |
| 2571607 | ShinRa-Bansho | Dynamite | 東方虹龍洞　～ Unconnected Marketeers | wip | osu | supported |
| 2575641 | KISIDA KYODAN & THE AKEBOSI ROCKETS | ANCIENT FLOWER (CUT VER.) | 東方妖々夢　～ Perfect Cherry Blossom. | wip | osu | unknown |
| 2581203 | Demetori | Yuuga ni Sakase, Sumizome no Sakura ~ Re:The Harm of Coming into Existence | 東方妖々夢　～ Perfect Cherry Blossom. | pending | osu | unknown |
| 2582380 | Halozy | eliminate anthem | 東方紅魔郷　～ the Embodiment of Scarlet Devil. | wip | osu | supported |
| 2582814 | ZUN | Gouka Mantle | 東方地霊殿　～ Subterranean Animism. | graveyard | osu | supported |
| 2585516 | Kurokotei | Scattered Faith | 東方星蓮船　〜 Undefined Fantastic Object. サウンドトラック | pending | mania | supported |
| 2585679 | Shinra-Bansho | Kyoukyou no Fortunate Polka | 東方天空璋　～ Hidden Star in Four Seasons. | pending | catch | unknown |
| 2587945 | Halozy feat. Nanahira | Monosugoi Kuruttoru Flan-chan ga Monosugoi Uta | 東方紅魔郷　～ the Embodiment of Scarlet Devil | pending | osu | unknown |
| 2588376 | -45 | Crimsonic dimension | 東方怪綺談　～ Mystic Square | pending | osu | supported |
| 2589413 | ZUN | Flowering Night | 東方花映塚　～ Phantasmagoria of Flower View | pending | osu | unknown |
| 2591405 | Demetori | Koyoi wa Hyouitsu na Egoist ~ Ego, Schizoid, Beat. | 東方憑依華　～ Antinomy of Common Flowers. | wip | osu | unknown |
| 2593229 | LeaF | Wizdomiot (extended ver.) | 東方地霊殿　～ Subterranean Animism. | wip | osu | unknown |
| 2594637 | ZUN | Shinkou wa Hakanaki Ningen no Tame ni | 東方風神録　～ Mountain of Faith. | wip | osu | supported |
| 2594740 | ryu5150 | Louder than steel | 東方夢時空　～ Phantasmagoria of Dim.Dream | pending | taiko | supported |
| 2597268 | Demetori | Pure Furies ~ Vengeance is Mine | 東方紺珠伝　～ Legacy of Lunatic Kingdom. | pending | catch,osu | unknown |
| 2597631 | Various Artists | Dan ~ REFORM ~ Touhou Map Pack | 東方紅魔郷　～ the Embodiment of Scarlet Devil. | pending | mania | unknown |
| 2598514 | Adust Rain | Joker's Cranberrybox | 東方紅魔郷　～ the Embodiment of Scarlet Devil. | pending | taiko | supported |
| 2598638 | Adust Rain | EViL DANCE | 東方風神録 〜 Mountain of Faith. | wip | osu | supported |
| 2598664 | Rin | Moriya set 00 ReEdit ~ Fuuin Sareshi Kamigami | 東方風神録　～ Mountain of Faith. | pending | catch,mania,osu,taiko | unknown |
| 2598673 | YaboiMatoi | Dark Side of Fate | 東方風神録　～ Mountain of Faith. | wip | osu | supported |
| 2599607 | Yuuhei Satellite feat. senya | Paranoia no Umi | 弾幕アマノジャク　～ Impossible Spell Card. | wip | osu | supported |
| 2600331 | Adust Rain | TRAUMATIC SYNDROME -Lenboxx Remix- | 東方地霊殿　～ Subterranean Animism. | wip | taiko | supported |
| 2600943 | UNDEAD CORPORATION | Everything will freeze | 東方花映塚　～ Phantasmagoria of Flower View. | pending | mania | supported |
| 2600955 | Rin | Daishibyo set 15 ~ Jinja no Atarashii Kaze | 東方神霊廟　～ Ten Desires. | pending | catch,mania,osu,taiko | unknown |
| 2601009 | maritumix | 514 | 東方地靈殿　～ Subterranean Animism. | pending | taiko | supported |
| 2601046 | beatMARIO | Help me, ERINNNNNN!! | 東方永夜抄　～ Imperishable Night. | pending | catch | supported |
| 2601612 | REDALiCE & aran | Sweet Requiem | 東方永夜抄　～ Imperishable Night. | wip | mania | supported |
| 2601725 | 3L | Tiny Little Adiantum (deadman's "Omae Wa Mou" remix) | 東方花映塚　～ Phantasmagoria of Flower View. | wip | osu | unknown |
| 2601979 | UNDEAD CORPORATION | Bloodstained Nocturne | Touhou Koumakyou ~ Embodiment of Scarlet Devil | pending | mania | supported |
| 2602110 | YaboiMatoi | We Are Japanese Goblin | 東方萃夢想　～ Immaterial and Missing Power. | pending | mania | supported |
| 2602352 | sawawa | Fire in the Phoenix | 東方永夜抄　～ Imperishable Night. | wip | mania | supported |
| 2602354 | sawawa | Koishi Circulation | 東方地霊殿　～ Subterranean Animism. | wip | mania | supported |
| 2602612 | Demetori | Kourou ~ Eastern Dream | 東方紅魔郷　～ the Embodiment of Scarlet Devil. | wip | osu | unknown |
| 2602685 | Unlucky Morpheus | FAITH | 東方風神録　～ Mountain of Faith. | pending | osu | supported |
| 2602711 | ZUN | Crazy Backup Dancers | 東方天空璋　～ Hidden Star in Four Seasons | wip | mania | supported |
| 2603559 | YaboiMatoi | Native Faith | 東方風神録 ～ Mountain of Faith. | pending | taiko | supported |
| 2603675 | IOSYS | Trauma Saimin Shoujo Satori! | 東方地霊殿　～ Subterranean Animism. | wip | mania | supported |
| 2603845 | EmoCosine & RiraN | Goddess Destroyed U | 東方紅魔郷　～ the Embodiment of Scarlet Devil | pending | osu | supported |
| 2604106 | Yuuhei Satellite feat. sroa | Tasogare Moyou no Kanjouron | 東方妖々夢　～ Perfect Cherry Blossom. | wip | osu | unknown |
| 2604116 | Xi | Rokujuu-nen Me no Shinsoku Saiban ~ Rapidity is a justice (Cut Ver.) | 東方花映塚　～ Phantasmagoria of Flower View. | wip | osu | unknown |
| 2604124 | ryu5150 | Last remote | 東方地霊殿　～ Subterranean Animism. | pending | osu | supported |
| 2604169 | Frozen Starfall | Unexplained (feat. Milkychan) | 東方風神録　～ Mountain of Faith. | wip | mania | unknown |
| 2604279 | Silver Forest | Tsurupettan (Game Ver.) | 東方永夜抄　～ Imperishable Night. | pending | catch | unknown |
| 2604657 | Demetori | Hishin Matara ~ Four seasons where Starless disappeared. | 東方天空璋　～ Hidden Star in Four Seasons. | pending | osu | unknown |
| 2604968 | Frozen Starfall | LUNARTANZ (Nhato Remix) | 東方永夜抄　～ Imperishable Night | wip | osu | supported |
| 2604996 | Halozy | Kikoku Doukoku Jigokuraku | 東方地霊殿　～ Subterranean Animism. | pending | taiko | unknown |
| 2605032 | ZUN | Hartmann no Youkai Shoujo | 東方地霊殿　～ Subterranean Animism. | wip | catch | supported |
| 2605068 | UNDEAD CORPORATION | Malicious Maggots | 東方紅魔郷　～ the Embodiment of Scarlet Devil | pending | mania | supported |
| 2605203 | Demetori | Youkai no Yama ~ Mysterious Mountain | 東方風神録　～ Mountain of Faith. | pending | taiko | unknown |
| 2605353 | ShinRa-Bansho | Not Good World | 東方星蓮船　～ Undefined Fantastic Object. | pending | taiko | unknown |
| 2605396 | Register6 | Houjou no Yume | 東方紅魔郷　～ the Embodiment of Scarlet Devil. | wip | osu | unknown |
| 2605568 | Shinigiwa Satellite feat. Meramipop | Seijaku Last Dance | 東方地霊殿 ～ Subterranean Animism. | wip | osu | supported |
| 2605577 | Halozy | Viva Evolution Introduction | 東方神霊廟　～ Ten Desires. | pending | taiko | supported |
| 2606458 | Para Dot. | Norinori Banki-chan | 東方輝針城　〜 Double Dealing Character. サウンドトラック | pending | taiko | unknown |
| 2606525 | SEPHID feat. darkxixin | Fu Xiang Di Xin De Luo Ri Liu Hao ~ Little Raven | 東方地霊殿　～ Subterranean Animism. | wip | taiko | unknown |
| 2606528 | YaboiMatoi | We Are Japanese Goblin | 東方萃夢想　～ Immaterial and Missing Power. | pending | mania | supported |
| 2607031 | COOL&CREATE feat. BeatMARIO & MARON | Matsuyoi Nightbug | 東方永夜抄　～Imperishable Night | wip | mania | supported |
| 2607080 | Akatsuki Records | HISTORIAN | 東方永夜抄　～ Imperishable Night | pending | osu | unknown |
| 2607088 | Akatsuki Records | AahnUNKNOWN | 東方星蓮船 ～ Undefined Fantastic Object. | wip | osu | unknown |
| 2607191 | ZUN | Ryokugan no Jealousy | 東方地霊殿　～ Subterranean Animism. | wip | osu | supported |
| 2607208 | komasy | the primal scene of hyperflip the girl saw | 東方風神録　～ Mountain of Faith. | pending | mania | unknown |
| 2607285 | ryu5150 | Glow on the Sky | 東方怪綺談　～ Mystic Square | pending | taiko | supported |
| 2607319 | BLANKFIELD | Voyage | 東方永夜抄　～ Imperishable Night. | pending | mania | supported |
| 2607791 | Akatsuki Records | LOVE LUCIFERIN | 東方永夜抄　～ Imperishable Night | wip | osu | supported |
| 2607895 | Shibayan feat. nachi | Que ela vem | 東方紅魔郷　～ the Embodiment of Scarlet Devil. | pending | osu | supported |
| 2608040 | FELT | Runway Drive | 東方永夜抄　～ Imperishable Night. | pending | osu | supported |
| 2608458 | senya | Yowamushi Vampire | 東方紅魔郷　～ the Embodiment of Scarlet Devil. | pending | taiko | supported |
| 2608571 | Hanaya | Realize in Death | 東方封魔録　～ the Story of Eastern Wonderland | wip | mania | supported |
| 2608686 | Unlucky Morpheus | BPM210 no Shanghai Alice (Instrumental) | 東方紅魔郷　～ the Embodiment of Scarlet Devil. | wip | osu | unknown |
| 2608734 | Liz Triangle | past lover | 東方輝針城　～ Double Dealing Character. | pending | taiko | supported |
| 2608977 | KISIDA KYODAN & THE AKEBOSI ROCKETS | Necrofantasia | 東方妖々夢　～ Perfect Cherry Blossom. | pending | osu | unknown |
| 2608999 | Demetori | Strawberry Crisis!! | 東方夢時空　～ The Phantasmagoria of Dim.Dream. | wip | osu | supported |
| 2609434 | ryu5150 | SAMURAI SWORD | 東方妖々夢　～ Perfect Cherry Blossom. | pending | taiko | supported |
| 2610601 | BLANKFIELD | Before He Dies | 東方風神録　～ Mountain of Faith. | pending | osu | supported |
| 2611235 | Akiyama Uni | Odoru Mizushibuki | 東方緋想天　～ Scarlet Weather Rhapsody | pending | taiko | supported |
| 2611736 | Scalding Coffee Cup | Too Much Information (feat. Angry Koishi) | 東方地霊殿　～ Subterranean Animism. | pending | taiko | supported |
| 2611820 | Sawawa | Fire in the Phoenix | 東方永夜抄　～ Imperishable Night. | wip | osu | supported |
| 2611880 | Xyris | Dystopian Exodus of the Magical Girls | 東方紅魔郷　～ the Embodiment of Scarlet Devil. | pending | mania | supported |
| 2612199 | Rin | Daishibyo set 00 ~ Yoku Fukaki Reikon | 東方神霊廟　～ Ten Desires. | wip | osu | unknown |
| 2612471 | BLANKFIELD | Flowering Game Night | 東方花映塚　～ Phantasmagoria of Flower View. | wip | osu | supported |
| 2612473 | Diao Ye Zong | Outo Mata | 東方神霊廟　～ Ten Desires | pending | osu | unknown |
| 2612504 | FalKKonE | Beneath the Scarlet Moon, The Crazed Blossoms' Severance | 東方紅魔郷　～ the Embodiment of Scarlet Devil | pending | osu | supported |
| 2613195 | Demetori | Flower Reflecting Mound ~ Higan Retour | 東方花映塚　～ Phantasmagoria of Flower View | pending | osu | unknown |
| 2613359 | DJ SHARPNEL feat. Ichinose Ruru | Trauma Saimin Shoujo Satori! (Motto Trauma Mix) | 東方地霊殿　～ Subterranean Animism. | pending | mania | unknown |
| 2613491 | BUTAOTOME | Shinitagari | 東方妖々夢 ～ Perfect Cherry Blossom | wip | osu | unknown |
| 2613639 | Wooden | LiMiNAL DRiVE (feat. Kaai Yuki) | 東方神霊廟　～ Ten Desires. | pending | mania | unknown |
| 2613786 | ryu5150 | Glow away | 東方地霊殿　～ Subterranean Animism. | pending | taiko | supported |
| 2614302 | A-One | Idoratrize World (Cut Ver.) | 東方鬼形獣　～ Wily Beast and Weakest Creature. | wip | taiko | unknown |
| 2614688 | ZUN | Kokyou no Hoshi ga Utsuru Umi | 東方紺珠伝 ～ Legacy of Lunatic Kingdom | wip | osu | supported |
| 2614783 | Foreground Eclipse | In A Night When Her Sorrow Resounds Around (Speed Up Ver.) | 東方永夜抄　～ Imperishable Night. | pending | osu | unknown |
| 2615275 | Mohican Sandbag | TOHO COCKTAIL | 東方紅魔郷　～ the Embodiment of Scarlet Devil, 東方妖々夢　～ Perfect Cherry Blossom | wip | osu | unknown |
| 2616083 | DJ-Technetium | Frenzy Is Like Teen Spirit | 東方緋想天　～ Scarlet Weather Rhapsody | wip | osu | supported |
| 2616210 | DJKurara | White Hair Little Swords Girl | 東方妖々夢　～ Perfect Cherry Blossom. | pending | mania | supported |

## Negative boundary

Candidate/probable-only hits, generic Touhou source labels, mapper-tag-only signals, direct-refetch failures, external contradictions, ambiguous provenance, policy violations, and the prior live-review identity mismatch `2473015` are all withheld. Existing catalog rows are restored exactly and are not refreshed or reclassified in this PR.

## Final verification

The temporary workflow runs `make check`, `make build`, `git diff --check`, and `touhou_osu.pr_audit --mode all --scope added --forbid-existing-changes`. Exact Deep Review counts are appended before committing.

### Deep Review result

- status: **passed**
- structural diff: **+250 / ~0 / -0**
- provenance: checked **250**, positive **183**, review flags **0**, provider errors **14**
- live osu! exact identity: checked **250**, failures **0**
