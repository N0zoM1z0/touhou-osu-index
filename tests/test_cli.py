import argparse
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from touhou_osu.catalog import Catalog
from touhou_osu.cli import command_discover, command_hydrate, command_reconcile
from touhou_osu.models import Entry


class FakeOsuApi:
    responses = {}
    beatmapsets = {}

    @classmethod
    def from_env(cls):
        return cls()

    def token(self):
        return "fake-token"

    def search(self, query, *, max_pages):
        return iter(self.responses[query])

    def beatmapset(self, beatmapset_id):
        return self.beatmapsets[beatmapset_id]


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


class ReconciliationTests(unittest.TestCase):
    def _run_reconcile(self, current: Entry, raw: dict) -> Entry:
        with tempfile.TemporaryDirectory() as directory:
            catalog_path = Path(directory) / "catalog.json"
            Catalog([current]).save(catalog_path)
            FakeOsuApi.beatmapsets = {current.beatmapset_id: raw}
            args = argparse.Namespace(
                catalog=catalog_path,
                workers=1,
                write=True,
                strict=True,
            )
            with patch("touhou_osu.cli.OsuApi", FakeOsuApi):
                self.assertEqual(command_reconcile(args), 0)
            return Catalog.load(catalog_path).entries[current.beatmapset_id]

    def test_reconcile_quarantines_trusted_evidence_on_replaced_identity(self):
        current = Entry(
            42,
            artist="LeaF",
            title="Arianrhod (hi19hi19) [Mabinogi 1.1x (176bpm)]",
            creator="_Kobii",
            touhou_kind="arrangement",
            origin_games=["Touhou Project"],
            original_themes=["Lunar Clock ~ Luna Dial"],
            evidence=["tmc:2nd", "tournament:467"],
            confidence="verified",
        )
        raw = {
            "id": 42,
            "artist": "cosMo@bousouP",
            "title": "Oceanus",
            "creator": "_Kobii",
            "source": "Deemo",
            "status": "graveyard",
            "tags": "",
            "last_updated": "2022-01-16T22:10:41Z",
            "beatmaps": [{"mode": "mania"}],
        }

        reconciled = self._run_reconcile(current, raw)

        self.assertEqual(reconciled.artist, "cosMo@bousouP")
        self.assertEqual(reconciled.title, "Oceanus")
        self.assertEqual(reconciled.confidence, "candidate")
        self.assertEqual(reconciled.evidence, ["reconcile:identity-mismatch"])
        self.assertEqual(reconciled.touhou_kind, "unknown")
        self.assertEqual(reconciled.origin_games, [])
        self.assertEqual(reconciled.original_themes, [])

    def test_reconcile_quarantines_sticky_manual_verification_on_replaced_identity(self):
        current = Entry(
            42,
            artist="LeaF",
            title="Arianrhod",
            creator="_Kobii",
            evidence=["manual:verified"],
            confidence="verified",
        )
        raw = {
            "id": 42,
            "artist": "cosMo@bousouP",
            "title": "Oceanus",
            "creator": "_Kobii",
            "source": "Deemo",
            "status": "graveyard",
            "tags": "",
            "last_updated": "2022-01-16T22:10:41Z",
            "beatmaps": [{"mode": "mania"}],
        }

        reconciled = self._run_reconcile(current, raw)

        self.assertEqual(reconciled.confidence, "candidate")
        self.assertEqual(reconciled.evidence, ["reconcile:identity-mismatch"])
        self.assertNotIn("manual:verified", reconciled.evidence)

    def test_reconcile_quarantines_reviewed_same_artist_title_replacement(self):
        current = Entry(
            42,
            artist="IOSYS",
            title="Verified Touhou Song",
            creator="mapper",
            evidence=["manual:verified"],
            confidence="verified",
        )
        raw = {
            "id": 42,
            "artist": "IOSYS",
            "title": "Different Song",
            "creator": "mapper",
            "source": "Non-Touhou Album",
            "status": "graveyard",
            "tags": "",
            "last_updated": "2022-01-16T22:10:41Z",
            "beatmaps": [{"mode": "osu"}],
        }

        reconciled = self._run_reconcile(current, raw)

        self.assertEqual(reconciled.confidence, "candidate")
        self.assertIn("reconcile:identity-mismatch", reconciled.evidence)
        self.assertIn("known_touhou_artist", reconciled.evidence)
        self.assertNotIn("manual:verified", reconciled.evidence)

    def test_reconcile_replaces_stale_metadata_after_identity_quarantine(self):
        current = Entry(
            42,
            artist="Old Artist",
            title="Old Touhou Song",
            creator="Old Mapper",
            source="東方永夜抄 ～ Imperishable Night.",
            status="ranked",
            modes=["osu"],
            evidence=["manual:verified", "osu_source"],
            confidence="verified",
            osu_last_updated="2020-01-01T00:00:00Z",
        )
        raw = {
            "id": 42,
            "artist": "New Artist",
            "title": "Different Song",
            "creator": "",
            "source": "",
            "status": "graveyard",
            "tags": "",
            "last_updated": "2026-01-02T00:00:00Z",
            "beatmaps": [{"mode": "mania"}],
        }

        reconciled = self._run_reconcile(current, raw)

        self.assertEqual(reconciled.artist, "New Artist")
        self.assertEqual(reconciled.title, "Different Song")
        self.assertEqual(reconciled.creator, "")
        self.assertEqual(reconciled.source, "")
        self.assertEqual(reconciled.status, "graveyard")
        self.assertEqual(reconciled.modes, ["mania"])
        self.assertEqual(reconciled.osu_last_updated, "2026-01-02T00:00:00Z")
        self.assertEqual(reconciled.confidence, "candidate")
        self.assertIn("reconcile:identity-mismatch", reconciled.evidence)
        self.assertNotIn("manual:verified", reconciled.evidence)
        self.assertNotIn("osu_source", reconciled.evidence)

    def test_reconcile_keeps_trusted_evidence_for_canonical_title_cleanup(self):
        current = Entry(
            42,
            artist="Shoegazer",
            title="Everything Will Freeze (Shoegazer) [Calamity]",
            creator="mapper",
            evidence=["manual:verified", "tmc:2nd", "tournament:467"],
            confidence="verified",
        )
        raw = {
            "id": 42,
            "artist": "UNDEAD CORPORATION",
            "title": "Everything Will Freeze",
            "creator": "mapper",
            "source": "東方Project",
            "status": "ranked",
            "tags": "",
            "last_updated": "2022-01-16T22:10:41Z",
            "beatmaps": [{"mode": "mania"}],
        }

        reconciled = self._run_reconcile(current, raw)

        self.assertEqual(reconciled.artist, "UNDEAD CORPORATION")
        self.assertEqual(reconciled.title, "Everything Will Freeze")
        self.assertEqual(reconciled.confidence, "verified")
        self.assertIn("manual:verified", reconciled.evidence)
        self.assertIn("tmc:2nd", reconciled.evidence)
        self.assertIn("tournament:467", reconciled.evidence)
        self.assertNotIn("reconcile:identity-mismatch", reconciled.evidence)


if __name__ == "__main__":
    unittest.main()
