"""Deterministic, explainable Touhou confidence classification."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

from .models import Entry

TOUHOU_SOURCE_TOKENS = (
    "touhou",
    "東方",
    "embodiment of scarlet devil",
    "perfect cherry blossom",
    "imperishable night",
    "phantasmagoria of flower view",
    "mountain of faith",
    "subterranean animism",
    "undefined fantastic object",
    "ten desires",
    "double dealing character",
    "legacy of lunatic kingdom",
    "hidden star in four seasons",
    "wily beast and weakest creature",
    "unconnected marketeers",
    "unfinished dream of all living ghost",
)
TOUHOU_TAG_TOKENS = ("touhou", "東方project", "team shanghai alice", "上海アリス幻樂団")
KNOWN_ARTISTS = {
    "zun",
    "a-one",
    "adust rain",
    "alstroemeria records",
    "butaotome",
    "c-clays",
    "cool&create",
    "diao ye zong",
    "halozy",
    "iosys",
    "leaF",
    "shinigiwa satellite",
    "shinra-bansho",
    "shibayanrecords",
    "syrufit",
    "unlucky morpheus",
    "undead corporation",
}


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).casefold()
    return re.sub(r"\s+", " ", value).strip()


def contains_any(value: str, tokens: tuple[str, ...] | set[str]) -> bool:
    normalized = normalize(value)
    return any(normalize(token) in normalized for token in tokens)


@dataclass(frozen=True)
class Classification:
    confidence: str
    evidence: tuple[str, ...]


def classify(entry: Entry, *, tags: str = "") -> Classification:
    evidence = set(entry.evidence)
    if "manual:excluded" in evidence:
        return Classification("excluded", tuple(sorted(evidence)))
    if "manual:verified" in evidence:
        return Classification("verified", tuple(sorted(evidence)))

    if any(item.startswith(("official_pack:", "tournament:", "tmc:")) for item in evidence):
        return Classification("verified", tuple(sorted(evidence)))

    if contains_any(entry.source, TOUHOU_SOURCE_TOKENS):
        evidence.add("osu_source")
        return Classification("verified", tuple(sorted(evidence)))

    tags_match = contains_any(tags, TOUHOU_TAG_TOKENS)
    artist_match = normalize(entry.artist) in {normalize(item) for item in KNOWN_ARTISTS}
    metadata_match = artist_match or contains_any(f"{entry.artist} {entry.title}", TOUHOU_SOURCE_TOKENS)
    if tags_match and metadata_match:
        evidence.update(("mapper_tags", "known_touhou_metadata"))
        return Classification("probable", tuple(sorted(evidence)))

    if tags_match:
        evidence.add("mapper_tags")
    if artist_match:
        evidence.add("known_touhou_artist")
    confidence = entry.confidence if entry.confidence in ("probable", "candidate") else "candidate"
    return Classification(confidence, tuple(sorted(evidence)))


def apply_classification(entry: Entry, *, tags: str = "") -> Entry:
    result = classify(entry, tags=tags)
    entry.confidence = result.confidence
    entry.evidence = list(result.evidence)
    return entry
