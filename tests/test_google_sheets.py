from __future__ import annotations

import io
import unittest
from unittest.mock import patch
from zipfile import ZipFile

from touhou_osu.google_sheets import (
    parse_google_sheet_beatmap_ids,
    parse_google_sheet_beatmapset_ids,
)
from touhou_osu.sources import import_google_sheet_tournament


class GoogleSheetsTests(unittest.TestCase):
    @staticmethod
    def fixture() -> bytes:
        buffer = io.BytesIO()
        with ZipFile(buffer, "w") as archive:
            archive.writestr(
                "xl/workbook.xml",
                """<?xml version="1.0"?>
                <workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
                  xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
                  <sheets>
                    <sheet name="Main" sheetId="1" r:id="rId1"/>
                    <sheet name="Mappools" sheetId="2" r:id="rId2"/>
                    <sheet name="Mappool | QF" sheetId="3" r:id="rId3"/>
                  </sheets>
                </workbook>""",
            )
            archive.writestr(
                "xl/_rels/workbook.xml.rels",
                """<?xml version="1.0"?>
                <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
                  <Relationship Id="rId1" Target="worksheets/sheet1.xml"/>
                  <Relationship Id="rId2" Target="worksheets/sheet2.xml"/>
                  <Relationship Id="rId3" Target="worksheets/sheet3.xml"/>
                </Relationships>""",
            )
            archive.writestr(
                "xl/sharedStrings.xml",
                """<?xml version="1.0"?>
                <sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
                  <si><t>https://osu.ppy.sh/beatmapsets/456</t></si>
                </sst>""",
            )
            archive.writestr(
                "xl/worksheets/sheet1.xml",
                """<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
                  <sheetData><row><c t="inlineStr"><is><t>https://osu.ppy.sh/beatmapsets/999</t></is></c></row></sheetData>
                </worksheet>""",
            )
            archive.writestr(
                "xl/worksheets/sheet2.xml",
                """<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
                  <sheetData><row>
                    <c t="inlineStr"><is><t>https://osu.ppy.sh/s/123</t></is></c>
                    <c t="s"><v>0</v></c>
                  </row></sheetData>
                </worksheet>""",
            )
            archive.writestr(
                "xl/worksheets/_rels/sheet2.xml.rels",
                """<?xml version="1.0"?>
                <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
                  <Relationship Id="h1" Target="https://osu.ppy.sh/beatmapsets/789#osu/10" TargetMode="External"/>
                  <Relationship Id="h2" Target="https://osu.ppy.sh/beatmapsets/123" TargetMode="External"/>
                  <Relationship Id="h3" Target="https://osu.ppy.sh/b/654321" TargetMode="External"/>
                  <Relationship Id="h4" Target="https://osu.ppy.sh/beatmaps/654322" TargetMode="External"/>
                </Relationships>""",
            )
            archive.writestr(
                "xl/worksheets/sheet3.xml",
                """<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
                  <sheetData><row><c t="inlineStr"><is><t>https://osu.ppy.sh/beatmapsets/777</t></is></c></row></sheetData>
                </worksheet>""",
            )
        return buffer.getvalue()

    def test_exact_sheet_and_shared_strings(self) -> None:
        ids = parse_google_sheet_beatmapset_ids(self.fixture(), sheet_names=["Mappools"])
        self.assertEqual(ids, [123, 456, 789])

    def test_legacy_beatmap_links_are_not_beatmapset_ids(self) -> None:
        beatmapset_ids = parse_google_sheet_beatmapset_ids(
            self.fixture(), sheet_names=["Mappools"]
        )
        beatmap_ids = parse_google_sheet_beatmap_ids(
            self.fixture(), sheet_names=["Mappools"]
        )
        self.assertEqual(beatmapset_ids, [123, 456, 789])
        self.assertEqual(beatmap_ids, [654321, 654322])

    def test_sheet_prefix_and_deduplication(self) -> None:
        ids = parse_google_sheet_beatmapset_ids(self.fixture(), sheet_prefixes=["Mappool"])
        self.assertEqual(ids, [123, 456, 789, 777])

    def test_unfiltered_import_sees_all_worksheets(self) -> None:
        ids = parse_google_sheet_beatmapset_ids(self.fixture())
        self.assertEqual(ids, [999, 123, 456, 789, 777])

    def test_missing_requested_sheet_fails_closed(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "requested worksheets"):
            parse_google_sheet_beatmapset_ids(self.fixture(), sheet_names=["Missing"])

    def test_invalid_xlsx_fails_closed(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "XLSX"):
            parse_google_sheet_beatmapset_ids(b"not a zip")

    @patch("touhou_osu.sources.fetch_google_sheet_beatmapset_ids", return_value=[123, 456])
    def test_trusted_tournament_is_verified(self, fetch_ids) -> None:
        entries = import_google_sheet_tournament(
            {
                "id": "fixture",
                "spreadsheet_id": "sheet-id",
                "sheet_names": ["Mappools"],
                "trusted": True,
            }
        )
        fetch_ids.assert_called_once_with(
            "sheet-id", sheet_names=["Mappools"], sheet_prefixes=()
        )
        self.assertEqual([entry.beatmapset_id for entry in entries], [123, 456])
        self.assertTrue(all(entry.confidence == "verified" for entry in entries))
        self.assertTrue(
            all("tournament:google_sheet:fixture" in entry.evidence for entry in entries)
        )

    @patch("touhou_osu.sources.fetch_google_sheet_beatmapset_ids", return_value=[123])
    def test_untrusted_tournament_stays_candidate(self, _fetch_ids) -> None:
        [entry] = import_google_sheet_tournament(
            {
                "id": "mixed-fixture",
                "spreadsheet_id": "sheet-id",
                "trusted": False,
                "confidence": "candidate",
            }
        )
        self.assertEqual(entry.confidence, "candidate")
        self.assertIn("tournament_candidate:google_sheet:mixed-fixture", entry.evidence)

    @patch("touhou_osu.sources.fetch_google_sheet_beatmap_ids", return_value=[10, 20, 30])
    def test_audited_subset_is_verified_even_when_whole_pool_is_untrusted(
        self, fetch_ids
    ) -> None:
        entries = import_google_sheet_tournament(
            {
                "id": "audited-fixture",
                "spreadsheet_id": "sheet-id",
                "sheet_names": ["Mappool"],
                "trusted": False,
                "minimum_source_beatmaps": 3,
                "audited_beatmaps": [
                    {"beatmap_id": 10, "beatmapset_id": 100},
                    {"beatmap_id": 30, "beatmapset_id": 300},
                ],
            }
        )
        fetch_ids.assert_called_once_with(
            "sheet-id", sheet_names=["Mappool"], sheet_prefixes=()
        )
        self.assertEqual([entry.beatmapset_id for entry in entries], [100, 300])
        self.assertTrue(all(entry.confidence == "verified" for entry in entries))
        self.assertTrue(
            all(
                "tournament:google_sheet:audited-fixture:audited" in entry.evidence
                for entry in entries
            )
        )

    @patch("touhou_osu.sources.fetch_google_sheet_beatmap_ids", return_value=[10, 20])
    def test_audited_subset_fails_if_reviewed_beatmap_disappears(self, _fetch_ids) -> None:
        with self.assertRaisesRegex(RuntimeError, "no longer contains audited beatmaps"):
            import_google_sheet_tournament(
                {
                    "id": "audited-fixture",
                    "spreadsheet_id": "sheet-id",
                    "audited_beatmaps": [
                        {"beatmap_id": 10, "beatmapset_id": 100},
                        {"beatmap_id": 30, "beatmapset_id": 300},
                    ],
                }
            )

    @patch("touhou_osu.sources.fetch_google_sheet_beatmap_ids", return_value=[10, 20])
    def test_audited_subset_rejects_duplicate_beatmap_ids(self, _fetch_ids) -> None:
        with self.assertRaisesRegex(RuntimeError, "duplicate audited beatmap_id"):
            import_google_sheet_tournament(
                {
                    "id": "audited-fixture",
                    "spreadsheet_id": "sheet-id",
                    "audited_beatmaps": [
                        {"beatmap_id": 10, "beatmapset_id": 100},
                        {"beatmap_id": 10, "beatmapset_id": 101},
                    ],
                }
            )

    @patch("touhou_osu.sources.fetch_google_sheet_beatmap_ids", return_value=[10, 20])
    def test_audited_subset_enforces_source_floor(self, _fetch_ids) -> None:
        with self.assertRaisesRegex(RuntimeError, "source beatmaps"):
            import_google_sheet_tournament(
                {
                    "id": "audited-fixture",
                    "spreadsheet_id": "sheet-id",
                    "minimum_source_beatmaps": 3,
                    "audited_beatmaps": [
                        {"beatmap_id": 10, "beatmapset_id": 100},
                    ],
                }
            )


if __name__ == "__main__":
    unittest.main()
