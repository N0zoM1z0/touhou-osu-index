"""Advisory external composition-provenance checks.

External music databases are cross-checks, not authorities. A provider hit is
reported for review but never changes catalog confidence by itself.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path

from .catalog import Catalog
from .classifier import is_generic_touhou_source
from .http import HttpError, get_json
from .models import Entry

TOUHOUDb_API = "https://touhoudb.com/api/songs"
THBWIKI_API = "https://thwiki.cc/album.php"
TRUSTED_VERIFICATION_PREFIXES = (
    "official_pack:",
    "official_pack_item:",
    "tournament:",
    "tmc:",
)


def compact(value: str) -> str:
    value = unicodedata.normalize("NFKC", str(value)).casefold()
    return "".join(char for char in value if char.isalnum())


def artist_matches(left: str, right: str) -> bool:
    left_key, right_key = compact(left), compact(right)
    if not left_key or not right_key:
        return False
    if left_key == right_key:
        return True
    return min(len(left_key), len(right_key)) >= 5 and (
        left_key in right_key or right_key in left_key
    )


def _strings(value) -> list[str]:
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        return [str(item).strip() for item in value if str(item).strip()]
    return [part.strip() for part in re.split(r"[,;/]", str(value)) if part.strip()]


@dataclass(frozen=True)
class ProvenanceHit:
    provider: str
    verdict: str
    relation: str
    originals: tuple[str, ...] = ()
    provider_id: str = ""
    detail: str = ""
    url: str = ""

    def to_dict(self) -> dict:
        return {
            "provider": self.provider,
            "verdict": self.verdict,
            "relation": self.relation,
            "originals": list(self.originals),
            "provider_id": self.provider_id,
            "detail": self.detail,
            "url": self.url,
        }


@dataclass
class ProvenanceAudit:
    beatmapset_id: int
    artist: str
    title: str
    source: str
    confidence: str
    hits: list[ProvenanceHit] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def supports(self) -> list[ProvenanceHit]:
        return [hit for hit in self.hits if hit.verdict == "supports"]

    @property
    def contradictions(self) -> list[ProvenanceHit]:
        return [hit for hit in self.hits if hit.verdict == "contradicts"]

    @property
    def verdict(self) -> str:
        if self.supports and self.contradictions:
            return "ambiguous"
        if self.contradictions:
            return "red_flag"
        if self.supports:
            return "supported"
        return "unknown"

    def to_dict(self) -> dict:
        return {
            "beatmapset_id": self.beatmapset_id,
            "artist": self.artist,
            "title": self.title,
            "source": self.source,
            "confidence": self.confidence,
            "verdict": self.verdict,
            "hits": [hit.to_dict() for hit in self.hits],
            "errors": list(self.errors),
        }


def _touhoudb_names(item: dict) -> list[str]:
    names = [item.get("name", ""), item.get("defaultName", "")]
    names.extend(_strings(item.get("additionalNames")))
    return [name for name in names if name]


def _touhoudb_artists(item: dict) -> list[str]:
    values = [item.get("artistString", "")]
    for link in item.get("artists", []) or []:
        if not isinstance(link, dict):
            continue
        values.extend([link.get("name", ""), link.get("additionalNames", "")])
        nested = link.get("artist") or {}
        if isinstance(nested, dict):
            values.extend(
                [
                    nested.get("name", ""),
                    nested.get("defaultName", ""),
                    nested.get("additionalNames", ""),
                ]
            )
    artists: list[str] = []
    for value in values:
        artists.extend(_strings(value))
    return artists


def _song_type(item: dict) -> str:
    value = item.get("songType")
    if isinstance(value, dict):
        value = value.get("name") or value.get("value") or ""
    return str(value or "")


def query_touhoudb(entry: Entry) -> list[ProvenanceHit]:
    params = urllib.parse.urlencode(
        {
            "query": entry.title,
            "nameMatchMode": "Exact",
            "fields": "Artists,AdditionalNames,Albums",
            "maxResults": "30",
            "getTotalCount": "true",
        }
    )
    payload = get_json(f"{TOUHOUDb_API}?{params}")
    wanted_title = compact(entry.title)
    hits: list[ProvenanceHit] = []
    for item in payload.get("items", []) if isinstance(payload, dict) else []:
        if not isinstance(item, dict):
            continue
        if wanted_title not in {compact(name) for name in _touhoudb_names(item)}:
            continue
        artists = _touhoudb_artists(item)
        if not any(artist_matches(entry.artist, artist) for artist in artists):
            continue
        if item.get("status") not in (None, "Finished", "Approved", "Locked"):
            continue

        provider_id = str(item.get("id", ""))
        url = f"https://touhoudb.com/S/{provider_id}" if provider_id else "https://touhoudb.com/"
        original_id = item.get("originalVersionId")
        if original_id:
            hits.append(
                ProvenanceHit(
                    provider="touhoudb",
                    verdict="supports",
                    relation="arrangement",
                    provider_id=provider_id,
                    detail=f"originalVersionId={original_id}",
                    url=url,
                )
            )
        elif _song_type(item).casefold() == "original":
            if any(compact(artist) == "zun" for artist in artists):
                hits.append(
                    ProvenanceHit(
                        provider="touhoudb",
                        verdict="supports",
                        relation="zun_original",
                        provider_id=provider_id,
                        url=url,
                    )
                )
            else:
                hits.append(
                    ProvenanceHit(
                        provider="touhoudb",
                        verdict="contradicts",
                        relation="non_zun_original",
                        provider_id=provider_id,
                        detail=str(item.get("artistString", "")),
                        url=url,
                    )
                )
    return hits


def _thbwiki_detail(payload) -> list[dict]:
    parsed: list[dict] = []
    for item in payload if isinstance(payload, list) else []:
        if not isinstance(item, list):
            continue
        obj: dict = {}
        for pair in item:
            if isinstance(pair, list) and len(pair) == 2:
                obj[str(pair[0])] = pair[1]
        parsed.append(obj)
    return parsed


def query_thbwiki(entry: Entry) -> list[ProvenanceHit]:
    search_params = urllib.parse.urlencode(
        {"m": "st", "v": entry.title, "o": "1", "d": "0", "g": "0", "l": "30"}
    )
    rows = get_json(f"{THBWIKI_API}?{search_params}")
    exact_rows = [
        row
        for row in rows if isinstance(rows, list) and isinstance(row, list) and len(row) >= 2
        if isinstance(row[0], int) and compact(row[1]) == compact(entry.title)
    ]
    if not exact_rows:
        return []

    detail_params = urllib.parse.urlencode(
        {
            "m": "gt",
            "p": "name circle artist arrange ogmusic ogwork",
            "d": "0",
            "g": "0",
            "i": ",".join(str(row[0]) for row in exact_rows),
        }
    )
    candidates: list[tuple[dict, list[str], list[str], list[str], tuple[str, ...], list[str]]] = []
    for obj in _thbwiki_detail(get_json(f"{THBWIKI_API}?{detail_params}")):
        originals = tuple(_strings(obj.get("ogmusic")))
        if not originals:
            continue
        circles = _strings(obj.get("circle"))
        artists = _strings(obj.get("artist"))
        arrangers = _strings(obj.get("arrange"))
        works = _strings(obj.get("ogwork"))
        identities = circles + artists + arrangers
        if identities and not any(artist_matches(entry.artist, identity) for identity in identities):
            continue
        # A row with no identity metadata is not promoted to a positive relation:
        # exact title alone is too weak for common track names.
        if not identities:
            continue
        candidates.append((obj, circles, artists, arrangers, originals, works))

    hits: list[ProvenanceHit] = []
    for obj, circles, artists, arrangers, originals, works in candidates:
        provider_id = str(obj.get("id", ""))
        details: list[str] = []
        if circles:
            details.append("circle=" + ", ".join(circles))
        if artists:
            details.append("artist=" + ", ".join(artists))
        if arrangers:
            details.append("arrange=" + ", ".join(arrangers))
        if works:
            details.append("ogwork=" + ", ".join(works))
        hits.append(
            ProvenanceHit(
                provider="thbwiki",
                verdict="supports",
                relation="arrangement",
                originals=originals,
                provider_id=provider_id,
                detail="; ".join(details),
                url="https://thwiki.cc/",
            )
        )
    return hits


def audit_entry(entry: Entry) -> ProvenanceAudit:
    audit = ProvenanceAudit(
        beatmapset_id=entry.beatmapset_id,
        artist=entry.artist,
        title=entry.title,
        source=entry.source,
        confidence=entry.confidence,
    )
    for provider, function in (("touhoudb", query_touhoudb), ("thbwiki", query_thbwiki)):
        try:
            audit.hits.extend(function(entry))
        except (HttpError, RuntimeError, ValueError, TypeError) as exc:
            audit.errors.append(f"{provider}: {exc}")
    return audit


def audit_entries(entries: list[Entry], *, workers: int = 4) -> list[ProvenanceAudit]:
    if workers < 1:
        raise RuntimeError("provenance workers must be at least 1")
    results: list[ProvenanceAudit] = []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(audit_entry, entry): entry.beatmapset_id for entry in entries}
        for future in as_completed(futures):
            beatmapset_id = futures[future]
            try:
                results.append(future.result())
            except Exception as exc:  # defensive: preserve the report if one worker fails
                results.append(
                    ProvenanceAudit(
                        beatmapset_id=beatmapset_id,
                        artist="",
                        title="",
                        source="",
                        confidence="candidate",
                        errors=[f"audit: {exc}"],
                    )
                )
    return sorted(results, key=lambda item: item.beatmapset_id)


def has_independent_verification(entry: Entry) -> bool:
    evidence = set(entry.evidence)
    if "manual:verified" in evidence:
        return True
    return any(item.startswith(TRUSTED_VERIFICATION_PREFIXES) for item in evidence)


def new_generic_verification_violations(current: Catalog, base: Catalog) -> list[int]:
    """Return newly verified generic-source rows without independent evidence."""

    violations: list[int] = []
    for beatmapset_id, entry in current.entries.items():
        if not is_generic_touhou_source(entry.source) or entry.confidence != "verified":
            continue
        previous = base.entries.get(beatmapset_id)
        if previous is not None and previous.confidence == "verified":
            continue
        if has_independent_verification(entry):
            continue
        violations.append(beatmapset_id)
    return sorted(violations)


def _changed_entries(current: Catalog, base: Catalog) -> list[Entry]:
    return [
        current.entries[beatmapset_id]
        for beatmapset_id in sorted(current.entries)
        if base.entries.get(beatmapset_id) is None
        or base.entries[beatmapset_id].to_dict() != current.entries[beatmapset_id].to_dict()
    ]


def _report_payload(audits: list[ProvenanceAudit], violations: list[int]) -> dict:
    return {
        "checked": len(audits),
        "supported": sum(audit.verdict == "supported" for audit in audits),
        "red_flags": sum(audit.verdict == "red_flag" for audit in audits),
        "ambiguous": sum(audit.verdict == "ambiguous" for audit in audits),
        "unknown": sum(audit.verdict == "unknown" for audit in audits),
        "provider_errors": sum(bool(audit.errors) for audit in audits),
        "policy_violations": violations,
        "results": [audit.to_dict() for audit in audits],
    }


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--catalog", type=Path, default=Path("data/catalog"))
    result.add_argument("--base-catalog", type=Path)
    result.add_argument(
        "--scope",
        choices=("changed", "generic", "verified", "all"),
        default="changed",
        help="rows to query; changed requires --base-catalog",
    )
    result.add_argument("--workers", type=int, default=4)
    result.add_argument("--limit", type=int, default=0, help="maximum rows; 0 means unlimited")
    result.add_argument("--output", type=Path, help="write JSON report to this path")
    result.add_argument("--fail-on-policy-violation", action="store_true")
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    current = Catalog.load(args.catalog)
    base = Catalog.load(args.base_catalog) if args.base_catalog else None

    if args.scope == "changed":
        if base is None:
            print("error: --scope changed requires --base-catalog", file=sys.stderr)
            return 2
        targets = _changed_entries(current, base)
    elif args.scope == "generic":
        targets = [entry for entry in current.entries.values() if is_generic_touhou_source(entry.source)]
    elif args.scope == "verified":
        targets = [entry for entry in current.entries.values() if entry.confidence == "verified"]
    else:
        targets = list(current.entries.values())

    targets = sorted(targets, key=lambda entry: entry.beatmapset_id)
    if args.limit:
        targets = targets[: args.limit]

    violations = new_generic_verification_violations(current, base) if base is not None else []
    audits = audit_entries(targets, workers=args.workers)
    payload = _report_payload(audits, violations)
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")

    print(
        "Provenance: "
        f"checked={payload['checked']} supported={payload['supported']} "
        f"red_flags={payload['red_flags']} ambiguous={payload['ambiguous']} "
        f"unknown={payload['unknown']} provider_errors={payload['provider_errors']} "
        f"policy_violations={len(violations)}",
        file=sys.stderr,
    )
    if args.fail_on_policy_violation and violations:
        print(
            "unsafe generic-source auto-verification: " + ", ".join(map(str, violations)),
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
