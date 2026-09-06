import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from touhou_osu.catalog import Catalog
from touhou_osu.http import HttpError
from touhou_osu.models import Entry
from touhou_osu.pr_audit import (
    AuditError,
    ProvenanceReviewException,
    accepted_ids_from_audit_document,
    catalog_diff,
    live_osu_audit,
    load_provenance_review_exceptions,
    provenance_audit,
    resolve_provenance_review_exceptions,
    structural_audit,
)
from touhou_osu.provenance import ProvenanceAudit, ProvenanceHit


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


def review_exception(**changes):
    values = {
        "beatmapset_id": 2,
        "artist": "Akiyama Uni",
        "title": "Kaoru Juyouka",
        "provider": "touhoudb",
        "provider_id": "636",
        "relation": "non_zun_original",
        "reason": "Reviewed official Touhou original.",
        "evidence_urls": ("https://example.test/evidence",),
    }
    values.update(changes)
    return ProvenanceReviewException(**values)


def contradiction_audit(*hits):
    return ProvenanceAudit(
        beatmapset_id=2,
        artist="Akiyama Uni",
        title="Kaoru Juyouka",
        source="Touhou Project",
        confidence="verified",
        hits=list(hits),
    )


def contradiction(provider="touhoudb", provider_id="636", relation="non_zun_original"):
    return ProvenanceHit(
        provider=provider,
        verdict="contradicts",
        relation=relation,
        provider_id=provider_id,
    )


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

    def test_repository_provenance_exception_is_valid_and_exact(self):
        path = Path(__file__).resolve().parents[1] / "config/provenance-review-exceptions.json"
        exceptions = load_provenance_review_exceptions(path)
        self.assertEqual(len(exceptions), 1)
        self.assertEqual(
            exceptions[0].key,
            (397764, "touhoudb", "636", "non_zun_original"),
        )
        self.assertEqual(exceptions[0].artist, "Akiyama Uni")
        self.assertEqual(exceptions[0].title, "Kaoru Juyouka")

    def test_provenance_exception_acknowledges_only_exact_contradiction(self):
        item = entry(2, artist="Akiyama Uni", title="Kaoru Juyouka")
        base, current = Catalog(), Catalog([item])
        diff = catalog_diff(base, current)
        audit = contradiction_audit(contradiction())
        with patch("touhou_osu.pr_audit.audit_entries", return_value=[audit]):
            report = provenance_audit(
                base,
                current,
                diff,
                scope="added",
                workers=1,
                exceptions=(review_exception(),),
            )
        self.assertEqual(report["review_flags"], [])
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["red_flags"], 1)
        self.assertEqual(report["acknowledged_review_flags"], [review_exception().to_dict()])

    def test_provenance_exception_mismatch_remains_fail_closed(self):
        item = entry(2, artist="Akiyama Uni", title="Kaoru Juyouka")
        base, current = Catalog(), Catalog([item])
        diff = catalog_diff(base, current)
        mismatches = (
            review_exception(beatmapset_id=3),
            review_exception(artist="Other Artist"),
            review_exception(title="Other Title"),
            review_exception(provider="thbwiki"),
            review_exception(provider_id="999"),
            review_exception(relation="other_relation"),
        )
        for exception in mismatches:
            with self.subTest(exception=exception), patch(
                "touhou_osu.pr_audit.audit_entries",
                return_value=[contradiction_audit(contradiction())],
            ):
                report = provenance_audit(
                    base,
                    current,
                    diff,
                    scope="added",
                    workers=1,
                    exceptions=(exception,),
                )
                self.assertEqual(report["review_flags"], [2])
                self.assertEqual(report["acknowledged_review_flags"], [])
                self.assertIn("external provenance needs review", report["errors"][0])

    def test_new_contradiction_still_fails_beside_acknowledged_one(self):
        item = entry(2, artist="Akiyama Uni", title="Kaoru Juyouka")
        base, current = Catalog(), Catalog([item])
        diff = catalog_diff(base, current)
        audit = contradiction_audit(
            contradiction(),
            contradiction(provider="other-provider", provider_id="new", relation="new_relation"),
        )
        with patch("touhou_osu.pr_audit.audit_entries", return_value=[audit]):
            report = provenance_audit(
                base,
                current,
                diff,
                scope="added",
                workers=1,
                exceptions=(review_exception(),),
            )
        self.assertEqual(report["review_flags"], [2])
        self.assertEqual(report["acknowledged_review_flags"], [review_exception().to_dict()])
        self.assertIn("external provenance needs review", report["errors"][0])

    def test_provenance_exception_file_rejects_unsafe_records(self):
        valid = review_exception().to_dict()
        invalid_records = (
            {**valid, "reason": ""},
            {**valid, "evidence_urls": []},
            {**valid, "evidence_urls": ["not-a-url"]},
            {**valid, "provider": "TouhouDB"},
            {**valid, "unexpected": "field"},
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "exceptions.json"
            for record in invalid_records:
                with self.subTest(record=record):
                    path.write_text(
                        json.dumps({"schema_version": 1, "exceptions": [record]}),
                        encoding="utf-8",
                    )
                    with self.assertRaises(AuditError):
                        load_provenance_review_exceptions(path)

    def test_provenance_exception_file_rejects_duplicate_keys(self):
        record = review_exception().to_dict()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "exceptions.json"
            path.write_text(
                json.dumps({"schema_version": 1, "exceptions": [record, record]}),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(AuditError, "duplicate provenance exception"):
                load_provenance_review_exceptions(path)

    def test_missing_default_exception_registry_means_no_exceptions(self):
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            self.assertEqual(resolve_provenance_review_exceptions(repository, None), ())
            with self.assertRaisesRegex(AuditError, "cannot load provenance exceptions"):
                resolve_provenance_review_exceptions(repository, Path("missing.json"))

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

    def test_live_osu_retries_public_page_rate_limit(self):
        item = entry(2)
        FakeApi.raw = {2: raw(item)}
        page = '<script id="json-beatmapset" type="application/json">' + json.dumps(raw(item)) + "</script>"
        diff = catalog_diff(Catalog(), Catalog([item]))
        with patch("touhou_osu.pr_audit.OsuApi", FakeApi), patch(
            "touhou_osu.pr_audit.get_text",
            side_effect=[HttpError("HTTP 429 from public page"), page],
        ):
            report = live_osu_audit(
                Catalog([item]),
                diff,
                scope="added",
                workers=1,
                public_interval=0,
                rate_limit_backoff=0,
            )
        self.assertEqual(report, {"checked": 1, "failures": [], "errors": []})


if __name__ == "__main__":
    unittest.main()
