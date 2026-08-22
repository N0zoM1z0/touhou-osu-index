"""Load, merge, and save the canonical catalog."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable

from .models import CatalogError, Entry

SCHEMA_VERSION = 1
CONFIDENCE_RANK = {"excluded": -1, "candidate": 0, "probable": 1, "verified": 2}
SHARD_ID_SPAN = 25_000
SHARD_ENTRY_LIMIT = 500
SHARD_NAME_RE = re.compile(r"^(\d{7})-(\d{7})\.json$")


class Catalog:
    def __init__(self, entries: Iterable[Entry] = ()) -> None:
        self.entries: dict[int, Entry] = {}
        for entry in entries:
            if entry.beatmapset_id in self.entries:
                raise CatalogError(f"duplicate beatmapset_id: {entry.beatmapset_id}")
            self.entries[entry.beatmapset_id] = entry

    @classmethod
    def load(cls, path: Path) -> "Catalog":
        if path.is_dir():
            return cls._load_shards(path)
        return cls._load_file(path)

    @classmethod
    def _load_file(cls, path: Path) -> "Catalog":
        raw = json.loads(path.read_text(encoding="utf-8"))
        records = cls._records_from_payload(raw, path)
        return cls(Entry.from_dict(record) for record in records)

    @staticmethod
    def _records_from_payload(raw: dict, path: Path) -> list[dict]:
        if raw.get("schema_version") != SCHEMA_VERSION:
            raise CatalogError(
                f"unsupported schema_version in {path}: {raw.get('schema_version')!r}"
            )
        records = raw.get("entries")
        if not isinstance(records, list):
            raise CatalogError(f"catalog entries in {path} must be a list")
        ids = [record.get("beatmapset_id") for record in records]
        if ids != sorted(ids):
            raise CatalogError(f"catalog entries in {path} must be sorted by numeric beatmapset_id")
        return records

    @classmethod
    def _load_shards(cls, directory: Path) -> "Catalog":
        paths = sorted(directory.glob("*.json"))
        if not paths:
            raise CatalogError(f"catalog shard directory is empty: {directory}")
        records: list[dict] = []
        for path in paths:
            match = SHARD_NAME_RE.fullmatch(path.name)
            if match is None:
                raise CatalogError(f"unexpected catalog shard filename: {path.name}")
            lower, upper = map(int, match.groups())
            if lower % SHARD_ID_SPAN or upper != lower + SHARD_ID_SPAN - 1:
                raise CatalogError(f"invalid catalog shard range: {path.name}")
            shard_records = cls._records_from_payload(
                json.loads(path.read_text(encoding="utf-8")), path
            )
            if len(shard_records) > SHARD_ENTRY_LIMIT:
                raise CatalogError(
                    f"catalog shard {path.name} has {len(shard_records)} entries; "
                    f"limit is {SHARD_ENTRY_LIMIT}"
                )
            misplaced = [
                record.get("beatmapset_id")
                for record in shard_records
                if not isinstance(record.get("beatmapset_id"), int)
                or not lower <= record["beatmapset_id"] <= upper
            ]
            if misplaced:
                raise CatalogError(
                    f"catalog shard {path.name} contains IDs outside its range: {misplaced[:5]}"
                )
            records.extend(shard_records)
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
        elif "manual:candidate" in manual:
            current.confidence = "candidate"
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
        if path.is_dir() or path.suffix != ".json":
            self.save_shards(path)
        else:
            self.save_aggregate(path)

    def save_aggregate(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        text = json.dumps(self.to_dict(), ensure_ascii=False, indent=2) + "\n"
        path.write_text(text, encoding="utf-8")

    @staticmethod
    def shard_name(beatmapset_id: int) -> str:
        lower = beatmapset_id // SHARD_ID_SPAN * SHARD_ID_SPAN
        upper = lower + SHARD_ID_SPAN - 1
        return f"{lower:07d}-{upper:07d}.json"

    def save_shards(self, directory: Path) -> None:
        self.validate()
        directory.mkdir(parents=True, exist_ok=True)
        shards: dict[str, list[dict]] = {}
        for beatmapset_id in sorted(self.entries):
            name = self.shard_name(beatmapset_id)
            shards.setdefault(name, []).append(self.entries[beatmapset_id].to_dict())

        oversized = {
            name: len(records)
            for name, records in shards.items()
            if len(records) > SHARD_ENTRY_LIMIT
        }
        if oversized:
            details = ", ".join(f"{name}={count}" for name, count in sorted(oversized.items()))
            raise CatalogError(
                f"catalog shards exceed the {SHARD_ENTRY_LIMIT}-entry limit: {details}"
            )

        for name, records in shards.items():
            path = directory / name
            text = json.dumps(
                {"schema_version": SCHEMA_VERSION, "entries": records},
                ensure_ascii=False,
                indent=2,
            ) + "\n"
            if not path.exists() or path.read_text(encoding="utf-8") != text:
                path.write_text(text, encoding="utf-8")

        expected = set(shards)
        for path in directory.glob("*.json"):
            if SHARD_NAME_RE.fullmatch(path.name) and path.name not in expected:
                path.unlink()
