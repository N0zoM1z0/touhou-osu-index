"""Deterministic, explainable Touhou confidence classification."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

from .models import Entry

EXACT_TOUHOU_SOURCES = (
    "touhou",
    "touhou project",
    "東方",
    "東方project",
    "東方プロジェクト",
)

# A concrete game title is substantially stronger than a generic "Touhou"
# label. Generic labels are useful discovery signals, but are not sufficient
# composition provenance on their own.
TOUHOU_GAME_TITLE_TOKENS = (
    "highly responsive to prayers",
    "story of eastern wonderland",
    "phantasmagoria of dim.dream",
    "lotus land story",
    "mystic square",
    "embodiment of scarlet devil",
    "perfect cherry blossom",
    "immaterial and missing power",
    "imperishable night",
    "phantasmagoria of flower view",
    "shoot the bullet",
    "mountain of faith",
    "scarlet weather rhapsody",
    "subterranean animism",
    "undefined fantastic object",
    "touhou hisoutensoku",
    "double spoiler",
    "great fairy wars",
    "ten desires",
    "hopeless masquerade",
    "double dealing character",
    "impossible spell card",
    "urban legend in limbo",
    "legacy of lunatic kingdom",
    "antinomy of common flowers",
    "hidden star in four seasons",
    "violet detector",
    "wily beast and weakest creature",
    "sunken fossil world",
    "unconnected marketeers",
    "100th black market",
    "unfinished dream of all living ghost",
    "fossilized wonders",
    "東方靈異伝",
    "東方封魔録",
    "東方夢時空",
    "東方幻想郷",
    "東方怪綺談",
    "東方紅魔郷",
    "東方妖々夢",
    "東方萃夢想",
    "東方永夜抄",
    "東方花映塚",
    "東方文花帖",
    "東方風神録",
    "東方緋想天",
    "東方地霊殿",
    "東方星蓮船",
    "東方非想天則",
    "ダブルスポイラー",
    "妖精大戦争",
    "東方神霊廟",
    "東方心綺楼",
    "東方輝針城",
    "弾幕アマノジャク",
    "東方深秘録",
    "東方紺珠伝",
    "東方憑依華",
    "東方天空璋",
    "秘封ナイトメアダイアリー",
    "東方鬼形獣",
    "東方剛欲異聞",
    "東方虹龍洞",
    "バレットフィリア達の闇市場",
    "東方獣王園",
    "東方錦上京",
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


def normalized_source(value: str) -> str:
    return normalize(value).strip(" .,:：;_-~～")


def is_generic_touhou_source(value: str) -> bool:
    normalized = normalized_source(value)
    return normalized in {normalize(source) for source in EXACT_TOUHOU_SOURCES}


def is_touhou_game_source(value: str) -> bool:
    normalized = normalized_source(value)
    if not normalized or is_generic_touhou_source(normalized):
        return False
    return contains_any(normalized, TOUHOU_GAME_TITLE_TOKENS)


def is_explicit_touhou_source(value: str) -> bool:
    """Return whether source metadata explicitly signals Touhou relevance.

    This broad predicate intentionally includes generic labels for discovery and
    audit purposes. Classification distinguishes generic labels from concrete
    game titles and only auto-verifies the latter.
    """

    return is_generic_touhou_source(value) or is_touhou_game_source(value)


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
    if "manual:candidate" in evidence:
        return Classification("candidate", tuple(sorted(evidence)))

    if any(
        item.startswith(("official_pack:", "official_pack_item:", "tournament:", "tmc:"))
        for item in evidence
    ):
        return Classification("verified", tuple(sorted(evidence)))

    if is_touhou_game_source(entry.source):
        evidence.add("osu_source")
        return Classification("verified", tuple(sorted(evidence)))

    # Keep the existing evidence vocabulary for compatibility and to avoid a
    # one-time catalog backfill that would consume the weekly meaningful-change
    # cap. The current source value itself determines whether this signal is
    # generic or game-specific.
    if is_generic_touhou_source(entry.source):
        evidence.add("osu_source")

    curated_queue_match = any(item.startswith("forum_queue:") for item in evidence)
    resolved_metadata = bool(entry.artist and entry.title and not entry.title.startswith("beatmapsets/"))
    if curated_queue_match and resolved_metadata:
        return Classification("probable", tuple(sorted(evidence)))

    tags_match = contains_any(tags, TOUHOU_TAG_TOKENS)
    artist_match = normalize(entry.artist) in {normalize(item) for item in KNOWN_ARTISTS}
    curated_collection_match = any(item.startswith("osucollector:") for item in evidence)
    if tags_match and artist_match and curated_collection_match:
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
