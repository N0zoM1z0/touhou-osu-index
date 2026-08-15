import argparse
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from touhou_osu.catalog import Catalog
from touhou_osu.cli import command_discover
from touhou_osu.models import Entry


class FakeOsuApi:
    responses = {
        "Touhou": [
            {
                "id": 42,
                "artist": "ShibayanRecords",
                "title": "Fall in the Dark",
                "creator": "mapper",
                "source": "",
                "status": "ranked",
                "tags": "touhou arrangement",
                "beatmaps": [{"mode": "osu"}],
            }
        ],
        "東方Project": [
            {
                "id": 42,
                "artist": "ShibayanRecords",
                "title": "Fall in the Dark",
                "creator": "mapper",
                "source": "",
                "status": "ranked",
                "tags": "touhou arrangement",
                "beatmaps": [{"mode": "osu"}],
            }
        ],
    }

    @classmethod
    def from_env(cls):
        return cls()

    def search(self, query, *, max_pages):
        return iter(self.responses[query])


class DiscoveryTests(unittest.TestCase):
    def test_combines_queries_with_existing_collection_evidence_before_classification(self):
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


if __name__ == "__main__":
    unittest.main()
