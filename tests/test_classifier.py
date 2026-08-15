import unittest

from touhou_osu.classifier import apply_classification
from touhou_osu.models import Entry


class ClassifierTests(unittest.TestCase):
    def test_explicit_source_is_verified(self):
        item = Entry(1, source="東方Project", evidence=["discovery_query:東方"], confidence="candidate")
        apply_classification(item)
        self.assertEqual(item.confidence, "verified")
        self.assertIn("osu_source", item.evidence)

    def test_known_game_source_is_verified(self):
        item = Entry(
            1,
            source="東方永夜抄 ～ Imperishable Night.",
            evidence=["discovery_query:source=東方Project"],
            confidence="candidate",
        )
        apply_classification(item)
        self.assertEqual(item.confidence, "verified")
        self.assertIn("osu_source", item.evidence)

    def test_unrelated_romanized_touhou_source_stays_candidate(self):
        item = Entry(
            1,
            artist="Faylan",
            title="God FATE (TV Size)",
            source="Hakkenden Touhou Hakken Ibun",
            evidence=["discovery_query:source=Touhou"],
            confidence="candidate",
        )
        apply_classification(item, tags="hakkenden touhou hakken ibun anime")
        self.assertEqual(item.confidence, "candidate")
        self.assertNotIn("osu_source", item.evidence)

    def test_unrelated_japanese_touhou_source_stays_candidate(self):
        item = Entry(
            1,
            artist="Tetsuya Kakihara",
            title="String of pain (TV Size)",
            source="八犬伝－東方八犬異聞－",
            evidence=["discovery_query:東方"],
            confidence="candidate",
        )
        apply_classification(item, tags="東方八犬異聞 anime")
        self.assertEqual(item.confidence, "candidate")
        self.assertNotIn("osu_source", item.evidence)

    def test_unreviewed_fan_source_stays_candidate(self):
        item = Entry(
            1,
            artist="IOSYS",
            title="Utage wa Eien ni",
            source="Touhou Suisui Suusuu",
            evidence=["discovery_query:source=Touhou"],
            confidence="candidate",
        )
        apply_classification(item)
        self.assertEqual(item.confidence, "candidate")
        self.assertNotIn("osu_source", item.evidence)

    def test_official_pack_is_verified(self):
        item = Entry(1, evidence=["official_pack:FQ55"], confidence="candidate")
        apply_classification(item)
        self.assertEqual(item.confidence, "verified")

    def test_known_artist_alone_stays_candidate(self):
        item = Entry(1, artist="IOSYS", evidence=["discovery_query:IOSYS"], confidence="candidate")
        apply_classification(item)
        self.assertEqual(item.confidence, "candidate")
        self.assertIn("known_touhou_artist", item.evidence)

    def test_tags_plus_known_artist_are_probable(self):
        item = Entry(1, artist="ShibayanRecords", evidence=["discovery_query:Touhou"])
        apply_classification(item, tags="touhou zun arrangement")
        self.assertEqual(item.confidence, "probable")


if __name__ == "__main__":
    unittest.main()
