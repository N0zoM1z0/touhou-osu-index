import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from touhou_osu.catalog import Catalog
from touhou_osu.models import Entry
from touhou_osu.pr_audit import (
    AuditError,
    accepted_ids_from_audit_document,
    catalog_diff,
    live_osu_audit,
    structural_audit,
)


def entry(beatmapset_id, **changes):
    values = {
        "beatmapset_id": beatmapset_id,
        "artist": "ZUN",
        "title": f"Theme {beatmapset_id}",
        "creator": "Mapper",
        "source": "Touhou Project",
        "status": "ranked",
        "modes": ["osu"],
        "evidence": ["manual:verified"],
        "confidence": "verified",
        "last_checked": "2026-09-06",
        "osu_last_updated": "2026-09-01T00:00:00Z",
    }
    values.update(changes)
    return Entry(**values)


class FakeApi:
    raw = {}

    @classmethod
    def from_env(cls):
        return cls()

    def token(self):
        return "token"

    def beatmapset(self, beatmapset_id):
        return self.raw[beatmapset_id]


def raw(item):
    return {
        "id": item.beatmapset_id,
        "artist": item.artist,
        "title": item.title,
        "creator": item.creator,
        "source": item.source,
        "status": item.status,
        "last_updated": item.osu_last_updated,
        "tags": "touhou",
        "beatmaps": [{"mode": mode} for mode in item.modes],
    }


class PrAuditTests(unittest.TestCase):
    def test_catalog_diff_reports_added_removed_and_changed_fields(self):
        base = Catalog([entry(1), entry(2)])
        current = Catalog([entry(2, title="Changed"), entry(3)])
        diff = catalog_diff(base, current)
        self.assertEqual(diff["added"], [3])
        self.assertEqual(diff["removed"], [1])
        self.assertEqual(diff["modified"], [2])
        self.assertEqual(diff["changed_fields"], {"2": ["title"]})

    def test_structural_audit_is_fail_closed_for_removals(self):
        diff = catalog_diff(Catalog([entry(1)]), Catalog())
        result = structural_audit(diff)
        self.assertIn("removals", result["errors"][0])

    def test_structural_audit_can_forbid_existing_row_changes(self):
        diff = catalog_diff(Catalog([entry(1)]), Catalog([entry(1, title="Changed")]))
        result = structural_audit(diff, forbid_existing_changes=True)
        self.assertIn("pre-existing rows changed", result["errors"][0])

    def test_audit_document_ids_must_equal_additions(self):
        document = """# Audit\n\n## Accepted beatmapsets\n\n| ID | Title |\n| ---: | --- |\n| 2 | Two |\n| 3 | Three |\n\n## Boundary\n"""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "audit.md"
            path.write_text(document, encoding="utf-8")
            self.assertEqual(accepted_ids_from_audit_document(path), [2, 3])
            diff = catalog_diff(Catalog([entry(1)]), Catalog([entry(1), entry(2), entry(3)]))
            self.assertEqual(structural_audit(diff, audit_document=path)["errors"], [])

    def test_audit_document_rejects_duplicate_ids(self):
        document = """## Accepted beatmapsets\n\n| ID |\n| ---: |\n| 2 |\n| 2 |\n"""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "audit.md"
            path.write_text(document, encoding="utf-8")
            with self.assertRaisesRegex(AuditError, "duplicate"):
                accepted_ids_from_audit_document(path)

    def test_live_osu_requires_catalog_api_and_public_page_to_match(self):
        item = entry(2)
        FakeApi.raw = {2: raw(item)}
        page = '<script id="json-beatmapset" type="application/json">' + json.dumps(raw(item)) + "</script>"
        diff = catalog_diff(Catalog(), Catalog([item]))
        with patch("touhou_osu.pr_audit.OsuApi", FakeApi), patch(
            "touhou_osu.pr_audit.get_text", return_value=page
        ):
            report = live_osu_audit(Catalog([item]), diff, scope="added", workers=1)
        self.assertEqual(report, {"checked": 1, "failures": [], "errors": []})

    def test_live_osu_reports_catalog_drift(self):
        item = entry(2)
        api_item = entry(2, title="Live title")
        FakeApi.raw = {2: raw(api_item)}
        diff = catalog_diff(Catalog(), Catalog([item]))
        with patch("touhou_osu.pr_audit.OsuApi", FakeApi):
            report = live_osu_audit(Catalog([item]), diff, scope="added", workers=1)
        self.assertEqual(report["checked"], 1)
        self.assertEqual(report["failures"][0]["beatmapset_id"], 2)
        self.assertIn("catalog/API drift: title", report["failures"][0]["error"])

    def test_live_osu_reports_public_page_drift(self):
        item = entry(2)
        page_item = entry(2, creator="Other mapper")
        FakeApi.raw = {2: raw(item)}
        page = '<script id="json-beatmapset" type="application/json">' + json.dumps(raw(page_item)) + "</script>"
        diff = catalog_diff(Catalog(), Catalog([item]))
        with patch("touhou_osu.pr_audit.OsuApi", FakeApi), patch(
            "touhou_osu.pr_audit.get_text", return_value=page
        ):
            report = live_osu_audit(Catalog([item]), diff, scope="added", workers=1)
        self.assertIn("API/public-page drift: creator", report["failures"][0]["error"])


if __name__ == "__main__":
    unittest.main()
