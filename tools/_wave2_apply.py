from __future__ import annotations

import json
import re
from pathlib import Path


PACKS = [
    {
        "tag": "A51",
        "name": "Rin Pack",
        "verified_ids": [974872, 985478, 985780, 991960, 993507, 996256, 1001360, 1006601, 1013620, 1014593, 1019506, 1022069, 1022358],
        "minimum_source_entries": 13,
    },
    {
        "tag": "A18",
        "name": "Demetori Pack",
        "verified_ids": [7084, 7158, 7940, 9641, 9960, 13204, 13223, 14309, 15393, 20125, 20686, 20949, 32574, 34484, 42234, 52401, 62764, 107565, 133693, 178777, 192900, 248162, 320299],
        "minimum_source_entries": 23,
    },
    {
        "tag": "A33",
        "name": "FELT Pack",
        "verified_ids": [44346, 51145, 105244, 129534, 161109, 297409, 327587, 403065, 407175],
        "minimum_source_entries": 11,
    },
    {
        "tag": "A32",
        "name": "Halozy Pack",
        "verified_ids": [25338, 34308, 39537, 63563, 64278, 75890, 114220, 372358, 408302, 419244],
        "minimum_source_entries": 11,
    },
    {
        "tag": "A16",
        "name": "Yuuhei Satellite Pack",
        "verified_ids": [20780, 21233, 24706, 28479, 38106, 40536, 42242, 42480, 44300, 44518, 47065, 52879, 58470, 59133, 60950, 63660, 66190, 67506, 68952, 69681, 70158, 72818, 80747, 86602, 91791, 92509, 95839, 110985, 122416, 138420, 145885, 148980, 150112, 174414],
        "minimum_source_entries": 34,
    },
    {
        "tag": "A85",
        "name": "Yuuhei Satellite & Catharsis Pack 2",
        "verified_ids": [82326, 92507, 119891, 158128, 174417, 195808, 218633, 223960, 234455, 250309, 252385, 363504, 377281, 398921, 420265],
        "minimum_source_entries": 22,
    },
    {
        "tag": "A86",
        "name": "Yuuhei Satellite & Catharsis Pack 3",
        "verified_ids": [291264, 370545, 392495, 428233, 434397, 440980, 455092, 467315, 483527, 657870, 704050, 734241, 744222, 778920, 808409, 858672],
        "minimum_source_entries": 22,
    },
    {
        "tag": "A87",
        "name": "Yuuhei Satellite & Catharsis Pack 4",
        "verified_ids": [552002, 747507, 887451, 935811, 969563, 982006, 1030134, 1053613, 1122983, 1271180, 1353531, 1376085, 1391331, 1461660, 1508174, 1550119, 1579161, 1822334, 1852871, 1330002],
        "minimum_source_entries": 22,
    },
    {
        "tag": "A23",
        "name": "Silver Forest Pack",
        "verified_ids": [1559, 2626, 6509, 7373, 8393, 8523, 9002, 9489, 9534, 11543, 11668, 12504, 12508, 13132, 13574, 13953, 14050, 15362, 17896, 18814, 20795, 21927, 22043, 22221, 23065, 23251, 23665, 26860, 27039, 28066],
        "minimum_source_entries": 30,
    },
]

WITHHELD = {
    154056,
    206284,
    223048,
    234999,
    242360,
    247319,
    250337,
    288997,
    320155,
    347460,
    349810,
    352351,
    491057,
    495283,
    562169,
    605290,
    1463878,
    1621390,
}


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if text.count(old) != 1:
        raise SystemExit(f"{path}: expected exactly one patch target, found {text.count(old)}")
    path.write_text(text.replace(old, new), encoding="utf-8")


def patch_sources() -> None:
    path = Path("touhou_osu/sources.py")
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(r"def import_official_pack\(source: dict\) -> list\[Entry\]:\n.*?\n\ndef import_wiki_tournament", re.S)
    replacement = '''def import_official_pack(source: dict) -> list[Entry]:
    tag = source["tag"]
    url = source.get("url", f"https://osu.ppy.sh/beatmaps/packs/{tag}")
    links = parse_beatmap_links(get_text(url))

    verified_ids = source.get("verified_ids")
    if verified_ids is None:
        evidence = f"official_pack:{tag}"
    else:
        verified_ids = [int(value) for value in verified_ids]
        if len(verified_ids) != len(set(verified_ids)):
            raise RuntimeError(f"official pack {tag} contains duplicate verified_ids")

        minimum_source_entries = int(source.get("minimum_source_entries", len(verified_ids)))
        if len(links) < minimum_source_entries:
            raise RuntimeError(
                f"official pack {tag} returned {len(links)} raw beatmapsets; "
                f"expected at least {minimum_source_entries}"
            )

        by_id = {item["id"]: item for item in links}
        missing = [beatmapset_id for beatmapset_id in verified_ids if beatmapset_id not in by_id]
        if missing:
            raise RuntimeError(
                f"official pack {tag} no longer contains audited beatmapsets: {missing}"
            )
        links = [by_id[beatmapset_id] for beatmapset_id in verified_ids]
        evidence = f"official_pack_item:{tag}"

    return [
        Entry(
            beatmapset_id=item["id"],
            artist=item["artist"],
            title=item["title"],
            modes=[item["mode"]] if item["mode"] else [],
            evidence=[evidence],
            confidence="verified",
            last_checked=date.today().isoformat(),
        )
        for item in links
    ]


def import_wiki_tournament'''
    updated, count = pattern.subn(replacement, text)
    if count != 1:
        raise SystemExit(f"sources.py: expected one import_official_pack block, replaced {count}")
    path.write_text(updated, encoding="utf-8")


def patch_classifier() -> None:
    replace_once(
        Path("touhou_osu/classifier.py"),
        'if any(item.startswith(("official_pack:", "tournament:", "tmc:")) for item in evidence):',
        'if any(\n        item.startswith(("official_pack:", "official_pack_item:", "tournament:", "tmc:"))\n        for item in evidence\n    ):',
    )


def patch_tests() -> None:
    path = Path("tests/test_sources.py")
    text = path.read_text(encoding="utf-8")
    old = "    import_forum_queue,\n    parse_beatmap_links,"
    if text.count(old) != 1:
        raise SystemExit("test_sources.py import target changed")
    text = text.replace(old, "    import_forum_queue,\n    import_official_pack,\n    parse_beatmap_links,")
    marker = '\n\nif __name__ == "__main__":\n'
    if text.count(marker) != 1:
        raise SystemExit("test_sources.py footer target changed")
    tests = r'''

    @patch("touhou_osu.sources.get_text")
    def test_audited_official_pack_only_emits_verified_ids(self, mock_get_text):
        mock_get_text.return_value = """
        <a href="https://osu.ppy.sh/beatmapsets/101#osu/1">
          <span class="beatmap-pack-items__artist">Touhou Artist</span>
          <span class="beatmap-pack-items__title">Keep A</span>
        </a>
        <a href="https://osu.ppy.sh/beatmapsets/202#osu/2">
          <span class="beatmap-pack-items__artist">Original Artist</span>
          <span class="beatmap-pack-items__title">Do Not Trust</span>
        </a>
        <a href="https://osu.ppy.sh/beatmapsets/303#osu/3">
          <span class="beatmap-pack-items__artist">Touhou Artist</span>
          <span class="beatmap-pack-items__title">Keep B</span>
        </a>
        """
        entries = import_official_pack(
            {
                "tag": "A99",
                "verified_ids": [303, 101],
                "minimum_source_entries": 3,
            }
        )
        self.assertEqual([entry.beatmapset_id for entry in entries], [303, 101])
        self.assertTrue(all(entry.evidence == ["official_pack_item:A99"] for entry in entries))
        self.assertTrue(all(entry.confidence == "verified" for entry in entries))

    @patch("touhou_osu.sources.get_text")
    def test_audited_official_pack_fails_if_verified_id_disappears(self, mock_get_text):
        mock_get_text.return_value = """
        <a href="https://osu.ppy.sh/beatmapsets/101#osu/1">
          <span class="beatmap-pack-items__artist">Artist</span>
          <span class="beatmap-pack-items__title">Title</span>
        </a>
        """
        with self.assertRaisesRegex(RuntimeError, "no longer contains audited beatmapsets"):
            import_official_pack({"tag": "A99", "verified_ids": [101, 202]})

    @patch("touhou_osu.sources.get_text")
    def test_audited_official_pack_enforces_raw_source_floor(self, mock_get_text):
        mock_get_text.return_value = """
        <a href="https://osu.ppy.sh/beatmapsets/101#osu/1">
          <span class="beatmap-pack-items__artist">Artist</span>
          <span class="beatmap-pack-items__title">Title</span>
        </a>
        """
        with self.assertRaisesRegex(RuntimeError, "raw beatmapsets"):
            import_official_pack(
                {
                    "tag": "A99",
                    "verified_ids": [101],
                    "minimum_source_entries": 2,
                }
            )

    @patch("touhou_osu.sources.get_text")
    def test_audited_official_pack_rejects_duplicate_verified_ids(self, mock_get_text):
        mock_get_text.return_value = """
        <a href="https://osu.ppy.sh/beatmapsets/101#osu/1">
          <span class="beatmap-pack-items__artist">Artist</span>
          <span class="beatmap-pack-items__title">Title</span>
        </a>
        """
        with self.assertRaisesRegex(RuntimeError, "duplicate verified_ids"):
            import_official_pack({"tag": "A99", "verified_ids": [101, 101]})
'''
    path.write_text(text.replace(marker, tests + marker), encoding="utf-8")

    path = Path("tests/test_classifier.py")
    text = path.read_text(encoding="utf-8")
    anchor = '''    def test_official_pack_is_verified(self):
        item = Entry(1, evidence=["official_pack:FQ55"], confidence="candidate")
        apply_classification(item)
        self.assertEqual(item.confidence, "verified")
'''
    if text.count(anchor) != 1:
        raise SystemExit("test_classifier.py official-pack test target changed")
    addition = anchor + '''
    def test_audited_official_pack_item_is_verified(self):
        item = Entry(1, evidence=["official_pack_item:A33"], confidence="candidate")
        apply_classification(item)
        self.assertEqual(item.confidence, "verified")

    def test_manual_exclusion_beats_audited_official_pack_item(self):
        item = Entry(
            1,
            evidence=["official_pack_item:A86", "manual:excluded"],
            confidence="verified",
        )
        apply_classification(item)
        self.assertEqual(item.confidence, "excluded")
'''
    path.write_text(text.replace(anchor, addition), encoding="utf-8")


def patch_config() -> None:
    path = Path("config/seeds.json")
    config = json.loads(path.read_text(encoding="utf-8"))
    tags = {source["tag"] for source in config["official_packs"]}
    incoming = {source["tag"] for source in PACKS}
    duplicate = tags & incoming
    if duplicate:
        raise SystemExit(f"audited pack tags already configured: {sorted(duplicate)}")
    for source in PACKS:
        configured = dict(source)
        configured["minimum_entries"] = len(source["verified_ids"])
        config["official_packs"].append(configured)
    path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def patch_catalog() -> None:
    path = Path("data/catalog.json")
    catalog = json.loads(path.read_text(encoding="utf-8"))
    matches = [item for item in catalog["entries"] if int(item["beatmapset_id"]) == 605290]
    if len(matches) != 1:
        raise SystemExit(f"expected exactly one catalog entry 605290, found {len(matches)}")
    item = matches[0]
    if item["confidence"] != "verified" or "tournament:1432" not in item["evidence"]:
        raise SystemExit("605290 baseline changed; refusing blind exclusion")
    item["evidence"] = sorted(set(item["evidence"]) | {"manual:excluded"}, key=str.casefold)
    item["confidence"] = "excluded"
    path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def patch_sources_doc() -> None:
    path = Path("SOURCES.md")
    text = path.read_text(encoding="utf-8")
    start = text.index("## Official osu! packs\n")
    end = text.index("## Tournament pools\n")
    section = '''## Official osu! packs

Whole-pack Touhou/theme packs use `official_pack:<tag>` and remain verified membership evidence. Mixed Featured Artist packs are different: they are imported only through an explicit, reviewed `verified_ids` allowlist and receive `official_pack_item:<tag>` evidence. The importer also checks the live raw pack size and fails closed if an audited ID disappears, so later upstream additions are never silently trusted.

| Pack | Canonical tag | Raw records | Audited verified records |
| --- | --- | ---: | ---: |
| [Touhou Chart](https://osu.ppy.sh/beatmaps/packs/R29) | R29 | 21 | whole pack |
| [Bad Apple!! Pack - Seductive Temptation](https://osu.ppy.sh/beatmaps/packs/T54) | T54 | 15 | whole pack |
| [Touhou Music Pack](https://osu.ppy.sh/beatmaps/packs/T65) | T65 | 20 | whole pack |
| [The Embodiment of Scarlet Devil Pack](https://osu.ppy.sh/beatmaps/packs/T96) | T96 | 15 | whole pack |
| [Touhou Pack](https://osu.ppy.sh/beatmaps/packs/T106) | T106 | 8 | whole pack |
| [Stan Touhou Music Pack](https://osu.ppy.sh/beatmaps/packs/FQ55) | FQ55 | 7 | whole pack |
| [UNDEAD CORPORATION Touhou pack](https://osu.ppy.sh/beatmaps/packs/FQ35) | FQ35 | 8 | whole pack |
| [Rin Pack](https://osu.ppy.sh/beatmaps/packs/A51) | A51 | 13 | 13 |
| [Demetori Pack](https://osu.ppy.sh/beatmaps/packs/A18) | A18 | 23 | 23 |
| [FELT Pack](https://osu.ppy.sh/beatmaps/packs/A33) | A33 | 11 | 9 |
| [Halozy Pack](https://osu.ppy.sh/beatmaps/packs/A32) | A32 | 11 | 10 |
| [Yuuhei Satellite Pack](https://osu.ppy.sh/beatmaps/packs/A16) | A16 | 34 | 34 |
| [Yuuhei Satellite & Catharsis Pack 2](https://osu.ppy.sh/beatmaps/packs/A85) | A85 | 22 | 15 |
| [Yuuhei Satellite & Catharsis Pack 3](https://osu.ppy.sh/beatmaps/packs/A86) | A86 | 22 | 16 |
| [Yuuhei Satellite & Catharsis Pack 4](https://osu.ppy.sh/beatmaps/packs/A87) | A87 | 22 | 20 |
| [Silver Forest Pack](https://osu.ppy.sh/beatmaps/packs/A23) | A23 | 30 | 30 |

The nine audited artist packs contain 188 memberships in total. Exactly 170 were individually verified as Touhou compositions; 18 original, Kantai Collection, or Seihou memberships are deliberately withheld. See [`docs/source-audit-2026-08-artist-packs-wave2.md`](docs/source-audit-2026-08-artist-packs-wave2.md) for the item-level decisions and provenance.

'''
    path.write_text(text[:start] + section + text[end:], encoding="utf-8")


def write_audit_doc() -> None:
    text = '''# Official artist-pack audit — 2026-08 wave 2

This audit reviews every beatmapset membership in nine official osu! Featured Artist packs instead of trusting circle/artist identity as proof of Touhou provenance.

## Import policy

`verified_ids` is an explicit per-pack allowlist. For these mixed artist packs the importer:

- fetches the live canonical osu! pack page;
- requires the raw pack to meet `minimum_source_entries`;
- requires every audited ID to still be present;
- emits only the allowlisted IDs with `official_pack_item:<tag>` verified evidence;
- ignores future/unreviewed pack additions until a new audit updates the allowlist.

This preserves the repository rule that a known Touhou circle alone is not verification.

## Results

| Pack | Raw | Verified | Withheld | Current candidate → verified | Current missing verified IDs |
| --- | ---: | ---: | ---: | ---: | ---: |
| A51 Rin | 13 | 13 | 0 | 7 | 0 |
| A18 Demetori | 23 | 23 | 0 | 19 | 0 |
| A33 FELT | 11 | 9 | 2 | 5 | 0 |
| A32 Halozy | 11 | 10 | 1 | 8 | 0 |
| A16 Yuuhei Satellite | 34 | 34 | 0 | 32 | 0 |
| A85 Yuuhei Satellite & Catharsis 2 | 22 | 15 | 7 | 14 | 0 |
| A86 Yuuhei Satellite & Catharsis 3 | 22 | 16 | 6 | 12 | 0 |
| A87 Yuuhei Satellite & Catharsis 4 | 22 | 20 | 2 | 14 | 0 |
| A23 Silver Forest | 30 | 30 | 0 | 23 | 2 |
| **Total** | **188** | **170** | **18** | **134** | **2** |

The other 34 audited Touhou memberships are already verified in the current catalog. The two currently missing verified IDs are `1559` and `2626`, both Silver Forest - Tsurupettan.

## Withheld memberships

These are intentionally not emitted as trusted pack evidence:

- A33 FELT: `206284` **In my room** and `320155` **Clean** — original compositions.
- A32 Halozy: `352351` **Snow Changes to a Beat Again** — original composition by sumijun.
- A85: `154056`, `223048`, `234999`, `242360`, `250337`, `288997` — Kantai Collection; `247319` **Handle Nigitte** — original composition by kamase-tora.
- A86: `347460`, `349810`, `491057`, `562169`, `605290` — Kantai Collection; `495283` **Zouka de Arou to Shita Mono** — arrangement of `二色蓮花蝶 ～ Ancients` from Seihou/Shuusou Gyoku, so it stays candidate under the existing Seihou boundary instead of being promoted as Touhou.
- A87: `1463878` **Daichi ni Saku Senritsu** — original composition by Iceon; `1621390` **Yureru Koi wa Nami no Gotoku (Short Ver.)** — Kantai Collection.

Sixteen of these eighteen were absent from the current catalog and are kept out. `495283` remains candidate. `605290` was already verified only because of `tournament:1432`; this audit found it is actually the Kantai Collection carrier Wo-class image song **Zetsubou no Fuchi**, so this PR adds `manual:excluded` while retaining the old tournament provenance for transparency.

## Cross-check provenance

Primary/canonical pack pages:

- https://osu.ppy.sh/beatmaps/packs/A51
- https://osu.ppy.sh/beatmaps/packs/A18
- https://osu.ppy.sh/beatmaps/packs/A33
- https://osu.ppy.sh/beatmaps/packs/A32
- https://osu.ppy.sh/beatmaps/packs/A16
- https://osu.ppy.sh/beatmaps/packs/A85
- https://osu.ppy.sh/beatmaps/packs/A86
- https://osu.ppy.sh/beatmaps/packs/A87
- https://osu.ppy.sh/beatmaps/packs/A23

The live audit also fetched every one of the 188 public beatmapset pages and recorded its current `source` and tags. Clear Touhou game/source metadata was accepted directly; ambiguous entries were cross-checked against album/artist provenance rather than inferred from the circle name.

Selected ambiguity checks:

- FELT `Clean`: https://vgmdb.net/album/52671 (`Original Track`); `In my room`: https://www.suruga-ya.jp/product/detail/186124615 (`Original Track`).
- Halozy `Snow Changes to a Beat Again`: https://halozy.bandcamp.com/album/snow-melody plus album credits at https://thwiki.cc/Snow_Melody_Instrumental identify track 1 as a sumijun composition rather than a ZUN arrangement.
- Yuuhei/Katharsis originals and Kantai Collection songs were checked against the circle's own discography, including https://www.yuuhei-satellite.jp/2939, https://www.yuuhei-satellite.jp/5882, https://www.yuuhei-satellite.jp/720, and https://www.yuuhei-satellite.jp/5871.
- `Zouka de Arou to Shita Mono`: the circle's official page identifies `二色蓮花蝶 ～ Ancients` as its original: https://www.yuuhei-satellite.jp/5871. osu! metadata identifies this mapping with Seihou, and the repository already treats ZUN-composed Seihou material as candidate-only.
- Silver Forest ambiguity checks include `Tsurupettan` → `竹取飛翔 ～ Lunatic Princess`, `Eternally Unreachable Distance` → `月まで届け、不死の煙`, `1000 Phantasm` → `千年幻想郷`, `Marisa Spark` → `恋色マスタースパーク`, `Phantasm Brigade` → `ネクロファンタジア`, and `萃夢想歌` → `萃夢想`/`東方萃夢想`; see https://thwiki.cc/東方萃奏楽, https://thwiki.cc/東方蒼天歌, https://thwiki.cc/Silver_Forest_2006-2012_BESTⅠ, and https://thwiki.cc/歌词:萃夢想歌.

## Verification

Before the PR is opened, the branch runs fixture tests, `make check`, `make build`, imports each live audited pack and verifies its exact allowlist, audits every configured source and safety floor, and simulates a complete `import-seeds` merge. Temporary audit/apply workflows are removed from the final diff.
'''
    Path("docs/source-audit-2026-08-artist-packs-wave2.md").write_text(text, encoding="utf-8")


def sanity_check_decisions() -> None:
    verified = [value for pack in PACKS for value in pack["verified_ids"]]
    if len(verified) != 170 or len(set(verified)) != 170:
        raise SystemExit(f"expected exactly 170 unique verified IDs, got {len(verified)}/{len(set(verified))}")
    overlap = set(verified) & WITHHELD
    if overlap:
        raise SystemExit(f"verified/withheld overlap: {sorted(overlap)}")
    if len(WITHHELD) != 18:
        raise SystemExit(f"expected 18 withheld IDs, got {len(WITHHELD)}")


def main() -> None:
    sanity_check_decisions()
    patch_sources()
    patch_classifier()
    patch_tests()
    patch_config()
    patch_catalog()
    patch_sources_doc()
    write_audit_doc()


if __name__ == "__main__":
    main()
