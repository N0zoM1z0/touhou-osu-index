import argparse
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from touhou_osu.catalog import Catalog
from touhou_osu.cli import command_discover, command_hydrate
from touhou_osu.models import Entry


class FakeOsuApi:
    responses = {}

    @classmethod
    def from_env(cls):
        return cls()

    def search(self, query, *, max_pages):
        return iter(self.responses[query])


class DiscoveryTests(unittest.TestCase):
    def test_combines_queries_with_existing_collection_evidence_before_classification(self):
        raw = {
            "id": 42,
            "artist": "ShibayanRecords",
            "title": "Fall in the Dark",
            "creator": "mapper",
            "source": "",
            "status": "ranked",
            "tags": "touhou arrangement",
            "beatmaps": [{"mode": "osu"}],
        }
        FakeOsuApi.responses = {"Touhou": [raw], "東方Project": [raw]}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            catalog_path = root / "catalog.json"
            config_path = root / "seeds.json"
            Catalog(
                [Entry(42, artist="ShibayanRecords", evidence=["osucollector:1402"])]
            ).save(catalog_path)
            config_path.write_text(
                json.dumps({"discovery_queries": ["Touhou", "東方Project"]}), encoding="utf-8"
            )
            args = argparse.Namespace(
                catalog=catalog_path,
                config=config_path,
                max_pages=4,
                max_changes=50,
                write=True,
            )

            with patch("touhou_osu.cli.OsuApi", FakeOsuApi):
                self.assertEqual(command_discover(args), 0)

            entry = Catalog.load(catalog_path).entries[42]
            self.assertEqual(entry.confidence, "probable")
            self.assertEqual(
                entry.evidence,
                [
                    "discovery_query:Touhou",
                    "discovery_query:東方Project",
                    "known_touhou_metadata",
                    "mapper_tags",
                    "osucollector:1402",
                ],
            )

    def test_existing_generic_verified_row_does_not_churn(self):
        raw = {
            "id": 42,
            "artist": "IOSYS",
            "title": "Known arrangement",
            "creator": "mapper",
            "source": "Touhou",
            "status": "ranked",
            "tags": "touhou",
            "last_updated": "2026-01-01T00:00:00Z",
            "beatmaps": [{"mode": "osu"}],
        }
        FakeOsuApi.responses = {"Touhou": [raw]}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            catalog_path = root / "catalog.json"
            config_path = root / "seeds.json"
            original = Entry(
                42,
                artist="IOSYS",
                title="Known arrangement",
                creator="mapper",
                source="Touhou",
                status="ranked",
                modes=["osu"],
                evidence=["discovery_query:Touhou", "known_touhou_artist", "mapper_tags", "osu_source"],
                confidence="verified",
                last_checked="2026-01-01",
                osu_last_updated="2026-01-01T00:00:00Z",
            )
            Catalog([original]).save(catalog_path)
            before = catalog_path.read_text(encoding="utf-8")
            config_path.write_text(json.dumps({"discovery_queries": ["Touhou"]}), encoding="utf-8")
            args = argparse.Namespace(
                catalog=catalog_path,
                config=config_path,
                max_pages=4,
                max_changes=50,
                write=True,
            )

            with patch("touhou_osu.cli.OsuApi", FakeOsuApi):
                self.assertEqual(command_discover(args), 0)

            after = catalog_path.read_text(encoding="utf-8")
            entry = Catalog.load(catalog_path).entries[42]
            self.assertEqual(entry.confidence, "verified")
            self.assertEqual(entry.last_checked, "2026-01-01")
            self.assertEqual(before, after)

    def test_caps_meaningful_changes_without_date_only_churn(self):
        def raw(beatmapset_id, *, source="東方永夜抄 ～ Imperishable Night."):
            return {
                "id": beatmapset_id,
                "artist": "ZUN",
                "title": f"Theme {beatmapset_id}",
                "creator": "mapper",
                "source": source,
                "status": "ranked",
                "tags": "touhou",
                "beatmaps": [{"mode": "osu"}],
            }

        FakeOsuApi.responses = {"Touhou": [raw(1, source="unknown"), raw(10), raw(20), raw(30)]}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            catalog_path = root / "catalog.json"
            config_path = root / "seeds.json"
            Catalog(
                [
                    Entry(
                        10,
                        artist="ZUN",
                        title="Theme 10",
                        creator="mapper",
                        source="東方永夜抄 ～ Imperishable Night.",
                        status="ranked",
                        modes=["osu"],
                        evidence=["discovery_query:Touhou", "osu_source"],
                        confidence="verified",
                        last_checked="2020-01-01",
                    )
                ]
            ).save(catalog_path)
            config_path.write_text(json.dumps({"discovery_queries": ["Touhou"]}), encoding="utf-8")
            args = argparse.Namespace(
                catalog=catalog_path,
                config=config_path,
                max_pages=4,
                max_changes=2,
                write=True,
            )

            with patch("touhou_osu.cli.OsuApi", FakeOsuApi):
                self.assertEqual(command_discover(args), 0)

            catalog = Catalog.load(catalog_path)
            self.assertEqual(set(catalog.entries), {10, 20, 30})
            self.assertEqual(catalog.entries[10].last_checked, "2020-01-01")
            self.assertEqual(catalog.entries[20].confidence, "verified")
            self.assertEqual(catalog.entries[30].confidence, "verified")

    def test_hydrates_incomplete_forum_source_without_oauth(self):
        raw = {
            "id": 42,
            "artist": "ZUN",
            "title": "Theme",
            "creator": "mapper",
            "source": "Touhou",
            "status": "ranked",
            "tags": "touhou",
            "last_updated": "2026-01-01T00:00:00Z",
            "beatmaps": [{"mode": "osu"}],
        }
        page = f'<script id="json-beatmapset" type="application/json">{json.dumps(raw)}</script>'
        with tempfile.TemporaryDirectory() as directory:
            catalog_path = Path(directory) / "catalog.json"
            Catalog(
                [Entry(42, evidence=["forum_queue:sd_touhou"], confidence="probable")]
            ).save(catalog_path)
            args = argparse.Namespace(
                catalog=catalog_path,
                workers=2,
                limit=0,
                write=True,
                strict=True,
            )

            with patch("touhou_osu.cli.get_text", return_value=page):
                self.assertEqual(command_hydrate(args), 0)

            entry = Catalog.load(catalog_path).entries[42]
            self.assertEqual(entry.artist, "ZUN")
            self.assertEqual(entry.title, "Theme")
            self.assertEqual(entry.confidence, "probable")
            self.assertIn("osu_source", entry.evidence)


if __name__ == "__main__":
    unittest.main()
