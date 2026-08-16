import json
import tempfile
import unittest
from pathlib import Path

from touhou_osu.catalog import Catalog
from touhou_osu.models import CatalogError, Entry


def entry(beatmapset_id=1, **changes):
    values = {
        "beatmapset_id": beatmapset_id,
        "artist": "ZUN",
        "title": "A Sacred Lot",
        "creator": "Mapper",
        "source": "Touhou Project",
        "status": "ranked",
        "modes": ["osu"],
        "evidence": ["osu_source"],
        "confidence": "verified",
        "last_checked": "2026-08-15",
    }
    values.update(changes)
    return Entry(**values)


class CatalogTests(unittest.TestCase):
    def test_round_trip_is_sorted(self):
        catalog = Catalog([entry(20), entry(3)])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "catalog.json"
            catalog.save(path)
            raw = json.loads(path.read_text())
            self.assertEqual([item["beatmapset_id"] for item in raw["entries"]], [3, 20])
            self.assertEqual(len(Catalog.load(path).entries), 2)

    def test_load_rejects_unsorted_source(self):
        payload = {"schema_version": 1, "entries": [entry(2).to_dict(), entry(1).to_dict()]}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "catalog.json"
            path.write_text(json.dumps(payload))
            with self.assertRaisesRegex(CatalogError, "sorted"):
                Catalog.load(path)

    def test_merge_unions_evidence_and_modes(self):
        catalog = Catalog([entry(evidence=["osucollector:1402"], confidence="candidate")])
        merged, changed = catalog.merge(
            entry(evidence=["official_pack:T65"], modes=["mania"], confidence="verified")
        )
        self.assertTrue(changed)
        self.assertEqual(merged.evidence, ["official_pack:T65", "osucollector:1402"])
        self.assertEqual(merged.modes, ["mania", "osu"])
        self.assertEqual(merged.confidence, "verified")

    def test_manual_exclusion_is_sticky(self):
        catalog = Catalog([entry(evidence=["manual:excluded"], confidence="excluded")])
        merged, _ = catalog.merge(entry(evidence=["official_pack:T65"], confidence="verified"))
        self.assertEqual(merged.confidence, "excluded")

    def test_manual_candidate_is_sticky(self):
        catalog = Catalog([entry(evidence=["manual:candidate"], confidence="candidate")])
        merged, _ = catalog.merge(entry(evidence=["tournament:google_sheet:fixture"], confidence="verified"))
        self.assertEqual(merged.confidence, "candidate")
        self.assertIn("manual:candidate", merged.evidence)
        self.assertIn("tournament:google_sheet:fixture", merged.evidence)

    def test_evidence_is_required(self):
        with self.assertRaisesRegex(CatalogError, "evidence"):
            entry(evidence=[]).validate()


if __name__ == "__main__":
    unittest.main()
