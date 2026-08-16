"""Import reproducible seed sources without osu! OAuth credentials."""

from __future__ import annotations

import json
import re
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import date
from html.parser import HTMLParser

from .classifier import apply_classification
from .google_sheets import fetch_google_sheet_beatmapset_ids
from .http import get_json, get_text
from .models import Entry, normalize_mode

BEATMAPSET_RE = re.compile(r"/beatmapsets/(\d+)(?:#(osu|taiko|fruits|mania))?")
FORUM_POST_ID_RE = re.compile(r'data-post-id="(\d+)"')
MARKDOWN_BEATMAPSET_RE = re.compile(
    r"\[([^\n]*?)\]\(https?://osu\.ppy\.sh/beatmapsets/(\d+)(?:#(osu|taiko|fruits|mania)/\d+)?\)"
)


@dataclass(frozen=True)
class SourceReport:
    kind: str
    name: str
    url: str
    beatmapsets: int

    def message(self) -> str:
        return f"{self.kind}/{self.name}: {self.beatmapsets} beatmapsets ({self.url})"


class BeatmapLinkParser(HTMLParser):
    """Extract beatmapset links and visible metadata from osu! HTML."""

    def __init__(self) -> None:
        super().__init__()
        self.links: list[dict] = []
        self._current: dict | None = None
        self._field: str | None = None
        self._pending_mode = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        classes = (attributes.get("class") or "").split()
        for class_name in classes:
            if class_name.startswith("fa-extra-mode-"):
                self._pending_mode = normalize_mode(class_name.removeprefix("fa-extra-mode-"))
        if tag == "a":
            match = BEATMAPSET_RE.search(attributes.get("href", "") or "")
            if match:
                self._current = {
                    "id": int(match.group(1)),
                    "mode": normalize_mode(match.group(2)) if match.group(2) else self._pending_mode,
                    "artist": "",
                    "title": "",
                    "text": "",
                }
        elif tag == "span" and self._current is not None:
            if "beatmap-pack-items__artist" in classes:
                self._field = "artist"
            elif "beatmap-pack-items__title" in classes:
                self._field = "title"

    def handle_data(self, data: str) -> None:
        if self._current is None:
            return
        self._current["text"] += data
        if self._field:
            self._current[self._field] += data

    def handle_endtag(self, tag: str) -> None:
        if tag == "span":
            self._field = None
        elif tag == "a" and self._current is not None:
            for key in ("artist", "title", "text"):
                self._current[key] = " ".join(self._current[key].split()).strip(" -–")
            if not self._current["artist"] and self._current["text"]:
                parts = re.split(r"\s+(?:-|–|—)\s+", self._current["text"], maxsplit=1)
                if len(parts) == 2:
                    self._current["artist"], self._current["title"] = parts
                else:
                    self._current["title"] = self._current["text"]
            self.links.append(self._current)
            self._current = None
            self._field = None
            self._pending_mode = ""


class JsonScriptParser(HTMLParser):
    def __init__(self, target_id: str) -> None:
        super().__init__()
        self.target_id = target_id
        self._capture = False
        self.value = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._capture = tag == "script" and dict(attrs).get("id") == self.target_id

    def handle_data(self, data: str) -> None:
        if self._capture:
            self.value += data

    def handle_endtag(self, tag: str) -> None:
        if tag == "script":
            self._capture = False


def parse_beatmap_links(text: str) -> list[dict]:
    parser = BeatmapLinkParser()
    parser.feed(text)
    by_id: dict[int, dict] = {}
    for item in parser.links:
        current = by_id.get(item["id"])
        if current is None:
            by_id[item["id"]] = item
        elif item["mode"] and not current["mode"]:
            current["mode"] = item["mode"]
    return list(by_id.values())


def parse_wiki_links(text: str) -> list[dict]:
    """Parse either osu! wiki JSON/Markdown or rendered HTML."""
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return parse_beatmap_links(text)
    markdown = payload.get("markdown", "")
    links: dict[int, dict] = {}
    for label, beatmapset_id, mode in MARKDOWN_BEATMAPSET_RE.findall(markdown):
        label = label.replace("\\[", "[").replace("\\]", "]").strip()
        parts = re.split(r"\s+(?:-|–|—)\s+", label, maxsplit=1)
        artist, title = (parts[0], parts[1]) if len(parts) == 2 else ("", label)
        item = {
            "id": int(beatmapset_id),
            "mode": normalize_mode(mode) if mode else "",
            "artist": artist,
            "title": title,
            "text": label,
        }
        links.setdefault(item["id"], item)
    return list(links.values())


def parse_beatmapset_page(text: str) -> dict:
    parser = JsonScriptParser("json-beatmapset")
    parser.feed(text)
    if not parser.value.strip():
        raise ValueError("osu! beatmapset page did not contain json-beatmapset")
    return json.loads(parser.value)


def _collector_entry(raw: dict, evidence: str, confidence: str, kind: str = "unknown") -> Entry | None:
    beatmapset = raw.get("beatmapset") or {}
    beatmapset_id = raw.get("beatmapset_id") or beatmapset.get("id")
    if not beatmapset_id:
        return None
    entry = Entry(
        beatmapset_id=beatmapset_id,
        artist=beatmapset.get("artist", ""),
        title=beatmapset.get("title", ""),
        creator=beatmapset.get("creator", ""),
        status=beatmapset.get("status") or raw.get("status", "unknown"),
        modes=[raw["mode"]] if raw.get("mode") else [],
        touhou_kind=kind,
        evidence=[evidence],
        confidence=confidence,
        last_checked=date.today().isoformat(),
        osu_last_updated=beatmapset.get("last_updated"),
    )
    return apply_classification(entry)


def import_collector_collection(source: dict) -> list[Entry]:
    source_id = int(source["id"])
    evidence = f"osucollector:{source_id}"
    params = {"perPage": "100", "sortBy": "beatmapset.artist", "orderBy": "asc"}
    cursor = None
    entries: dict[int, Entry] = {}
    while True:
        if cursor is not None:
            params["cursor"] = str(cursor)
        url = f"https://osucollector.com/api/collections/{source_id}/beatmapsv2?{urllib.parse.urlencode(params)}"
        payload = get_json(url)
        for raw in payload.get("beatmaps", []):
            incoming = _collector_entry(
                raw,
                evidence,
                source.get("confidence", "candidate"),
                source.get("touhou_kind", "unknown"),
            )
            if incoming is None:
                continue
            current = entries.get(incoming.beatmapset_id)
            if current is None:
                entries[incoming.beatmapset_id] = incoming
            else:
                current.modes = sorted(set(current.modes) | set(incoming.modes))
        if not payload.get("hasMore") or payload.get("nextPageCursor") is None:
            break
        cursor = payload["nextPageCursor"]
    return list(entries.values())


def import_collector_tournament(source: dict) -> list[Entry]:
    source_id = int(source["id"])
    trusted = bool(source.get("trusted", True))
    evidence = f"tournament:{source_id}" if trusted else f"tournament_candidate:{source_id}"
    confidence = "verified" if trusted else source.get("confidence", "candidate")
    payload = get_json(source.get("api_url", f"https://osucollector.com/api/tournaments/{source_id}"))
    entries: dict[int, Entry] = {}
    for round_data in payload.get("rounds", []):
        for mod in round_data.get("mods", []):
            for raw in mod.get("maps", []):
                incoming = _collector_entry(raw, evidence, confidence)
                if incoming is None:
                    continue
                current = entries.get(incoming.beatmapset_id)
                if current is None:
                    entries[incoming.beatmapset_id] = incoming
                else:
                    current.modes = sorted(set(current.modes) | set(incoming.modes))
    return list(entries.values())


def import_official_pack(source: dict) -> list[Entry]:
    tag = source["tag"]
    url = source.get("url", f"https://osu.ppy.sh/beatmaps/packs/{tag}")
    links = parse_beatmap_links(get_text(url))
    evidence = f"official_pack:{tag}"
    return [
        Entry(
            beatmapset_id=item["id"],
            artist=item["artist"],
            title=item["title"],
            modes=[item["mode"]] if item["mode"] else [],
            evidence=[evidence],
            confidence="verified",
            last_checked=date.today().isoformat(),
        )
        for item in links
    ]


def import_wiki_tournament(source: dict) -> list[Entry]:
    evidence = f"tmc:{source['edition']}"
    links = parse_wiki_links(get_text(source["url"]))
    return [
        Entry(
            beatmapset_id=item["id"],
            artist=item["artist"],
            title=item["title"],
            modes=[item["mode"]] if item["mode"] else ["mania"],
            evidence=[evidence],
            confidence="verified",
            last_checked=date.today().isoformat(),
        )
        for item in links
    ]


def import_google_sheet_tournament(source: dict) -> list[Entry]:
    """Import a reproducible tournament pool from selected Google Sheet tabs."""
    source_id = str(source["id"])
    trusted = bool(source.get("trusted", True))
    evidence = (
        f"tournament:google_sheet:{source_id}"
        if trusted
        else f"tournament_candidate:google_sheet:{source_id}"
    )
    confidence = "verified" if trusted else source.get("confidence", "candidate")
    beatmapset_ids = fetch_google_sheet_beatmapset_ids(
        source["spreadsheet_id"],
        sheet_names=source.get("sheet_names", ()),
        sheet_prefixes=source.get("sheet_prefixes", ()),
    )
    return [
        apply_classification(
            Entry(
                beatmapset_id=beatmapset_id,
                evidence=[evidence],
                confidence=confidence,
                last_checked=date.today().isoformat(),
            )
        )
        for beatmapset_id in beatmapset_ids
    ]


def _forum_page_url(url: str, start: int | None) -> str:
    if start is None:
        return url
    parsed = urllib.parse.urlsplit(url)
    query = dict(urllib.parse.parse_qsl(parsed.query, keep_blank_values=True))
    query["start"] = str(start)
    return urllib.parse.urlunsplit(
        (parsed.scheme, parsed.netloc, parsed.path, urllib.parse.urlencode(query), parsed.fragment)
    )


def import_forum_queue(source: dict) -> list[Entry]:
    """Import every beatmapset linked in a paginated osu! forum queue."""
    slug = source["slug"]
    evidence = f"forum_queue:{slug}"
    entries: dict[int, Entry] = {}
    start: int | None = None
    seen_last_posts: set[int] = set()
    max_pages = int(source.get("max_pages", 20))

    for _ in range(max_pages):
        text = get_text(_forum_page_url(source["url"], start))
        for item in parse_beatmap_links(text):
            incoming = Entry(
                beatmapset_id=item["id"],
                artist=item["artist"],
                title=item["title"],
                modes=[item["mode"]] if item["mode"] else [],
                evidence=[evidence],
                # A bare forum link is kept out of the public index until its
                # beatmapset metadata can be resolved and classified.
                confidence="candidate",
                last_checked=date.today().isoformat(),
            )
            current = entries.get(incoming.beatmapset_id)
            if current is None:
                entries[incoming.beatmapset_id] = incoming
            else:
                current.modes = sorted(set(current.modes) | set(incoming.modes))

        post_ids = [int(value) for value in FORUM_POST_ID_RE.findall(text)]
        if not post_ids:
            raise RuntimeError(f"forum queue {slug} did not contain any forum posts")
        last_post = post_ids[-1]
        if last_post == start or last_post in seen_last_posts:
            return list(entries.values())
        seen_last_posts.add(last_post)
        start = last_post

    raise RuntimeError(f"forum queue {slug} exceeded its {max_pages}-page safety limit")


def source_url(kind: str, source: dict) -> str:
    if source.get("url"):
        return source["url"]
    if kind == "osu_collector_collections":
        return f"https://osucollector.com/collections/{source['id']}"
    if kind == "osu_collector_tournaments":
        return source.get("api_url", f"https://osucollector.com/api/tournaments/{source['id']}")
    if kind == "official_packs":
        return f"https://osu.ppy.sh/beatmaps/packs/{source['tag']}"
    if kind == "google_sheet_tournaments":
        return f"https://docs.google.com/spreadsheets/d/{source['spreadsheet_id']}/edit"
    return "unknown"


def import_source(kind: str, source: dict) -> list[Entry]:
    if kind == "osu_collector_collections":
        return import_collector_collection(source)
    if kind == "osu_collector_tournaments":
        return import_collector_tournament(source)
    if kind == "official_packs":
        return import_official_pack(source)
    if kind == "wiki_tournaments":
        return import_wiki_tournament(source)
    if kind == "google_sheet_tournaments":
        return import_google_sheet_tournament(source)
    if kind == "forum_queues":
        return import_forum_queue(source)
    raise ValueError(f"unsupported seed source type: {kind}")


def import_all(config: dict, *, workers: int = 4) -> tuple[list[Entry], list[SourceReport]]:
    tasks = [
        (kind, source)
        for kind in (
            "osu_collector_collections",
            "osu_collector_tournaments",
            "official_packs",
            "wiki_tournaments",
            "google_sheet_tournaments",
            "forum_queues",
        )
        for source in config.get(kind, [])
    ]
    entries: list[Entry] = []
    reports: list[SourceReport] = []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(import_source, kind, source): (kind, source) for kind, source in tasks}
        for future in as_completed(futures):
            kind, source = futures[future]
            label = source.get("name") or source.get("tag") or source.get("edition") or source.get("id")
            imported = future.result()
            minimum = int(source.get("minimum_entries", 1))
            if len(imported) < minimum:
                raise RuntimeError(
                    f"{kind}/{label} returned {len(imported)} beatmapsets; expected at least {minimum}"
                )
            entries.extend(imported)
            reports.append(SourceReport(kind, str(label), source_url(kind, source), len(imported)))
    return entries, sorted(reports, key=lambda item: (item.kind, item.name.casefold()))
