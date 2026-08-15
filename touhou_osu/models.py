"""Canonical catalog models and validation."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from typing import Any

CONFIDENCES = ("verified", "probable", "candidate", "excluded")
KINDS = ("original", "arrangement", "mixed", "unknown")
MODES = ("osu", "taiko", "catch", "mania")
STATUSES = (
    "approved",
    "deleted",
    "graveyard",
    "loved",
    "pending",
    "qualified",
    "ranked",
    "unknown",
    "wip",
)
MODE_ALIASES = {"fruits": "catch", "ctb": "catch", "standard": "osu"}


class CatalogError(ValueError):
    """Raised when canonical data violates the schema."""


def normalize_mode(value: str) -> str:
    return MODE_ALIASES.get(value.casefold(), value.casefold())


def _sorted_unique(values: list[str] | tuple[str, ...]) -> list[str]:
    return sorted({str(value).strip() for value in values if str(value).strip()}, key=str.casefold)


def _validate_date(value: str | None, field_name: str, *, timestamp: bool = False) -> None:
    if value is None:
        return
    try:
        if timestamp:
            datetime.fromisoformat(value.replace("Z", "+00:00"))
        else:
            date.fromisoformat(value)
    except ValueError as exc:
        raise CatalogError(f"invalid {field_name}: {value!r}") from exc


@dataclass
class Entry:
    beatmapset_id: int
    artist: str = ""
    title: str = ""
    creator: str = ""
    source: str = ""
    status: str = "unknown"
    modes: list[str] = field(default_factory=list)
    touhou_kind: str = "unknown"
    origin_games: list[str] = field(default_factory=list)
    original_themes: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    confidence: str = "candidate"
    last_checked: str | None = None
    osu_last_updated: str | None = None

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "Entry":
        allowed = set(cls.__dataclass_fields__)
        extra = set(raw) - allowed
        if extra:
            raise CatalogError(f"beatmapset {raw.get('beatmapset_id', '?')}: unknown fields: {sorted(extra)}")
        try:
            entry = cls(**raw)
        except TypeError as exc:
            raise CatalogError(f"invalid entry: {exc}") from exc
        entry.normalize()
        entry.validate()
        return entry

    def normalize(self) -> None:
        self.beatmapset_id = int(self.beatmapset_id)
        self.artist = str(self.artist).strip()
        self.title = str(self.title).strip()
        self.creator = str(self.creator).strip()
        self.source = str(self.source).strip()
        self.status = str(self.status).casefold().strip() or "unknown"
        self.modes = _sorted_unique([normalize_mode(value) for value in self.modes])
        self.touhou_kind = str(self.touhou_kind).casefold().strip() or "unknown"
        self.origin_games = _sorted_unique(self.origin_games)
        self.original_themes = _sorted_unique(self.original_themes)
        self.evidence = _sorted_unique(self.evidence)
        self.confidence = str(self.confidence).casefold().strip()

    def validate(self) -> None:
        if self.beatmapset_id <= 0:
            raise CatalogError(f"beatmapset_id must be positive: {self.beatmapset_id}")
        if self.status not in STATUSES:
            raise CatalogError(f"beatmapset {self.beatmapset_id}: unknown status {self.status!r}")
        unknown_modes = set(self.modes) - set(MODES)
        if unknown_modes:
            raise CatalogError(f"beatmapset {self.beatmapset_id}: unknown modes {sorted(unknown_modes)}")
        if self.touhou_kind not in KINDS:
            raise CatalogError(f"beatmapset {self.beatmapset_id}: unknown Touhou kind {self.touhou_kind!r}")
        if self.confidence not in CONFIDENCES:
            raise CatalogError(f"beatmapset {self.beatmapset_id}: unknown confidence {self.confidence!r}")
        if not self.evidence:
            raise CatalogError(f"beatmapset {self.beatmapset_id}: evidence is required")
        _validate_date(self.last_checked, "last_checked")
        _validate_date(self.osu_last_updated, "osu_last_updated", timestamp=True)

    def to_dict(self) -> dict[str, Any]:
        self.normalize()
        self.validate()
        return asdict(self)
