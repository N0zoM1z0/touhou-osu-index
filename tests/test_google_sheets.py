from __future__ import annotations

import io
import unittest
from unittest.mock import patch
from zipfile import ZipFile

from touhou_osu.google_sheets import parse_google_sheet_beatmapset_ids
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


if __name__ == "__main__":
    unittest.main()
