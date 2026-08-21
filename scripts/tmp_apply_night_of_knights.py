from __future__ import annotations

import json
import re
import sys
import unicodedata
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from touhou_osu.catalog import Catalog
from touhou_osu.classifier import apply_classification, is_explicit_touhou_source
from touhou_osu.osu_api import OsuApi, entry_from_osu

STATUS_LOG = Path(sys.argv[1])


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


def norm(value: str) -> str:
    return "".join(
        ch
        for ch in unicodedata.normalize("NFKC", value or "").casefold()
        if ch.isalnum()
    )


BASE = [norm(x) for x in ["ナイト・オブ・ナイツ", "Night of Nights", "Night of Knights", "Knight of Nights"]]
TOKENS = [
    "thousandknives",
    "elementasremix",
    "豚乙女ver",
    "alrremix",
    "crankyremix",
    "tosremix",
    "緋想天mix",
    "少女理論観測所ver",
    "tpzoverheatremix",
    "狐夢想style",
    "iqの低いナイツ",
    "かめりあ",
    "onceuponanight",
    "kors kremix",
    "usaoremix",
    "amaterasrecordsremix",
    "armremix",
    "redaliceremix",
    "maronbounce",
    "higedriverremix",
    "xiremix",
    "mrmremix",
    "crankyvstpazolite",
    "ryu remix",
    "gamesize",
    "超ナイトオブナイツ",
    "chounightofknights",
    "choknightofknights",
    "cosmobsp398",
    "マサラダremix",
    "chromaremix",
    "32kidosancore",
    "原口オブリミックス",
    "南ノ南ahwowremix",
    "namigrooveremix",
    "八王子premix",
    "sawtowneremix",
    "reナイトオブナイツ",
]
NTOK = [norm(x) for x in TOKENS]
KNOWN_REMIXERS = [
    norm(x)
    for x in [
        "Cranky",
        "t+pazolite",
        "Camellia",
        "かめりあ",
        "kors k",
        "USAO",
        "REDALiCE",
        "MARON",
        "Hige Driver",
        "xi",
        "Morimori Atsushi",
        "モリモリあつし",
        "Ryu",
        "Amateras Records",
        "Chroma",
        "黒魔",
        "八王子P",
        "cosMo",
        "SAWTOWNE",
        "marasy",
        "まらしぃ",
        "A-One",
        "IOSYS",
        "SOUND HOLIC",
        "Masayoshi Minoshima",
    ]
]


def base_exact(title: str) -> bool:
    return norm(title) in BASE


def parent_artist(artist: str) -> bool:
    value = norm(artist)
    return "beatmario" in value or "coolcreate" in value or value == "ビートまりお"


def official_exactish(artist: str, title: str) -> bool:
    title_n = norm(title)
    artist_n = norm(artist)
    if not any(token and token in title_n for token in NTOK):
        return False
    return parent_artist(artist) or any(token and token in artist_n for token in KNOWN_REMIXERS)


def bucket(artist: str, title: str, source: str) -> str | None:
    if is_explicit_touhou_source(source):
        return "explicit_source"
    if official_exactish(artist, title):
        return "official_exactish"
    if base_exact(title) and parent_artist(artist):
        return "base_parent_exact"
    return None


report = load_status_report(STATUS_LOG)
rows = report["missing"]
selected = {
    int(row["beatmapset_id"]): bucket(row["artist"], row["title"], row.get("source", ""))
    for row in rows
}
selected = {beatmapset_id: kind for beatmapset_id, kind in selected.items() if kind}
assert len(selected) == 284, {
    kind: list(selected.values()).count(kind) for kind in set(selected.values())
}

catalog_path = Path("data/catalog.json")
catalog = Catalog.load(catalog_path)
pending = [beatmapset_id for beatmapset_id in sorted(selected) if beatmapset_id not in catalog.entries]
if not pending:
    print("NIGHT_APPLY_ALREADY_COMPLETE")
    raise SystemExit(0)

api = OsuApi.from_env()
api.token()


def fetch(beatmapset_id: int) -> tuple[int, str, dict]:
    raw = api.beatmapset(beatmapset_id)
    assert int(raw["id"]) == beatmapset_id
    fresh_bucket = bucket(raw.get("artist", ""), raw.get("title", ""), raw.get("source", ""))
    if fresh_bucket is None:
        raise AssertionError(
            (
                beatmapset_id,
                "no-longer-qualified",
                raw.get("artist"),
                raw.get("title"),
                raw.get("source"),
            )
        )
    return beatmapset_id, fresh_bucket, raw


with ThreadPoolExecutor(max_workers=8) as pool:
    fetched = list(pool.map(fetch, pending))

counts = {"explicit_source": 0, "official_exactish": 0, "base_parent_exact": 0}
ids_by = {key: [] for key in counts}
for beatmapset_id, kind, raw in fetched:
    incoming = entry_from_osu(
        raw,
        evidence=["audit:night-of-knights-2026-08"],
        confidence="candidate",
    )
    if kind != "explicit_source":
        incoming.evidence.extend(["manual:verified", "composition:cool-create:night-of-knights"])
        incoming.touhou_kind = "arrangement"
        incoming = apply_classification(incoming, tags=raw.get("tags", ""))
    assert incoming.confidence == "verified", (
        beatmapset_id,
        kind,
        incoming.confidence,
        incoming.source,
    )
    _, changed = catalog.merge(incoming)
    assert changed, (beatmapset_id, "expected-new-entry")
    counts[kind] += 1
    ids_by[kind].append(beatmapset_id)

assert sum(counts.values()) == len(fetched)
catalog.save(catalog_path)

doc_path = Path("docs/source-audit-2026-08-night-of-knights.md")
doc = doc_path.read_text(encoding="utf-8")
start = "<!-- NIGHT_IMPLEMENTATION_START -->"
end = "<!-- NIGHT_IMPLEMENTATION_END -->"
block = f'''{start}

## Status-scoped exhaustive title-family pass

The default osu! beatmapset search ranking hides a large amount of old graveyard material, so the audit also enumerated six explicit status buckets (`graveyard`, `ranked`, `loved`, `qualified`, `pending`, `wip`) for seven controlled title queries. The completed pass covered **42 query/status pairs**, saw **7,159 distinct search results**, and direct-refetched **448 title-family matches**. At the pre-change catalog boundary those were **440 absent**, **1 existing candidate**, and **7 already verified**.

The 440 absent sets were then split by fail-closed evidence rules. This first implementation wave accepts **284 newly verified beatmapsets** only:

- **{counts['explicit_source']}** have a fresh current osu! `source` that independently satisfies the repository's exact Touhou/game-source classifier. These do not receive a manual override.
- **{counts['official_exactish']}** match a distinctive remix/variant from COOL&CREATE's first-party 2018/2019/2025 `オールナイト・オブ・ナイツ` corpus and an appropriate parent/remixer artist guard. These receive sticky `manual:verified` evidence tied to this audit.
- **{counts['base_parent_exact']}** use an exact controlled base title (`ナイト・オブ・ナイツ` / `Night of Nights` / `Night of Knights` / `Knight of Nights`) with beatMARIO or COOL&CREATE as artist. These receive sticky `manual:verified` evidence backed by the primary COOL&CREATE provenance above.

Every one of the {len(fetched)} applied sets was re-fetched directly from `/api/v2/beatmapsets/{{id}}` immediately before writing and had to satisfy the same rule again on fresh metadata. Search snapshots alone were never accepted.

The remaining **156 absent title-family hits are deliberately held for manual composition-chain review**. That bucket contains genuine-looking covers and mashups (for example RichaadEB and Para Dot variants) mixed with weakly attributed uploads, memes, BMS/game-source labels, and obvious token collisions. They are not promoted merely to maximize count.

Applied IDs by rule (for reproducibility):

<details><summary>explicit current Touhou/game source ({counts['explicit_source']})</summary>

`{','.join(map(str, ids_by['explicit_source']))}`

</details>

<details><summary>first-party exact/distinctive derivative ({counts['official_exactish']})</summary>

`{','.join(map(str, ids_by['official_exactish']))}`

</details>

<details><summary>beatMARIO / COOL&CREATE exact base title ({counts['base_parent_exact']})</summary>

`{','.join(map(str, ids_by['base_parent_exact']))}`

</details>

{end}'''
if start in doc:
    doc = doc[: doc.index(start)] + block + doc[doc.index(end) + len(end) :]
else:
    doc = doc.rstrip() + "\n\n" + block + "\n"
doc_path.write_text(doc, encoding="utf-8")

print("NIGHT_APPLY_OK", len(fetched), counts)
