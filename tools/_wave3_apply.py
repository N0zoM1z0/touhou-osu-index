from __future__ import annotations

import ast
import json
from pathlib import Path


def load_proposals() -> list[dict]:
    tree = ast.parse(Path("tools/_wave3_proposal_audit.py").read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "PROPOSALS" for target in node.targets
        ):
            value = ast.literal_eval(node.value)
            if not isinstance(value, list):
                raise SystemExit("PROPOSALS is not a list")
            return value
    raise SystemExit("PROPOSALS assignment not found")


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if text.count(old) != 1:
        raise SystemExit(f"{path}: expected exactly one patch target, got {text.count(old)}")
    path.write_text(text.replace(old, new), encoding="utf-8")


def patch_sources() -> None:
    path = Path("touhou_osu/sources.py")
    replace_once(path, "import json\nimport re\nimport urllib.parse\n", "import json\nimport re\nimport time\nimport urllib.parse\n")

    marker = "\n\ndef import_wiki_tournament(source: dict) -> list[Entry]:\n"
    batch_code = r'''


def import_official_pack_batch(source: dict) -> list[Entry]:
    """Import many audited official packs sequentially while preserving per-pack evidence."""
    packs = list(source.get("packs", ()))
    if not packs:
        raise RuntimeError("official pack batch must contain at least one pack")

    tags = [str(pack["tag"]) for pack in packs]
    if len(tags) != len(set(tags)):
        raise RuntimeError("official pack batch contains duplicate pack tags")

    delay = float(source.get("delay_seconds", 0))
    if delay < 0:
        raise RuntimeError("official pack batch delay_seconds must be non-negative")

    entries: dict[int, Entry] = {}
    for index, pack in enumerate(packs):
        imported = import_official_pack(pack)
        minimum = int(pack.get("minimum_entries", 1))
        if len(imported) < minimum:
            raise RuntimeError(
                f"official pack {pack['tag']} returned {len(imported)} audited beatmapsets; "
                f"expected at least {minimum}"
            )
        for incoming in imported:
            current = entries.get(incoming.beatmapset_id)
            if current is None:
                entries[incoming.beatmapset_id] = incoming
                continue
            current.evidence = sorted(set(current.evidence) | set(incoming.evidence))
            current.modes = sorted(set(current.modes) | set(incoming.modes))
        if delay and index + 1 < len(packs):
            time.sleep(delay)
    return list(entries.values())
'''
    text = path.read_text(encoding="utf-8")
    if text.count(marker) != 1:
        raise SystemExit("sources.py wiki importer marker changed")
    path.write_text(text.replace(marker, batch_code + marker), encoding="utf-8")

    replace_once(
        path,
        '    if kind == "official_packs":\n        return import_official_pack(source)\n',
        '    if kind == "official_packs":\n        return import_official_pack(source)\n'
        '    if kind == "official_pack_batches":\n        return import_official_pack_batch(source)\n',
    )

    old_tail = '''    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(import_source, kind, source): (kind, source) for kind, source in tasks}
        for future in as_completed(futures):
            kind, source = futures[future]
            label = source.get("name") or source.get("tag") or source.get("edition") or source.get("id")
            imported = future.result()
            minimum = int(source.get("minimum_entries", 1))
            if len(imported) < minimum:
                raise RuntimeError(
                    f"{kind}/{label} returned {len(imported)} beatmapsets; expected at least {minimum}"
                )
            entries.extend(imported)
            reports.append(SourceReport(kind, str(label), source_url(kind, source), len(imported)))
    return entries, sorted(reports, key=lambda item: (item.kind, item.name.casefold()))
'''
    new_tail = '''    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(import_source, kind, source): (kind, source) for kind, source in tasks}
        for future in as_completed(futures):
            kind, source = futures[future]
            label = source.get("name") or source.get("tag") or source.get("edition") or source.get("id")
            imported = future.result()
            minimum = int(source.get("minimum_entries", 1))
            if len(imported) < minimum:
                raise RuntimeError(
                    f"{kind}/{label} returned {len(imported)} beatmapsets; expected at least {minimum}"
                )
            entries.extend(imported)
            reports.append(SourceReport(kind, str(label), source_url(kind, source), len(imported)))

    # Audited pack batches deliberately run after the concurrent source pool.
    # Their canonical osu! pack pages are paced sequentially to avoid turning
    # broad Spotlight coverage into rate-limit-sensitive CI.
    for source in config.get("official_pack_batches", []):
        kind = "official_pack_batches"
        label = source.get("name") or source.get("id")
        imported = import_source(kind, source)
        minimum = int(source.get("minimum_entries", 1))
        if len(imported) < minimum:
            raise RuntimeError(
                f"{kind}/{label} returned {len(imported)} beatmapsets; expected at least {minimum}"
            )
        entries.extend(imported)
        reports.append(SourceReport(kind, str(label), source_url(kind, source), len(imported)))

    return entries, sorted(reports, key=lambda item: (item.kind, item.name.casefold()))
'''
    replace_once(path, old_tail, new_tail)


def patch_hydrate() -> None:
    replace_once(
        Path("touhou_osu/cli.py"),
        '    prefixes = ("forum_queue:", "tournament_candidate:", "tournament:google_sheet:")\n',
        '    prefixes = (\n'
        '        "forum_queue:",\n'
        '        "tournament_candidate:",\n'
        '        "tournament:google_sheet:",\n'
        '        "official_pack:",\n'
        '        "official_pack_item:",\n'
        '    )\n',
    )


def patch_config(proposals: list[dict]) -> None:
    packs = [
        {
            "tag": item["tag"],
            "name": item["name"],
            "verified_ids": item["ids"],
            "minimum_source_entries": item["raw"],
            "minimum_entries": len(item["ids"]),
        }
        for item in proposals
    ]
    batch = {
        "id": "official-pack-wave3",
        "name": "Audited official Touhou pack items (wave 3)",
        "url": "https://osu.ppy.sh/beatmaps/packs",
        "delay_seconds": 1.05,
        "minimum_entries": 84,
        "packs": packs,
    }
    batch_json = json.dumps(batch, ensure_ascii=False, indent=2)
    batch_json = "\n".join("    " + line for line in batch_json.splitlines())
    section = '  "official_pack_batches": [\n' + batch_json + '\n  ],\n'

    path = Path("config/seeds.json")
    text = path.read_text(encoding="utf-8")
    official = text.index('  "official_packs": [')
    anchor = '\n  ],\n  "osu_collector_tournaments": ['
    position = text.index(anchor, official)
    replacement = '\n  ],\n' + section + '  "osu_collector_tournaments": ['
    path.write_text(text[:position] + replacement + text[position + len(anchor):], encoding="utf-8")


def patch_catalog() -> None:
    path = Path("data/catalog.json")
    catalog = json.loads(path.read_text(encoding="utf-8"))
    matches = [item for item in catalog["entries"] if int(item["beatmapset_id"]) == 4135]
    if len(matches) != 1:
        raise SystemExit(f"expected exactly one catalog entry 4135, found {len(matches)}")
    item = matches[0]
    if item.get("confidence") != "verified" or "osu_source" not in item.get("evidence", []):
        raise SystemExit("4135 baseline changed; refusing blind exclusion")
    item["evidence"] = sorted(set(item["evidence"]) | {"manual:excluded"}, key=str.casefold)
    item["confidence"] = "excluded"
    path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def patch_tests() -> None:
    path = Path("tests/test_sources.py")
    text = path.read_text(encoding="utf-8")
    old = "    import_official_pack,\n    parse_beatmap_links,"
    if text.count(old) != 1:
        raise SystemExit("test_sources import target changed")
    text = text.replace(old, "    import_official_pack,\n    import_official_pack_batch,\n    parse_beatmap_links,")
    if "from touhou_osu.models import Entry\n" not in text:
        text = text.replace("from unittest.mock import patch\n\n", "from unittest.mock import patch\n\nfrom touhou_osu.models import Entry\n")
    marker = '\n\nif __name__ == "__main__":\n'
    tests = r'''

    @patch("touhou_osu.sources.time.sleep")
    @patch("touhou_osu.sources.import_official_pack")
    def test_official_pack_batch_merges_duplicate_membership_evidence(self, mock_import, mock_sleep):
        mock_import.side_effect = [
            [Entry(1, modes=["osu"], evidence=["official_pack_item:R1"], confidence="verified")],
            [
                Entry(1, modes=["taiko"], evidence=["official_pack_item:R2"], confidence="verified"),
                Entry(2, evidence=["official_pack_item:R2"], confidence="verified"),
            ],
        ]
        entries = import_official_pack_batch(
            {
                "packs": [
                    {"tag": "R1", "minimum_entries": 1},
                    {"tag": "R2", "minimum_entries": 2},
                ],
                "delay_seconds": 0.5,
            }
        )
        by_id = {entry.beatmapset_id: entry for entry in entries}
        self.assertEqual(set(by_id), {1, 2})
        self.assertEqual(by_id[1].evidence, ["official_pack_item:R1", "official_pack_item:R2"])
        self.assertEqual(by_id[1].modes, ["osu", "taiko"])
        mock_sleep.assert_called_once_with(0.5)

    def test_official_pack_batch_rejects_duplicate_tags(self):
        with self.assertRaisesRegex(RuntimeError, "duplicate pack tags"):
            import_official_pack_batch({"packs": [{"tag": "R1"}, {"tag": "R1"}]})
'''
    if text.count(marker) != 1:
        raise SystemExit("test_sources footer target changed")
    path.write_text(text.replace(marker, tests + marker), encoding="utf-8")

    path = Path("tests/test_hydrate_sources.py")
    text = path.read_text(encoding="utf-8")
    marker = '\n\nif __name__ == "__main__":\n'
    test = r'''

    def test_official_pack_item_partial_record_is_hydrated_without_demotion(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            catalog_path = Path(directory) / "catalog.json"
            Catalog(
                [
                    Entry(
                        beatmapset_id=456,
                        artist="Pack Artist",
                        title="Pack Title",
                        evidence=["official_pack_item:Rfixture"],
                        confidence="verified",
                    )
                ]
            ).save(catalog_path)

            raw = {
                "id": 456,
                "artist": "Pack Artist",
                "title": "Pack Title",
                "creator": "Fixture Mapper",
                "source": "東方妖々夢 ～ Perfect Cherry Blossom",
                "status": "ranked",
                "beatmaps": [{"mode": "catch"}],
                "tags": "touhou",
                "last_updated": "2026-08-01T00:00:00Z",
            }
            args = argparse.Namespace(catalog=catalog_path, workers=1, limit=0, write=True, strict=True)
            with patch("touhou_osu.cli.get_text", return_value="fixture"), patch(
                "touhou_osu.cli.parse_beatmapset_page", return_value=raw
            ):
                self.assertEqual(command_hydrate(args), 0)

            hydrated = Catalog.load(catalog_path).entries[456]
            self.assertEqual(hydrated.source, "東方妖々夢 ～ Perfect Cherry Blossom")
            self.assertEqual(hydrated.status, "ranked")
            self.assertEqual(hydrated.confidence, "verified")
            self.assertIn("official_pack_item:Rfixture", hydrated.evidence)
'''
    if text.count(marker) != 1:
        raise SystemExit("test_hydrate_sources footer target changed")
    path.write_text(text.replace(marker, test + marker), encoding="utf-8")

    path = Path("tests/test_classifier.py")
    text = path.read_text(encoding="utf-8")
    marker = "    def test_known_artist_alone_stays_candidate(self):\n"
    test = '''    def test_manual_exclusion_beats_explicit_touhou_source(self):\n        item = Entry(1, source="Touhou", evidence=["osu_source", "manual:excluded"], confidence="verified")\n        apply_classification(item)\n        self.assertEqual(item.confidence, "excluded")\n\n'''
    if text.count(marker) != 1:
        raise SystemExit("test_classifier insertion target changed")
    path.write_text(text.replace(marker, test + marker), encoding="utf-8")


def patch_sources_doc() -> None:
    path = Path("SOURCES.md")
    text = path.read_text(encoding="utf-8")
    marker = "\n## Tournament pools\n"
    addition = '''

### Audited official pack batches

Large mixed-pack audits can be declared as `official_pack_batches`. Each nested
pack still has its own canonical tag, raw-size floor, frozen `verified_ids`
allowlist and `official_pack_item:<tag>` evidence, but the batch is fetched
sequentially after the normal concurrent source pool. This keeps broad
Spotlight coverage reproducible without making `audit-sources` depend on dozens
of simultaneous osu! pack-page requests.

The August 2026 third-wave batch covers A2 Secret Seven, FQ70 BLANKFIELD,
FQ66 A-One, one Touhou item from FQ40 LeaF, and 38 modern Beatmap Spotlight
packs. Across 91 audited pack memberships it emits 84 unique Touhou beatmapsets;
47 were absent from every previously configured live source. See
[`docs/source-audit-2026-08-official-packs-wave3.md`](docs/source-audit-2026-08-official-packs-wave3.md).
'''
    if text.count(marker) != 1:
        raise SystemExit("SOURCES tournament marker changed")
    path.write_text(text.replace(marker, addition + marker), encoding="utf-8")


def write_audit_doc(proposals: list[dict]) -> None:
    rows = []
    for item in proposals:
        rows.append(
            f"| `{item['tag']}` | {item['name']} | {item['raw']} | {len(item['ids'])} | "
            f"`{', '.join(map(str, item['ids']))}` |"
        )
    text = f'''# Official pack audit — 2026-08 wave 3

This wave extends the per-item official-pack policy to an older album pack,
Featured Artist mini-packs and modern Beatmap Spotlights. Spotlight membership
alone is **not** treated as Touhou evidence; every emitted ID is frozen in an
explicit allowlist and retains the evidence tag of the exact canonical pack it
came from.

## Discovery scope

A read-only osu! API scan enumerated 154 Featured packs and 342 chart (`R`)
packs. The Spotlight pass reviewed all 56 chart packs dated 2020 or later.
Potential rows were first intersected with the canonical catalog, explicit
Touhou source metadata and known Touhou artists, then individually narrowed.

The final proposal contains **42 canonical pack pages**, **91 audited pack
memberships**, and **84 unique beatmapsets**. Against the pre-wave live source
universe (6,796 source records / 41 sources / 3,022 unique beatmapsets):

- **47** IDs were absent from every configured live source and from the
  canonical catalog;
- **21** existing candidate/probable IDs gain audited official-pack evidence;
- **16** existing verified IDs gain redundant official provenance.

## Album / Featured Artist decisions

- `A2` Secret Seven: **6/7**. SYNC.ART'S official discography identifies
  `I will -Short-` as the album's original composition and the remaining six
  tracks as Touhou arrangements. Beatmapset `4135` is therefore not trusted;
  this audit also corrects its existing false-positive `osu_source` status with
  `manual:excluded`.
- `FQ70` BLANKFIELD: **4/4** audited Touhou items.
- `FQ66` A-One: **6/6** audited Touhou items; all six were missing from the
  prior source universe.
- `FQ40` LeaF: **1/3**. Only `Arianrhod` (`1128939`, EoSD) is included;
  `Mopemope` and `I` are not Touhou works.

Primary/canonical references include:

- https://syncarts.jp/cd/etclist.htm
- https://osu.ppy.sh/beatmaps/artists/148
- https://osu.ppy.sh/beatmaps/artists/28
- https://osu.ppy.sh/beatmaps/packs/A2
- https://osu.ppy.sh/beatmaps/packs/FQ70
- https://osu.ppy.sh/beatmaps/packs/FQ66
- https://osu.ppy.sh/beatmaps/packs/FQ40

## Modern Spotlight allowlists

Only per-item reviewed Touhou rows are emitted; no Spotlight pack is trusted as
a whole. Specific recognized Touhou game sources follow the repository's
existing exact-source rule. Generic `Touhou` source rows were separately
cross-checked because A2 demonstrates that mapper-entered source metadata can
be wrong. Representative checks include FELT `BRIGHTEST WAY`, Halozy
`Genryuu Kaiko` / `Paranoid Lost`, LeaF `Calamity Fortune`, tsunamix
`Period.`, Kurokotei `Galaxy Collapse`, 3L `Amoritachite Kami to Miyu`, FELT
`Goldrop`, IOSYS `Endless Tewi-ma Park`, Chata `Remind`, and Meramipop
`Rakujitsu Romance` against artist/album provenance.

| Pack | Name | Raw | Audited Touhou | Frozen beatmapset IDs |
| --- | --- | ---: | ---: | --- |
{chr(10).join(rows)}

## Rate-limit and fail-closed design

The 42 pack pages are grouped under one `official_pack_batches` source. Nested
packs still use the existing `import_official_pack` safety checks: duplicate
allowlist IDs are rejected, the live raw pack must meet its
`minimum_source_entries` floor, and every frozen ID must still exist upstream.
The batch imports nested packs sequentially with a 1.05-second delay, merges
duplicate Spotlight memberships while unioning their per-pack evidence, and
fails its outer 84-entry floor if coverage shrinks.

`hydrate` also recognizes `official_pack:` and `official_pack_item:` evidence,
so newly discovered pack-only records can obtain public osu! source/status/mode
metadata without OAuth while keeping their audited verified evidence.

## Reproduction

Before the PR is opened, the branch runs unit tests, `make check`, `make build`,
a live exact batch import, a full source audit, a complete `import-seeds`
simulation, and boundary checks for `4135`, `605290`, and `495283`. Temporary
scan/apply tooling is removed from the final diff.
'''
    Path("docs/source-audit-2026-08-official-packs-wave3.md").write_text(text, encoding="utf-8")


def main() -> None:
    proposals = load_proposals()
    if len(proposals) != 42:
        raise SystemExit(f"expected 42 proposal packs, got {len(proposals)}")
    unique_ids = {beatmapset_id for item in proposals for beatmapset_id in item["ids"]}
    memberships = sum(len(item["ids"]) for item in proposals)
    if len(unique_ids) != 84 or memberships != 91:
        raise SystemExit(f"proposal totals changed: unique={len(unique_ids)} memberships={memberships}")

    patch_sources()
    patch_hydrate()
    patch_config(proposals)
    patch_catalog()
    patch_tests()
    patch_sources_doc()
    write_audit_doc(proposals)


if __name__ == "__main__":
    main()
