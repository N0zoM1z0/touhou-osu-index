"""Load, merge, and save the canonical catalog."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from .models import CatalogError, Entry

SCHEMA_VERSION = 1
CONFIDENCE_RANK = {"excluded": -1, "candidate": 0, "probable": 1, "verified": 2}


class Catalog:
    def __init__(self, entries: Iterable[Entry] = ()) -> None:
        self.entries: dict[int, Entry] = {}
        for entry in entries:
            if entry.beatmapset_id in self.entries:
                raise CatalogError(f"duplicate beatmapset_id: {entry.beatmapset_id}")
            self.entries[entry.beatmapset_id] = entry

    @classmethod
    def load(cls, path: Path) -> "Catalog":
        raw = json.loads(path.read_text(encoding="utf-8"))
        if raw.get("schema_version") != SCHEMA_VERSION:
            raise CatalogError(f"unsupported schema_version: {raw.get('schema_version')!r}")
        records = raw.get("entries")
        if not isinstance(records, list):
            raise CatalogError("catalog entries must be a list")
        ids = [record.get("beatmapset_id") for record in records]
        if ids != sorted(ids):
            raise CatalogError("catalog entries must be sorted by numeric beatmapset_id")
        return cls(Entry.from_dict(record) for record in records)

    def merge(self, incoming: Entry) -> tuple[Entry, bool]:
        incoming.normalize()
        incoming.validate()
        current = self.entries.get(incoming.beatmapset_id)
        if current is None:
            self.entries[incoming.beatmapset_id] = incoming
            return incoming, True

        before = current.to_dict()
        for field_name in ("artist", "title", "creator", "source", "status", "osu_last_updated"):
            value = getattr(incoming, field_name)
            if value and value != "unknown":
                setattr(current, field_name, value)

        current.modes = sorted(set(current.modes) | set(incoming.modes))
        current.origin_games = sorted(set(current.origin_games) | set(incoming.origin_games), key=str.casefold)
        current.original_themes = sorted(
            set(current.original_themes) | set(incoming.original_themes), key=str.casefold
        )
        current.evidence = sorted(set(current.evidence) | set(incoming.evidence), key=str.casefold)
        if current.touhou_kind == "unknown" and incoming.touhou_kind != "unknown":
            current.touhou_kind = incoming.touhou_kind

        manual = {item for item in current.evidence if item.startswith("manual:")}
        if "manual:excluded" in manual:
            current.confidence = "excluded"
        elif "manual:verified" in manual:
            current.confidence = "verified"
        elif CONFIDENCE_RANK[incoming.confidence] > CONFIDENCE_RANK[current.confidence]:
            current.confidence = incoming.confidence

        dates = [value for value in (current.last_checked, incoming.last_checked) if value]
        current.last_checked = max(dates) if dates else None
        current.normalize()
        current.validate()
        return current, current.to_dict() != before

    def validate(self) -> None:
        for entry in self.entries.values():
            entry.normalize()
            entry.validate()

    def to_dict(self) -> dict:
        self.validate()
        return {
            "schema_version": SCHEMA_VERSION,
            "entries": [self.entries[key].to_dict() for key in sorted(self.entries)],
        }

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        text = json.dumps(self.to_dict(), ensure_ascii=False, indent=2) + "\n"
        path.write_text(text, encoding="utf-8")
