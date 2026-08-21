from __future__ import annotations

import json
import re
import sys
import unicodedata
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from touhou_osu.catalog import Catalog
from touhou_osu.osu_api import OsuApi

STATUS_LOG = Path(sys.argv[1])


def norm(value: str) -> str:
    return "".join(
        ch
        for ch in unicodedata.normalize("NFKC", value or "").casefold()
        if ch.isalnum()
    )


def load_status_report(path: Path) -> dict:
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    begins = [i for i, line in enumerate(lines) if "NIGHT_STATUS_ENUM_BEGIN" in line]
    ends = [i for i, line in enumerate(lines) if "NIGHT_STATUS_ENUM_END" in line]
    assert begins and ends
    begin = begins[-1]
    end = next(i for i in ends if i > begin)
    payload = []
    for line in lines[begin + 1 : end]:
        payload.append(
            re.sub(
                r"^.*?\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z\s*",
                "",
                line,
            )
        )
    text = "\n".join(payload).strip()
    return json.loads(text[text.find("{") : text.rfind("}") + 1])


BASE = {
    norm(x)
    for x in [
        "ナイト・オブ・ナイツ",
        "Night of Nights",
        "Night of Knights",
        "Knight of Nights",
    ]
}


def bucket(raw: dict) -> str:
    title = raw.get("title", "")
    low = title.casefold()
    title_n = norm(title)
    if any(token in low for token in ["mashup", " but ", " x ", "wall of", "number one", "friday night"]):
        return "mashup_or_meme"
    if any(token in low for token in ["remix", "cover", "piano", "sax", "phone", "telephone", "arrenge", "arrangement"]):
        return "cover_or_remix"
    if title_n in BASE:
        return "base_unattributed"
    return "other_variant"


report = load_status_report(STATUS_LOG)
catalog = Catalog.load(Path("data/catalog.json"))
remaining_ids = [
    int(row["beatmapset_id"])
    for row in report["missing"]
    if int(row["beatmapset_id"]) not in catalog.entries
]
assert len(remaining_ids) == 94, (len(remaining_ids), remaining_ids)

api = OsuApi.from_env()
api.token()


def fetch(beatmapset_id: int) -> dict:
    raw = api.beatmapset(beatmapset_id)
    assert int(raw["id"]) == beatmapset_id
    return raw


with ThreadPoolExecutor(max_workers=8) as pool:
    rows = list(pool.map(fetch, remaining_ids))

counts = Counter(bucket(row) for row in rows)
print("NIGHT_UNRESOLVED_LIVE_AUDIT_BEGIN")
print("remaining=", len(rows))
print("buckets=", json.dumps(dict(sorted(counts.items())), ensure_ascii=False))
for raw in sorted(rows, key=lambda row: int(row["id"])):
    fields = [
        str(raw["id"]),
        raw.get("status", ""),
        bucket(raw),
        raw.get("artist", ""),
        raw.get("title", ""),
        raw.get("source", ""),
        raw.get("tags", ""),
    ]
    clean = [str(value).replace("|", "/").replace("\n", " ") for value in fields]
    print("REMAIN|" + "|".join(clean))
print("NIGHT_UNRESOLVED_LIVE_AUDIT_END")
