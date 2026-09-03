import unittest
from unittest.mock import patch

from touhou_osu.catalog import Catalog
from touhou_osu.http import HttpError
from touhou_osu.models import Entry
from touhou_osu.provenance import (
    audit_entry,
    new_generic_verification_violations,
    query_thbwiki,
    query_touhoudb,
)


class ProvenanceTests(unittest.TestCase):
    def test_touhoudb_exact_arrangement_supports(self):
        entry = Entry(1, artist="Shibayan feat. Tsubaki Ichimatsu", title="GAZE IT", source="Touhou")
        payload = {
            "items": [
                {
                    "id": 123,
                    "name": "GAZE IT",
                    "artistString": "Shibayan feat. Tsubaki Ichimatsu",
                    "artists": [],
                    "status": "Finished",
                    "songType": "Arrangement",
                    "originalVersionId": 456,
                }
            ]
        }
        with patch("touhou_osu.provenance.get_json", return_value=payload):
            hits = query_touhoudb(entry)
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0].verdict, "supports")
        self.assertEqual(hits[0].relation, "arrangement")
        self.assertIn("originalVersionId=456", hits[0].detail)

    def test_touhoudb_non_zun_original_is_red_flag(self):
        entry = Entry(1, artist="Some Circle", title="Image Song", source="Touhou")
        payload = {
            "items": [
                {
                    "id": 123,
                    "name": "Image Song",
                    "artistString": "Some Circle",
                    "artists": [],
                    "status": "Finished",
                    "songType": "Original",
                    "originalVersionId": None,
                }
            ]
        }
        with patch("touhou_osu.provenance.get_json", return_value=payload):
            hits = query_touhoudb(entry)
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0].verdict, "contradicts")
        self.assertEqual(hits[0].relation, "non_zun_original")

    def test_touhoudb_same_title_wrong_artist_is_ignored(self):
        entry = Entry(1, artist="Expected Artist", title="Same Title", source="Touhou")
        payload = {
            "items": [
                {
                    "id": 123,
                    "name": "Same Title",
                    "artistString": "Different Artist",
                    "artists": [],
                    "status": "Finished",
                    "originalVersionId": 456,
                }
            ]
        }
        with patch("touhou_osu.provenance.get_json", return_value=payload):
            self.assertEqual(query_touhoudb(entry), [])

    def test_thbwiki_circle_identity_and_original_supports(self):
        entry = Entry(1, artist="minimum electric design", title="miscalc", source="Touhou")
        search = [[123, "miscalc"]]
        detail = [
            [
                ["id", 123],
                ["name", "miscalc"],
                ["circle", ["minimum electric design"]],
                ["artist", ["dalin"]],
                ["arrange", ["dalin"]],
                ["ogmusic", ["童祭 ～ Innocent Treasures"]],
                ["ogwork", ["夢違科学世紀"]],
            ]
        ]
        with patch("touhou_osu.provenance.get_json", side_effect=[search, detail]):
            hits = query_thbwiki(entry)
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0].verdict, "supports")
        self.assertEqual(hits[0].relation, "arrangement")
        self.assertEqual(hits[0].originals, ("童祭 ～ Innocent Treasures",))
        self.assertIn("circle=minimum electric design", hits[0].detail)
        self.assertIn("ogwork=夢違科学世紀", hits[0].detail)

    def test_thbwiki_arranger_identity_supports(self):
        entry = Entry(1, artist="shio", title="Qronostasis", source="Touhou")
        search = [[123, "Qronostasis"]]
        detail = [
            [
                ["id", 123],
                ["name", "Qronostasis"],
                ["circle", ["Other Circle"]],
                ["arrange", ["shio"]],
                ["ogmusic", ["天空のグリニッジ"]],
            ]
        ]
        with patch("touhou_osu.provenance.get_json", side_effect=[search, detail]):
            hits = query_thbwiki(entry)
        self.assertEqual(len(hits), 1)
        self.assertIn("arrange=shio", hits[0].detail)

    def test_thbwiki_named_nonmatching_identities_are_not_claimed(self):
        entry = Entry(1, artist="Expected Artist", title="Same Title", source="Touhou")
        search = [[123, "Same Title"]]
        detail = [
            [
                ["id", 123],
                ["name", "Same Title"],
                ["circle", ["Different Circle"]],
                ["artist", ["Different Vocalist"]],
                ["arrange", ["Different Arranger"]],
                ["ogmusic", ["Touhou Theme"]],
            ]
        ]
        with patch("touhou_osu.provenance.get_json", side_effect=[search, detail]):
            self.assertEqual(query_thbwiki(entry), [])

    def test_thbwiki_title_only_row_is_not_claimed(self):
        entry = Entry(1, artist="Expected Artist", title="Common Title", source="Touhou")
        search = [[123, "Common Title"]]
        detail = [
            [
                ["id", 123],
                ["name", "Common Title"],
                ["ogmusic", ["Touhou Theme"]],
            ]
        ]
        with patch("touhou_osu.provenance.get_json", side_effect=[search, detail]):
            self.assertEqual(query_thbwiki(entry), [])

    def test_provider_failure_is_advisory(self):
        entry = Entry(1, artist="Artist", title="Title", source="Touhou")
        with patch("touhou_osu.provenance.query_touhoudb", side_effect=HttpError("down")), patch(
            "touhou_osu.provenance.query_thbwiki", return_value=[]
        ):
            result = audit_entry(entry)
        self.assertEqual(result.verdict, "unknown")
        self.assertEqual(len(result.errors), 1)
        self.assertIn("touhoudb", result.errors[0])

    def test_new_generic_verified_without_independent_evidence_is_violation(self):
        base = Catalog([Entry(1, source="Touhou", confidence="candidate", evidence=["discovery_query:Touhou"])])
        current = Catalog([Entry(1, source="Touhou", confidence="verified", evidence=["osu_source"])])
        self.assertEqual(new_generic_verification_violations(current, base), [1])

    def test_generic_verified_with_official_pack_is_not_violation(self):
        base = Catalog([Entry(1, source="Touhou", confidence="candidate")])
        current = Catalog(
            [Entry(1, source="Touhou", confidence="verified", evidence=["official_pack_item:A16"])]
        )
        self.assertEqual(new_generic_verification_violations(current, base), [])

    def test_preexisting_generic_verified_is_not_retroactively_blocked(self):
        base = Catalog([Entry(1, source="Touhou", confidence="verified")])
        current = Catalog([Entry(1, source="Touhou", confidence="verified", evidence=["osu_source"])])
        self.assertEqual(new_generic_verification_violations(current, base), [])


if __name__ == "__main__":
    unittest.main()
