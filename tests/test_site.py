import json
import tempfile
import unittest
from pathlib import Path

from touhou_osu.catalog import Catalog
from touhou_osu.models import Entry
from touhou_osu.site import build


class SiteTests(unittest.TestCase):
    def test_build_splits_public_and_review_exports(self):
        catalog = Catalog(
            [
                Entry(1, evidence=["manual:verified"], confidence="verified", modes=["osu"]),
                Entry(2, evidence=["osucollector:1402"], confidence="candidate", modes=["mania"]),
                Entry(3, evidence=["manual:excluded"], confidence="excluded"),
            ]
        )
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            stats = build(catalog, output)
            accepted = json.loads((output / "catalog.json").read_text())["entries"]
            review = json.loads((output / "review.json").read_text())["entries"]
            self.assertEqual([item["beatmapset_id"] for item in accepted], [1])
            self.assertEqual([item["beatmapset_id"] for item in review], [2, 3])
            self.assertEqual(stats["total"], 3)
            self.assertTrue((output / "assets" / "app.js").exists())
            self.assertNotIn("{{ACCEPTED_COUNT}}", (output / "index.html").read_text())


if __name__ == "__main__":
    unittest.main()
