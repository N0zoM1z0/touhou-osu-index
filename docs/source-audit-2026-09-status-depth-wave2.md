# Status-scoped Touhou discovery audit — wave 2 (2026-09-14)

## Decision

Add **250** beatmapsets absent from the current `main` catalog. This is an addition-only continuation of the 2026-09-07 status-depth pass: every accepted row still exposes a concrete recognized Touhou game source on a fresh direct osu! API refetch, and rows with THBWiki/TouhouDB contradictions or ambiguity are withheld.

Open weekly PR #42 touches only `0500000-0599999` and `0600000-0699999`; this pass deliberately excludes beatmapset IDs 500000–699999 so the final changed-file set cannot collide with that PR.

## Search breadth

- base catalog: **5044** beatmapsets
- concrete configured game-source queries: **66**
- status buckets: **3** (`graveyard`, `wip`, `pending`)
- query/status buckets attempted: **198**
- official osu! search pages fetched: **302**
- unique absent verified search hits outside the #42 collision range: **4287**
- diversified direct-refetch shortlist: **500**
- accepted after direct `/api/v2/beatmapsets/<id>` refetch: **380**
- direct-refetch failures/drift withheld: **0**
- THBWiki/TouhouDB rows audited before selection: **380**
- red/ambiguous provenance rows withheld: **2**
- final accepted rows: **250**
- final provenance verdicts: **{"supported": 155, "unknown": 95}**
- final rows with advisory provider transport/errors: **0**
- status distribution: **{"graveyard": 221, "pending": 15, "wip": 14}**
- mode coverage: **{"catch": 7, "mania": 51, "osu": 170, "taiko": 28}**

Search membership alone is never acceptance evidence. The search object first has to cross the repository's deterministic `verified` boundary through a concrete recognized Touhou game source; then the ID is fetched again directly from the official beatmapset endpoint. External composition provenance is checked before the final boundary is frozen. The repository Deep Review subsequently repeats external provenance and performs an additional exact identity comparison between the stored row, a fresh osu! API object, and the public beatmapset page.

## Accepted beatmapsets

| Beatmapset ID | Artist | Title | Source | Status | Modes | Query hits | Provenance verdict |
| ---: | --- | --- | --- | --- | --- | ---: | --- |
| 7066 | ZUN | Flandres scarlets theme | The embodiment of scarlet devil extra stage | graveyard | osu | 1 | unknown |
| 7152 | ZUN | The Young Descendants of Tepes | Embodiment of Scarlet Devil | graveyard | osu | 1 | unknown |
| 7913 | ZUN | Faith is for the Transient People | Touhou 10: Mountain of Faith | graveyard | osu | 1 | unknown |
| 8732 | ZUN | Heian Alien | Touhou Project 12 - Undefined Fantastic Object | graveyard | osu | 1 | unknown |
| 10508 | ZUN, Tasogare Frontier | Faith is for the Transient People | Touhou Hisoutensoku | graveyard | osu | 1 | unknown |
| 11996 | SOUND HOLIC feat. 709sec. | Draw the Line | Touhou Youyoumu ~ Perfect Cherry Blossom | graveyard | osu | 1 | supported |
| 11998 | Demetori | Nuclear Fusion | Touhou 11 - Subterranean Animism | graveyard | osu | 1 | unknown |
| 12125 | ZUN | Ball of the Witches | Immaterial and Missing Power | graveyard | osu | 1 | unknown |
| 12584 | Akiyama Uni (U2) | The Doll Maker of Bucuresti | Scarlet Weather Rhapsody | graveyard | osu | 1 | unknown |
| 13554 | ZUN | Mystic Oriental Dream ~ Ancient Temple | Perfect Cherry Blossom OST | graveyard | osu | 1 | supported |
| 17242 | ZUN | Phantom Ensemble | Touhou Youyoumu: Perfect Cherry Blossom | graveyard | osu | 1 | unknown |
| 18296 | ZUN | Shoujo Kisoukyoku ~ Dream Battle | Touhou Eiyashou - Imperishable Night | graveyard | osu | 1 | supported |
| 18913 | ZUN McRolld'd | Heian Alien ~ ShAdOwPoZo version | Touhou 12: Undefined Fantastic Object | graveyard | osu | 1 | unknown |
| 19252 | ZUN | Grave of Being | Mountain of Faith | graveyard | osu | 1 | unknown |
| 19797 | ZUN | The Traditional Old Man and The Stylish Girl | Undefined Fantastic Object | graveyard | osu | 1 | unknown |
| 20835 | ZUN / nazz-can | Solar sect of mystic wisdom | Touhou 11 : Subterranean Animism | graveyard | osu | 1 | unknown |
| 22270 | ZUN | Satori Maiden ~ third eye | th11 Chireiden ~ Subterranean Animism | graveyard | osu | 1 | unknown |
| 26224 | ZUN | The Great Fairy Wars | Touhou 12.8 ~ Great Fairy Wars | graveyard | osu | 1 | unknown |
| 28548 | ZUN | Illusionary Night ~ Ghostly Eyes | Imperishable Night - Touhou 8 | graveyard | osu,taiko | 1 | supported |
| 38306 | Akiyamauni, ZUN | Septette for the Dead Princess | Touhou Hisouten ~Scarlet Weather Rhapsody | graveyard | osu | 1 | unknown |
| 39006 | ZUN | Toono Gensou Monogatari | Perfect Cherry Blossom | graveyard | osu | 1 | supported |
| 47020 | ZUN | Old Yuanxian | Touhou 13- Ten Desires | graveyard | osu | 1 | unknown |
| 48953 | ZUN | Green-Eyed Jealousy | Touhou 11- Subterranean Animism | graveyard | osu | 1 | supported |
| 52683 | Zun | Lunar Clock  Luna Dial | Touhou 7.5 Immaterial and Missing Power | graveyard | osu | 1 | unknown |
| 57005 | Dobu Usagi | Shikai Henai Kyoku | [Touhou 13] Ten Desires | graveyard | osu | 1 | unknown |
| 85106 | Merami | ~ Lost Place | 東方地霊殿 ~ Touhou Subterranean Animism | graveyard | osu | 1 | unknown |
| 87020 | ZUN | Magus Night | Touhou 12.8 Great Fairy Wars | graveyard | mania | 1 | unknown |
| 102897 | Twilight Frontier | Shoutoku Legend ~ True Administrator | Hopeless Masquerade | graveyard | taiko | 1 | unknown |
| 108631 | ZUN | The Capital City of Flowers in the Sky | 東方妖々夢 | graveyard | osu | 1 | unknown |
| 111534 | ZUN | Hiroari Shoots a Strange Bird ~ Till When? | Touhou Scarlet Weather Rhapsody | graveyard | osu | 1 | unknown |
| 113291 | Tasogare furontia | Touhou hisouten | 全人類ノ天楽録 ～東方緋想天 OR | graveyard | osu | 1 | unknown |
| 124069 | ZUN | Loss Emotion | Touhou Shinkirou ～ Hopeless Masquerade | graveyard | osu | 1 | unknown |
| 125216 | ZUN | Mysterious Exorcism Rod | Double Dealing Character | graveyard | taiko | 1 | unknown |
| 131502 | ZUN | Voyage 1970 | 東方永夜秒 ~ Imperishable Night | graveyard | osu | 1 | supported |
| 136085 | Masayoshi Minoshima ft. Nico Nico Chorus | Bad Apple!! feat. nomico (Short ver.) | TH4 Touhou Gensoukyou ~ Lotus Land Story | graveyard | osu | 1 | unknown |
| 144691 | maritumix | Defiance | 東方輝針城 | graveyard | mania | 1 | supported |
| 160133 | SOUND HOLIC/Nana Takahashi | Dancing like Nirvana | 東方星蓮船 | graveyard | osu | 1 | supported |
| 163801 | ZUN | Flight of the Bamboo Cutter ~ Lunatic Princess | Touhou 8: Imperishable Night | graveyard | osu | 1 | unknown |
| 184638 | ZUN | Cheat Against Impossible Danmaku | Danmaku Amanojaku ~ Impossible Spell Card | graveyard | osu | 1 | unknown |
| 192689 | CROW'SCLAW | Strawberry Crisis | 東方夢時空 | graveyard | osu | 1 | supported |
| 228331 | dBu | Hartmann's Youkai Girl | Touhou Chireiden ~ Subterranean Animism | graveyard | osu | 1 | unknown |
| 247479 | Alstroemeria Records | Starbow Dream | Phantasmagoria of dim.dream unused track | graveyard | osu | 1 | supported |
| 268259 | Akiyamauni | Dancing Water Spray | 東方緋想天 | graveyard | taiko | 1 | supported |
| 271451 | ZUN | Raise the Flag of Cheating | Touhou 14.3: Impossible spell card | graveyard | osu | 1 | unknown |
| 288926 | Demetori | Old Yuanxian | 東方神霊廟　～ Ten Desires Touhou | graveyard | osu | 1 | unknown |
| 312390 | Halozy | 8 Ganme no Roji | Touhou Gensoukyou ~ Lotus Land Story | graveyard | osu | 1 | unknown |
| 320100 | IOSYS | Third Eyer! | 東方地霊殿 | graveyard | osu | 1 | unknown |
| 324147 |  | Hartmann's Youkai Girl | Touhou 14.5 Urban Legend In Limbo OST | graveyard | mania | 1 | unknown |
| 349956 | ZUN | The Clown of the Star-Spangled Banner | Touhou Kanjuden ~ Legacy of Lunatic Kingdom | graveyard | osu | 1 | unknown |
| 350334 | ZUN | Pierrot of the Star Spangled Banner (Clownpiece's theme) | Touhou 15: Legacy of Lunatic Kingdom | graveyard | osu | 1 | unknown |
| 354140 | Foreground Eclipse | Last Liar Standing | Subterranean Animism | graveyard | mania | 1 | supported |
| 354210 | Demetori | Alice Maestra ~ Flow My Tears, the Said | 東方幻想郷　～ Lotus Land Story. | graveyard | osu | 3 | unknown |
| 357617 | Starsand | Eternal Paradise | Touhou 5 - Mystic Square | graveyard | mania | 1 | supported |
| 364396 | ZUN | Pierrot of the Star-Spangled Banner | Touhoy 15: Legacy of Lunatic Kingdom | graveyard | osu | 1 | unknown |
| 397180 | Kishida | Hartmann's Youkai Girl | 東方深秘録　～ Urban Legend in Limbo | graveyard | osu | 2 | unknown |
| 408710 | 3L | The Rise and Fall | Touhou 12 - Undefined Fantastic Object | graveyard | osu | 1 | supported |
| 412299 | FELT | inside | 東方文花帖　～ Shoot the Bullet | graveyard | osu | 2 | supported |
| 454213 | ZUN | Demystify Feast | 東方萃夢想 | graveyard | mania | 1 | supported |
| 479282 | Maika | crescent moon | 東方心綺楼 ～ Hopeless Masquerade | graveyard | osu | 2 | supported |
| 485971 | Unlucky Morpheus | Now, Until the Moment You Die | 東方靈異伝　〜 Highly Responsive to Prayers | graveyard | osu | 2 | unknown |
| 701891 | U2 Akiyama | Naki Oujo no Tame no Septette | 東方緋想天 ～ Scarlet Weather Rhapsody | graveyard | osu | 2 | supported |
| 705831 | ZUN | Secret God Matara ~ Hidden Star in All Seasons | 東方天空璋　～ Hidden Star in Four Seasons | graveyard | osu | 2 | unknown |
| 708318 | Jun.A | The Refrain of the Lovely Great War | 妖精大戦争　～ 東方三月精 | graveyard | osu | 1 | supported |
| 711594 | "Syrup Comfiture" x ALADDIN | Say my name | 東方夢時空　～ Phantasmagoria of Dim.Dream | graveyard | osu | 2 | supported |
| 724307 | A-ONE | Time Will Tell | 東方靈異伝 ～ Highly Responsive to Prayers. | graveyard | osu | 2 | supported |
| 728273 | SOUND HOLIC | The other-side | 東方封魔録 ～ Story of Eastern Wonderland | graveyard | osu | 2 | supported |
| 734008 | Masayoshi Minoshima feat.nomico | Lost Emotion | 東方心綺楼 | graveyard | osu | 1 | supported |
| 740855 | ELEMENTAS(A-One) | Night Falls ~ Evening Star | 東方憑依華 ～ Antinomy of Common Flowers. | graveyard | catch | 2 | supported |
| 749399 | U2 | Ningyou Saiban | 東方萃夢想 ～ Immaterial and Missing Power. | graveyard | osu,taiko | 2 | supported |
| 775235 | Akiyama Uni | Odoru Mizushibuki | 東方緋想天 〜 Scarlet Weather Rhapsody | graveyard | catch | 2 | supported |
| 776471 | CielArc | Stargazer | 東方天空璋 〜 Hidden Star in Four Seasons | graveyard | osu | 2 | unknown |
| 779513 | FELT | crescent moon | 東方心綺樓 ～ Hopeless Masquerade. | graveyard | osu | 1 | supported |
| 788507 | EastNewSound | You're the Love of My Life | Touhou Kishinjou Shining Needle Castle~ Double Dealing Character (東方輝針城)～ Double Dealing Character | graveyard | osu | 1 | supported |
| 795239 | motoko | Tears in dreams | 東方神霊廟 | graveyard | osu | 1 | supported |
| 813310 | Unlucky Morpheus | Makyou Daten Roku Sariel | 東方靈異伝　～ The Highly Responsive to Prayers | graveyard | taiko | 2 | unknown |
| 814460 | Liz Triangle | Immortal Philosophy | 東方深秘録 ～ Urban Legend in Limbo, Ibaraki Kasen's Theme | graveyard | taiko | 2 | unknown |
| 829617 | ZUN | Secret God Matara ~ Hidden Star in All Seasons. | Touhou 16: Hidden Star in Four Seasons | graveyard | osu | 1 | supported |
| 831065 | MISATO | Necro Fantasia | 東方妖々夢 Perfect Cherry Blossom | graveyard | osu | 1 | supported |
| 834973 | ZUN | Game Over | 東方夢時空 〜 Phantasmagoria of Dim.Dream. | graveyard | taiko | 2 | supported |
| 841127 | Demetori | retrospective kyoto ~ Japanese Beautiful Barrage | 東方文花帖～ Shoot the Bullet. | graveyard | osu | 2 | unknown |
| 852508 | ZUN | Nightmare Diary | Touhou 16.5 Violet Detector | graveyard | osu | 1 | supported |
| 855622 | SOUND HOLIC | Hell Rose | 東方紺珠伝 | graveyard | osu | 1 | supported |
| 868324 | SOUND HOLIC | IMAGiNATE | 东方天空璋　～ Hidden Star in Four Seasons | graveyard | osu | 1 | supported |
| 915960 | IOSYS | Club Ibuki in Break All | 東方萃夢想～ Immaterial and Missing Power | graveyard | taiko | 2 | supported |
| 918724 | Rokugen Alice | Kao no Nai Tsuki | 東方心綺楼 ～Hopeless Masquerade. | graveyard | osu | 2 | supported |
| 919853 | EUGEN/Scarlet | Abaddon's 5th Chord | 東方紅魔郷～the Embodiment of Scarlet Devil. | graveyard | osu | 1 | supported |
| 924396 | Komiya Mao | (can you) understand me? | 東方輝針城　? Double Dealing Character. | graveyard | osu | 1 | supported |
| 925849 | ZUN | Onbashira no Hakaba ~ Grave of Being | 東方風神録 | graveyard | osu | 1 | supported |
| 930662 | Ryu-5150 | Louder Than Steel | 東方夢時空　～ Pantasmagria of Dim.Dream | graveyard | mania | 1 | supported |
| 945730 | Ichiko | Limmit | 東方Project ～ Perfect Cherry Blossom | graveyard | osu | 1 | supported |
| 949326 | Foreground Eclipse | Vermillion Halo | Touhou Kaeidzuka ~ Phantasmagoria of Flower View. | graveyard | osu | 1 | supported |
| 955971 | Unlucky Morpheus | Fuujin Shoujo ~ God Of Guitar | 東方花映塚 〜 Phantasmagoria of Flower View | graveyard | osu | 2 | unknown |
| 970939 | FELT | Star Velocity | 東方幻想郷 〜 Lotus Land Story. | graveyard | osu | 2 | supported |
| 993802 | Hachimitsu-Lemon | Disappearing Queen | 東方封魔録　～ the Story of Eastern Wonderland. | graveyard | osu | 2 | unknown |
| 1018979 | Akatsuki Records | Trance Dance Anarchy | Hidden Star in Four Seasons | graveyard | osu | 1 | supported |
| 1019536 | ZUN | Guuzou ni Sekai wo Yudanete ~ Idoratrize World | 東方鬼形獣　～ Wily Beast and Weakest Creature | graveyard | osu | 2 | unknown |
| 1021448 | ill.bell | PARFECT FREEEEEEEEEZE!! | 妖精大戦争　～ Fairy Wars | graveyard | osu | 1 | supported |
| 1024007 | Aki | Cosmic Rainbow | EUROBEAT VOL 9 UNDEFINED FANTASTIC OBJECT | graveyard | osu | 1 | supported |
| 1034751 | Foreground Eclipse | Destruction | 東方風神録　～ Mountain of Faith, Sanae Kochiya's Theme | graveyard | osu | 1 | supported |
| 1038095 | ALiCE'S EMOTiON | Ghostly Parapara Ship (Hardcore Edit) | 東方Project ～ Undefined Fantastic Object | graveyard | osu | 1 | supported |
| 1055729 | Diao ye zong | tamesugame | ダブルスポイラー　～ 東方文花帖, 東方文花帖　～ Shoot the Bullet | graveyard | mania | 3 | unknown |
| 1059428 | DiGiTAL WiNG | DON'T STOP | 東方妖々夢 〜 Perfect Cherry Blossom | graveyard | mania | 1 | supported |
| 1062334 | Rin | Lunatic set 15 ~ The Moon as Seen from the Shrine | Touhou Kanjuden Legacy of Lunatic Kingdom | graveyard | mania | 1 | supported |
| 1064817 | Diao Ye Zong feat. nayuta | Tori yo | æ±æ–¹æ–‡èŠ±å¸–ã€€ï½ž Shoot the Bullet. | graveyard | osu | 1 | supported |
| 1068162 | Akatsuki Records | Trans Dance Anarchy | 出典：東方天空璋 ～ Hidden Star in Four Seasons | graveyard | osu | 2 | unknown |
| 1076253 | A-One | flower tartan | 東方 ~Phantasmagoria of Flower View | graveyard | osu | 1 | supported |
| 1077448 | A-One | Dreamy Purple | 東方 Project ~Legacy of Lunatic Kingdom | graveyard | osu | 1 | supported |
| 1081568 | ELEMENTAS (A-One) | Night Falls ~ Evening Star | Touhou 15.5 ~ Antinomy of Common Flowers | graveyard | osu | 1 | supported |
| 1091456 | Stack | HANIPAGANDA | 東方鬼形獣　〜 Wily Beast and Weakest Creature | graveyard | mania,taiko | 2 | supported |
| 1096890 | Matsumoto Sara | Ito Hakanaki Hikari no Gotoku | 妖精大戦争 ～ Eastern Three Fairies. | graveyard | osu | 1 | supported |
| 1097634 | maritumix | Blackout | 東方地霊殿 ～Subterranean Animism | graveyard | osu | 1 | supported |
| 1098754 | AUTUMN+GHOST feat. Akira Complex | PURE FURY | Touhou 15: Kanjuden ~ Legacy of Lunatic Kingdom | graveyard | osu | 1 | supported |
| 1100519 | Ayaponzu * | Watashi Kenshi | 東方妖々夢　～ Ancient Temple | graveyard | osu | 1 | supported |
| 1114271 | Risutaru | Broken Moon | 东方萃梦想　～ Immaterial and Missing Power. | graveyard | osu | 1 | supported |
| 1118935 | ZUN | Tonight Stars an Easygoing Egoist(Live ver.) ~ Egoistic Flower | 東方憑依華(とうほうひょういばな) ~ Antinomy of Common Flowers. | graveyard | mania | 2 | unknown |
| 1151043 | ZUN | Kobito of the Shining Needle ~ Little Princess | 东方辉针城 ～ Double Dealing Character | graveyard | osu | 1 | supported |
| 1155214 | Alstroemeria Records | WORLD THOERY | 東方夢時空 ~ the Phantasmagoria of Dim.Dream. | graveyard | mania | 2 | unknown |
| 1166349 | Misato | Paranoid Lost | Touhou, 東方風神録　～ Mountain of Faith. | graveyard | osu | 1 | supported |
| 1179553 | Diao ye zong feat. Meramipop | Karakurenai no Kage | 東方非想天則　～ 超弩級ギニョルの謎を追え. | graveyard | taiko | 1 | supported |
| 1185615 | Kurenainagi Tabibito | Beloved Tomboyish Girl | 東方紅魔郷　～ Embodiment of Scarlet Devil. | graveyard | osu | 2 | unknown |
| 1190942 | FELT | Vagueness & JOURNEY | 東方緋想天〜Scarlet Weather Rhapsody | graveyard | osu | 2 | unknown |
| 1209716 | SOUND HOLIC | POLYHEDRA | touhou hopeless masquerade | graveyard | osu | 1 | supported |
| 1216027 | Foreground Eclipse | You May Not Want To Hear This But | 東方Project ～ Subterranean Animism | graveyard | osu | 1 | supported |
| 1244065 | Chata | Remind | 東方Project 東方神霊廟 | graveyard | osu | 1 | supported |
| 1247967 | Twilight Frontier | The Ground's Color is Yellow | 東方Project 10.5: 東方緋想天 ～ Scarlet Weather Rhapsody | graveyard | osu | 2 | unknown |
| 1286563 | SOUND HOLIC feat. Nana Takahashi | DIMENSION FREEZE | 東方夢時空 ～ Phantasmagoria of Dimensional Dream, Kana Anaberal's theme | graveyard | taiko | 1 | supported |
| 1287866 | ShinRa-Bansho feat. Ayo | Real or Fake | 東方文花帖 〜 Shoot the Bullet. | graveyard | taiko | 2 | supported |
| 1310130 | ZUN | Jelly stone | 東方鬼形獣 | graveyard | osu | 1 | supported |
| 1326259 | sun3 | Perfect Cherry Storm | 東方妖々梦 ～ Perfect Cherry Blossom. | graveyard | mania | 1 | supported |
| 1361096 | ZUN | Yume Shoushitsu ~ Lost Dream | Touhou Yumekijuu ~ the Phantasmagoria of Dim.Dream | graveyard | osu | 1 | supported |
| 1402707 | Rin | Lunatic set 16 ~ The Space Shrine Maiden Returns Home | 東方紺珠伝　～ Legacy of Lunatic Kingdom | graveyard | osu | 2 | supported |
| 1413239 | Zun | Fortunate Kitten | 东方虹龙洞　～ Unconnected Marketeers. | graveyard | osu | 1 | supported |
| 1423403 | ZUN | Smoking Dragon | Touhou 18 Unconnected Marketeers OST | graveyard | mania | 1 | supported |
| 1433488 | S.S.H. | Touhou Judgment in the Sixtieth Year ~ Fate of Sixty Years | Touhou Phantasmagoria of Flower View | graveyard | osu | 2 | unknown |
| 1434961 | ZUN | Fortunate Kitten (BegissoR's Remix) | 東方虹龍洞　～ Unconnected Marketeers | graveyard | taiko | 2 | unknown |
| 1435632 | ELEMENTAS | Night Falls ~ Evening Star | Touhou 15.5 Antinomy of Common Flowers | graveyard | osu | 1 | supported |
| 1446911 | 3L | Endless night | Touhou Yume Jikan ~ Phantasmagoria of Dim.Dream | graveyard | mania | 1 | supported |
| 1453479 | SOUND HOLIC | THE EVENING STAR (feat. YURiCa/hanatan) | 東方萃夢想 〜 Immaterial and Missing Power. | graveyard | mania | 2 | unknown |
| 1483091 | T. Stebbins | On The Moon | 東方紺珠伝 - Legacy of Lunatic Kingdom | graveyard | mania,taiko | 2 | supported |
| 1501131 | Foreground Eclipse | Dear, Are You Getting Sober | 東方Project ～ Mountain of Faith | graveyard | osu | 1 | supported |
| 1517522 | MISATO | Necro Fantasia | 東方Project 東方妖々夢　～ Perfect Cherry Blossom. | graveyard | osu | 1 | supported |
| 1531685 | GET IN THE RING | Face To Face | 東方文花帖 | graveyard | osu | 1 | supported |
| 1542580 | SiIvaGunner | Bad Apple!! (Promotional Version) | Touhou 4: Lotus Land Story | graveyard | osu | 1 | supported |
| 1553983 | Komiya mao | (can you)understand me? | 東方輝針城　〜 Double Dealing Character. | graveyard | osu | 2 | unknown |
| 1580781 | Akatsuki Records | Senritsu no COLORS | 東方輝針城　～ Double Dealing Character. | graveyard | osu | 2 | unknown |
| 1584251 | Unlucky Morpheus and Undead Corporation | You're better off alive | 東方 Project ～ Phantasmagoria of Flower View | graveyard | mania | 1 | supported |
| 1608373 | Hosen | UM Chimata's Theme - Where is That Bustling Marketplace Now | 東方虹龍洞　〜 Unconnected Marketeers. | graveyard | mania | 2 | unknown |
| 1619078 | Nachi | Against, Perfect Cherry Blossom | Alstroemeria Records, 東方妖々夢 | graveyard | mania | 1 | supported |
| 1620298 | Marcia | Amaku Surudoi Toge | 東方虹龍洞 | graveyard | osu | 1 | supported |
| 1625096 | Akatsuki Records | Reverse Trigger | 弾幕アマノジャク　～ Impossible Spell Card. | graveyard | osu | 2 | unknown |
| 1631297 | ZUN | Magus Night | 妖精大戦争 ～ Great Fairy Wars | graveyard | osu | 2 | unknown |
| 1635161 | UNDEAD CORPORATION | Wheel of Doom | 東方紺珠伝 〜 Legacy of Lunatic Kingdom. | graveyard | osu | 2 | supported |
| 1635287 | katikatiyama | Yuureisen No Uta | 東方Project 〜 Undefined Fantastic Object | graveyard | osu | 1 | supported |
| 1659346 | mokemoke | Forbidden Ideal | 東方怪綺談 Mystic Square | graveyard | taiko | 1 | supported |
| 1673409 | nayuta | Stray Star | 東方怪綺談　～ Mystic Square. | graveyard | mania | 2 | supported |
| 1691302 | BUTAOTOME | Voice of the Distant Sky | ダブルスポイラー　～ 東方文花帖 | graveyard | osu | 2 | unknown |
| 1735382 | ZUN | Eternal Paradise | 東方怪綺談 〜 Mystic Square | graveyard | osu,taiko | 2 | supported |
| 1735515 | ZUN | The Princess Who Slays Dragon Kings | 東方紅龍洞　～ Unconnected Marketeers. | graveyard | osu | 1 | supported |
| 1797734 | Eternal Melody | Scarlet Serenade | 東方Project ~ Embodiment of Scarlet Devil | graveyard | osu | 1 | supported |
| 1814521 | katagiri | WallHakkr | 東方神霊廟　～ Ten Desires. | graveyard | mania | 2 | supported |
| 1838990 | A-One feat. Shihori | Bloody Night | 東方妖々夢　～ Perfect Cherry Blossom. | wip | taiko | 2 | supported |
| 1864956 | Alstroemeria Records | PUNISHMENT feat. Sakaue Nachi | 東方夢時空　～ Phantasmagoria of Dim. Dream. | graveyard | osu | 2 | unknown |
| 1888457 | Pizuya's Cell feat. Futoumeido | NOiSE | 秘封ナイトメアダイアリー　〜 Violet Detector. | graveyard | catch | 2 | supported |
| 1899153 | Odyssey Eurobeat | Rain Dance | 東方風神録 〜 Mountain of Faith. サウンドトラック | graveyard | osu | 1 | supported |
| 1900085 | Kisida | Hartman's Youkai Girl | 東方深秘録 〜 Urban Legend in Limbo. | graveyard | osu | 2 | unknown |
| 1912985 | katikatiyama | Alien no uta | 東方星蓮船　～ Undefined Fantastic Object. | graveyard | osu | 2 | unknown |
| 1913275 | katikatiyama | Yosuzume no Uta | 東方Project ～ Imperishable Night | graveyard | osu | 1 | supported |
| 1916669 | Paradot / Parako Tsuruga | Ultimate Taste | Touhou 6 Koumakyou ~ the Embodiment of Scarlet Devil | graveyard | mania,osu | 1 | supported |
| 1917553 | SYNC.ART'S feat. Kaori Aihara | Absolute Demolition | 東方紅魔郷　～ the Embodiment | graveyard | osu | 1 | supported |
| 1923987 | ZUN | Complete Darkness | Touhou 2: Story of Eastern Wonderland | graveyard | osu | 1 | supported |
| 1932692 | Akatsuki Records | Gotcha Gotcha | バレットフィリア達の闇市場　〜 100th Black Market. | graveyard | osu | 2 | supported |
| 1954238 | UNDEAD CORPORATION | Flowering Night Fever | TouHou ~ Phantasmagoria of Flower View | graveyard | mania | 1 | supported |
| 1959001 | Saitama Saisyu Heiki & Aether | Desire Drive | 東方神霊廟 〜 Ten Desires. | graveyard | mania | 2 | unknown |
| 1965948 | Zun | Jelly Stone | Touhou 17: Wily Beast and Weakest Creature | graveyard | mania | 1 | supported |
| 1998287 | ZUN | The World Is Made in an Adorable Way | 東方獣王園　～ Unfinished Dream of All Living Ghost. | graveyard | osu | 2 | supported |
| 1998558 | ZUN | Sekai wa kawaiku dekiteiru | 東方獣王園　〜 Unfinished Dream of All Living Ghost | graveyard | osu | 2 | supported |
| 2002636 | HAGISOPH | Lamento | 東方剛欲異聞　～ 水没した沈愁地獄 (Touhou Gouyoku Ibun ~ Submerged Hell of Sunken Sorrow) Memento of All Organisms ~ Memory of Fossil Energy (有機体全てのメメント　～ Memory of Fossil Energy) | graveyard | mania | 1 | supported |
| 2044388 | Demetori | The Primal Scene of Japan the Girl Saw ~ Dance of puNDarika | 東方風神録 ～ Mountain of Faith. | pending | osu | 2 | unknown |
| 2049059 | Ryu5150 | Louder than steel | 東方夢時空　～ Phantasmagria of Dim.Dream | graveyard | osu | 1 | supported |
| 2077356 | Demetori | Yumeshoushitsu ~ Lost Dream | 東方夢時空　～ The Phantasmagoria of Dim. Dream | graveyard | mania | 2 | unknown |
| 2081821 | dBuMusic | Plastic Mind | touhou 5 mystic square stage 3 boss theme remix by dbu | graveyard | osu | 1 | supported |
| 2088862 | Xenoglossy | Alice in Electron Land | 东方怪绮谈 ～ Mystic Square | graveyard | mania | 1 | supported |
| 2097656 | Xi | Rokujuu-nen Me no Shinsoku Saiban ~ Rapidity is a justice | 東方花映塚　～ Phantasmagoria of Flower View. | graveyard | mania | 3 | unknown |
| 2100719 | Vivienne | Different Kind of Love | 東方風神録より "明日ハレの日、ケの昨日" | graveyard | osu | 1 | supported |
| 2105888 | Akiyama Uni | Drunk as i like | 东方绯想天 ～ Scarlet Weather Rhapsody. | graveyard | osu | 1 | supported |
| 2148417 | Hanatan | Eternal Party | TOHO EUROBEAT VOL 11 HIGHLY RESPONSIVE TO PRAYERS | graveyard | osu | 1 | supported |
| 2156334 | Para Dot | Myriad texture | 东方星莲船　～ Undefined Fantastic Object. | graveyard | mania | 1 | supported |
| 2201245 | UNDEAD CORPORATION | Adore Your Pain | 東方地霊殿　～ Subterranean Animism. | wip | osu | 2 | supported |
| 2229234 | MONO | Fantasmagoria | BMS / 東方妖々夢　～ Perfect Cherry Blossom | graveyard | mania | 1 | supported |
| 2247858 | LA KIA | Ruten no Michi | 东方神灵庙　～ Ten Desires. | graveyard | osu | 1 | supported |
| 2260643 | Adust Rain | Last Blast | 東方風神録 神さびた古戦場～Suwa Foughten Field | graveyard | osu | 1 | supported |
| 2264583 | ShinRa-Bansho | The Maid's Heart is a Puppet | 東方花映塚　～ Phantasmagoria of Flower View. | pending | mania | 2 | unknown |
| 2265550 | ZUN | Taketori Hishou ~ Lunatic Princess | 東方永夜抄　～ Imperishable Night. | graveyard | mania | 2 | supported |
| 2266172 | ZUN | The Primal Scene of Japan the Girl Saw | Touhou 19 - Unfinished Dream of All Living Ghost (東方獣王園　〜 Unfinished Dream of All Living Ghost) | graveyard | taiko | 2 | supported |
| 2267230 | TaNaBaTa | Ougon Kouro | Touhou Seirensen ~ Undefined Fantastic Object | graveyard | osu | 1 | supported |
| 2276262 | Xyris | Dystopian Exodus of the Magical Girls | 东方红魔乡　～ the Embodiment of Scarlet Devil | graveyard | osu | 1 | supported |
| 2289072 | Paradot. | ARTIFACTS | 東方鬼形獣 ～Wily Beast and Weakest Creature. | graveyard | mania | 2 | supported |
| 2293760 | ZUN | Love-coloured Magic | Touhou 02: The Story of Eastern Wonderland | graveyard | osu | 1 | supported |
| 2321848 | Yuuhei Satellite | Hitomi o Tojite, Utsusu Mugen | 東方地霊殿　～ Subterranean Animism. | pending | osu | 2 | unknown |
| 2335619 | co7ty | Gate of Year-Round | Touhou Tenkuushou (東方天空璋) | graveyard | mania | 1 | supported |
| 2335650 | ShinRa-Bansho | Zenryoku Happy Life | 東方永夜抄　～ Imperishable Night. | wip | osu | 2 | unknown |
| 2345920 | Akatsuki Records | Midnight Parade | Touhou 6 - Embodiment of Scarlet Devil. | graveyard | mania | 1 | supported |
| 2358042 | Mamemi | Love The BEAT | TOHO EUROBEAT VOL.10 HIGHLY RESPONSIVE TO PRAYERS | graveyard | osu | 1 | supported |
| 2369697 | Paradot | Nazokake | Touhou 20: Fossilized Wonders | graveyard | mania | 1 | supported |
| 2379634 | EastNewSound | poisonous rain | 東方花映塚　～ Phantasmagoria of Flower View, Medicine Melancholy's theme | graveyard | osu | 1 | supported |
| 2380793 | ShinRa-Bansho | Administrator's Logic | 東方妖々夢　～ Perfect Cherry Blossom | graveyard | osu | 2 | unknown |
| 2383593 | Shinra-Bansho | Muishiki Requiem (cosmobsp rmx) | 東方地霊殿　～ Subterranean Animism. | graveyard | taiko | 2 | supported |
| 2390231 | izna | A null set (izna remix) | 東方文花帖　～ Double Spoiler. | graveyard | taiko | 2 | supported |
| 2399199 | Syrufit feat. Mei Ayakura & Ichimatsu Tsubaki | ESCAPE | 東方紅魔郷　～ the Embodiment of Scarlet Devil. | graveyard | osu | 2 | supported |
| 2400857 | ZUN | Sailor of Time | The Phantasmagoria of Dim.Dream | graveyard | mania | 1 | supported |
| 2402465 | Yuuyu / Yuuna sasara | Imperishable Night 2006 (2016 Refine) | 東方永夜抄 ～Imperishable Night. | graveyard | mania | 2 | unknown |
| 2403482 | ziki_7 | Submerged Hell of Sunken Sorrow (Arrange Version) | Touhou 17.5 Gouyoku Ibun ~ Sunken Fossil World | graveyard | osu | 1 | supported |
| 2404559 | ZUN | Jelly Stone | Touhou Kikeijuu ~ Wily Beast and Weakest Creature | graveyard | mania | 1 | supported |
| 2411431 | BilliumMoto | Four Veiled Stars | 東方永夜抄 ～ Hidden Star in Four Seasons | graveyard | osu | 1 | supported |
| 2426219 | ZUN | Onbashira no Hakaba ~ Grave of Being | 東方風神録　～ Mountain of Faith. | graveyard | taiko | 2 | supported |
| 2431141 | Poplica* | Zillion Lights | 東方星蓮船～Undefined Fantastic Object | graveyard | mania | 1 | supported |
| 2432202 | ZUN | Itooshiki Chiri no Sumika | 東方錦上京　～ Fossilized Wonders. | graveyard | taiko | 2 | supported |
| 2453994 | Rien | Gen ~ In her dreams | 東方封魔録.　～ the Story of Eastern Wonderland. | graveyard | taiko | 2 | unknown |
| 2461880 | Adust Rain | Joker's Cranberrybox | 東方花映塚　～ U.N. Owen was her? | graveyard | mania | 1 | supported |
| 2463139 | Spacelectro ft. Shiiki Reku | Rhythmy | 東方花映塚.　～ Phantasmagoria of Flower View. | graveyard | taiko | 1 | supported |
| 2472017 | senya | Kanousei no Keshin | 東方非想天則　～ 超弩級ギニョルの謎を追え | wip | taiko | 1 | supported |
| 2473015 | Matsubame Frame | The Waltz of the Night | 東方永夜抄　～　Imperishable Night | pending | osu | 2 | unknown |
| 2476061 | Rin | Eientewi set 12 Another ~ Voyage 1970 | 東方永夜抄~ Imperishable Night | graveyard | mania | 1 | supported |
| 2482178 | ShinRa-Bansho | Nonfic Inbouron | 東方錦上京　～ Fossilized Wonders. | pending | osu | 2 | unknown |
| 2482750 | SOUND HOLIC | Earthquake Super Shock | 東方緋想天 ～ Scarlet Weather Rhapsody | pending | osu | 2 | supported |
| 2493017 | Para Dot. | Alone Goddess | 東方錦上京 〜 Fossilized Wonders. | graveyard | osu | 2 | supported |
| 2496988 | ZUN | Complete Darkness (Cut Ver.) | 東方封魔録 〜 Story of Eastern Wonderland | graveyard | osu | 2 | unknown |
| 2504831 | Toby Fox x ZUN | Necrolovania | UNDERTALE x 東方妖々夢　～ Perfect Cherry Blossom | graveyard | osu | 1 | supported |
| 2536084 | Amateras Records | Reverside Relief | 東方鬼形獣　～ Wily Beast and Weakest Creature. | pending | taiko | 2 | supported |
| 2547719 | A-ONE | Rain Dance | TOHO EUROBEAT VOL.7 MOUNTAIN OF FAITH | wip | osu | 1 | supported |
| 2548689 | GLS | Flawless Wings of Yatagarasu | 東方地霊殿 〜 Subterranean Animism | graveyard | mania | 2 | supported |
| 2559424 | Steiner | cosmicalism | 東方星蓮船 〜 Undefined Fantastic Object. | graveyard | mania | 2 | supported |
| 2560545 | LeaF | Armageddon | 東方非想天則~ 超弩級ギニョルの謎を追え | graveyard | mania | 1 | supported |
| 2570941 | Xi | Rokujuu-nen Me no Shinsoku Saiban ~ Rapidity is a justice | 東方花映塚　～ Phantasmagoria of Flower View. | wip | osu | 2 | unknown |
| 2574305 | FELT | Puppet in the Dark(Part2:Buried Away) | 東方神霊廟  ～ Ten Desires. | wip | mania | 2 | unknown |
| 2590124 | IOSYS | Endless Tewi-me-park | 東方花映塚(东方花映冢) ~ Phantasmagoria of Flower View | pending | catch | 2 | unknown |
| 2591962 | ryu5150 | Louder than steel | 東方夢時空　～ Phantasmagoria of Dim.Dream | pending | taiko | 2 | supported |
| 2598918 | Shibayan feat. 3L | MyonMyonMyonMyonMyonMyon! (Cut Ver.) | 東方妖々夢　～ Perfect Cherry Blossom. | pending | catch | 2 | unknown |
| 2605173 | BUTAOTOME | In the Black | 東方憑依華　～ Antinomy of Common Flowers. | wip | osu | 2 | unknown |
| 2606790 | Everyone from the Red Cucumber thread | Kappa-sama no Iu Toori ~ One-way Accelerator | 東方地霊殿　～ Subterranean Hatred | wip | osu | 2 | unknown |
| 2607094 | Akatsuki Records | KUNG-FU MASTER No.9 | 東方紅魔郷　～ the Embodiment of Scarlet Devil | pending | osu | 2 | unknown |
| 2609950 | Alstroemeria Records | Ingress | バレットフィリア達の闇市場 ばれっとふぃりあたちのやみしじょう ～ 100th Black Market. | pending | mania | 2 | supported |
| 2611339 | Sally | Remind | 東方神霊廟　～ Ten Desires. | pending | osu | 2 | unknown |
| 2612629 | O-LIFE.JP | Yakujinsama no Couple Dance | 東方風神録　～ Mountain of Faith. | wip | catch | 2 | unknown |
| 2612960 | 7_7 | Bitch Gun | 東方紅魔郷　～ the Embodiment of Scarlet Devil. | wip | osu | 2 | unknown |
| 2613222 | HotAnimeBoyz | Paha Omena (Bad Apple!! Finnish Cover) | 東方幻想郷　～ Lotus Land Story | wip | osu | 2 | unknown |
| 2616224 | ShinRa-Bansho | Time Paradox | 東方輝針城　～ Double Dealing Character | pending | mania | 2 | unknown |
| 2617851 | A-One | Magic Girl !! | TOHO EUROBEAT VOL.3 (THE EMBODIMENT OF SCARLET DEVIL) | pending | osu | 1 | supported |
| 2618424 | Eru | Pure Furies ~ Whereabouts of the Heart | 東方紺珠伝　～ Legacy of Lunatic Kingdom. | wip | osu | 2 | unknown |
| 2620320 | Rolling Contact | Snow, White, Echo | 東方夢時空　～ Pantasmagria of Dim.Dream | wip | catch | 1 | supported |

## Negative boundary

The following classes are intentionally outside this batch:

- any beatmapset already present in the base catalog;
- IDs 500000–699999 while weekly PR #42 is open, solely to avoid shard conflicts;
- generic `Touhou` / `東方Project` source rows that do not name a concrete recognized game;
- search hits that fail a fresh direct beatmapset refetch, change status, or no longer classify as verified;
- any external-provenance `red_flag` or `ambiguous` result.

Explicit provenance rejects from this run:

- `930037` — U2 Akiyama — **red_flag**
- `1785950` — U2 Akiyama — **red_flag**

## Verification contract

The final branch is required to pass:

- `make check`;
- `make build`;
- `git diff --check`;
- Deep Review in `mode=all`, `scope=added`, with exactly 250 additions and `--forbid-existing-changes`;
- Deep Review live osu! identity: catalog row = fresh API object = public beatmapset-page object for every added ID.
