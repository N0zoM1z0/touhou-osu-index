"""Read beatmap and beatmapset links from public Google Sheets without dependencies."""

from __future__ import annotations

import posixpath
import re
from io import BytesIO
from typing import Iterable, Pattern
from xml.etree import ElementTree as ET
from zipfile import BadZipFile, ZipFile

from .http import request

_BEATMAPSET_URL_RE = re.compile(
    r"https?://osu\.ppy\.sh/(?:beatmapsets|s)/(\d+)", re.IGNORECASE
)
_BEATMAP_URL_RE = re.compile(
    r"https?://osu\.ppy\.sh/(?:b/|beatmaps/)(\d+)", re.IGNORECASE
)
_PACKAGE_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
_DOCUMENT_REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
_SPREADSHEET_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"


def google_sheet_export_url(spreadsheet_id: str) -> str:
    return f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=xlsx"


def _relationship_targets(xml_bytes: bytes) -> dict[str, str]:
    root = ET.fromstring(xml_bytes)
    return {
        rel.attrib["Id"]: rel.attrib.get("Target", "")
        for rel in root.findall(f"{{{_PACKAGE_REL_NS}}}Relationship")
        if rel.attrib.get("Id")
    }


def _normalize_archive_path(source_path: str, target: str) -> str:
    if target.startswith("/"):
        return target.lstrip("/")
    return posixpath.normpath(posixpath.join(posixpath.dirname(source_path), target))


def _worksheet_rels_path(sheet_path: str) -> str:
    directory, filename = posixpath.split(sheet_path)
    return posixpath.join(directory, "_rels", f"{filename}.rels")


def _shared_strings(archive: ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in archive.namelist():
        return []
    root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
    values: list[str] = []
    for item in root.findall(f"{{{_SPREADSHEET_NS}}}si"):
        values.append(
            "".join(node.text or "" for node in item.iter(f"{{{_SPREADSHEET_NS}}}t"))
        )
    return values


def _worksheet_texts(
    archive: ZipFile, sheet_path: str, shared_strings: list[str]
) -> list[str]:
    raw = archive.read(sheet_path)
    root = ET.fromstring(raw)
    texts = [raw.decode("utf-8", errors="replace")]

    for cell in root.iter(f"{{{_SPREADSHEET_NS}}}c"):
        if cell.attrib.get("t") != "s":
            continue
        value = cell.find(f"{{{_SPREADSHEET_NS}}}v")
        if value is None or value.text is None or not value.text.isdigit():
            continue
        index = int(value.text)
        if 0 <= index < len(shared_strings):
            texts.append(shared_strings[index])

    rels_path = _worksheet_rels_path(sheet_path)
    if rels_path in archive.namelist():
        texts.extend(_relationship_targets(archive.read(rels_path)).values())
    return texts


def _parse_google_sheet_ids(
    payload: bytes,
    pattern: Pattern[str],
    *,
    sheet_names: Iterable[str] = (),
    sheet_prefixes: Iterable[str] = (),
) -> list[int]:
    exact_names = set(sheet_names)
    prefixes = tuple(sheet_prefixes)

    try:
        with ZipFile(BytesIO(payload)) as archive:
            workbook_path = "xl/workbook.xml"
            workbook = ET.fromstring(archive.read(workbook_path))
            workbook_rels = _relationship_targets(
                archive.read("xl/_rels/workbook.xml.rels")
            )
            shared_strings = _shared_strings(archive)

            selected: list[tuple[str, str]] = []
            for sheet in workbook.findall(f".//{{{_SPREADSHEET_NS}}}sheet"):
                name = sheet.attrib.get("name", "")
                relation_id = sheet.attrib.get(f"{{{_DOCUMENT_REL_NS}}}id", "")
                target = workbook_rels.get(relation_id, "")
                if not target:
                    continue
                if exact_names or prefixes:
                    matches_exact = name in exact_names
                    matches_prefix = any(name.startswith(prefix) for prefix in prefixes)
                    if not matches_exact and not matches_prefix:
                        continue
                selected.append(
                    (name, _normalize_archive_path(workbook_path, target))
                )

            if (exact_names or prefixes) and not selected:
                requested = sorted(exact_names) + [f"{prefix}*" for prefix in prefixes]
                raise RuntimeError(
                    f"Google Sheet contains none of the requested worksheets: {requested}"
                )

            ids: list[int] = []
            seen: set[int] = set()
            for _, sheet_path in selected:
                for text in _worksheet_texts(archive, sheet_path, shared_strings):
                    for match in pattern.finditer(text):
                        value = int(match.group(1))
                        if value in seen:
                            continue
                        seen.add(value)
                        ids.append(value)
            return ids
    except RuntimeError:
        raise
    except (BadZipFile, KeyError, ET.ParseError) as exc:
        raise RuntimeError("Could not parse Google Sheet XLSX export") from exc


def parse_google_sheet_beatmapset_ids(
    payload: bytes,
    *,
    sheet_names: Iterable[str] = (),
    sheet_prefixes: Iterable[str] = (),
) -> list[int]:
    """Extract ordered unique osu! beatmapset IDs from selected XLSX worksheets."""
    return _parse_google_sheet_ids(
        payload,
        _BEATMAPSET_URL_RE,
        sheet_names=sheet_names,
        sheet_prefixes=sheet_prefixes,
    )


def parse_google_sheet_beatmap_ids(
    payload: bytes,
    *,
    sheet_names: Iterable[str] = (),
    sheet_prefixes: Iterable[str] = (),
) -> list[int]:
    """Extract ordered unique osu! beatmap IDs from selected XLSX worksheets."""
    return _parse_google_sheet_ids(
        payload,
        _BEATMAP_URL_RE,
        sheet_names=sheet_names,
        sheet_prefixes=sheet_prefixes,
    )


def fetch_google_sheet_beatmapset_ids(
    spreadsheet_id: str,
    *,
    sheet_names: Iterable[str] = (),
    sheet_prefixes: Iterable[str] = (),
) -> list[int]:
    payload = request(
        google_sheet_export_url(spreadsheet_id),
        headers={
            "Accept": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        },
    )
    return parse_google_sheet_beatmapset_ids(
        payload,
        sheet_names=sheet_names,
        sheet_prefixes=sheet_prefixes,
    )


def fetch_google_sheet_beatmap_ids(
    spreadsheet_id: str,
    *,
    sheet_names: Iterable[str] = (),
    sheet_prefixes: Iterable[str] = (),
) -> list[int]:
    payload = request(
        google_sheet_export_url(spreadsheet_id),
        headers={
            "Accept": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        },
    )
    return parse_google_sheet_beatmap_ids(
        payload,
        sheet_names=sheet_names,
        sheet_prefixes=sheet_prefixes,
    )
