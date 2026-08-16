from __future__ import annotations

import argparse
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from touhou_osu.catalog import Catalog
from touhou_osu.cli import command_hydrate
from touhou_osu.models import Entry


class HydrateSourceTests(unittest.TestCase):
    def test_google_sheet_tournament_partial_record_is_hydrated_without_demotion(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            catalog_path = Path(directory) / "catalog.json"
            Catalog(
                [
                    Entry(
                        beatmapset_id=123,
                        evidence=["tournament:google_sheet:fixture"],
                        confidence="verified",
                    )
                ]
            ).save(catalog_path)

            raw = {
                "id": 123,
                "artist": "Fixture Artist",
                "title": "Fixture Title",
                "creator": "Fixture Mapper",
                "source": "Fixture Album",
                "status": "ranked",
                "beatmaps": [{"mode": "osu"}],
                "tags": "",
                "last_updated": "2026-08-01T00:00:00Z",
            }
            args = argparse.Namespace(
                catalog=catalog_path,
                workers=1,
                limit=0,
                write=True,
                strict=True,
            )

            with patch("touhou_osu.cli.get_text", return_value="fixture"), patch(
                "touhou_osu.cli.parse_beatmapset_page", return_value=raw
            ):
                self.assertEqual(command_hydrate(args), 0)

            hydrated = Catalog.load(catalog_path).entries[123]
            self.assertEqual(hydrated.artist, "Fixture Artist")
            self.assertEqual(hydrated.title, "Fixture Title")
            self.assertEqual(hydrated.source, "Fixture Album")
            self.assertEqual(hydrated.status, "ranked")
            self.assertEqual(hydrated.modes, ["osu"])
            self.assertEqual(hydrated.confidence, "verified")
            self.assertIn("tournament:google_sheet:fixture", hydrated.evidence)


if __name__ == "__main__":
    unittest.main()
