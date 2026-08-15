"""Generate machine-readable exports and the static browser."""

from __future__ import annotations

import csv
import json
import shutil
from collections import Counter
from datetime import date
from pathlib import Path

from .catalog import Catalog

ROOT = Path(__file__).resolve().parents[1]
WEBSITE = ROOT / "website"


def statistics(catalog: Catalog) -> dict:
    entries = list(catalog.entries.values())
    return {
        "total": len(entries),
        "accepted": sum(entry.confidence in ("verified", "probable") for entry in entries),
        "confidence": dict(sorted(Counter(entry.confidence for entry in entries).items())),
        "modes": dict(sorted(Counter(mode for entry in entries for mode in entry.modes).items())),
        "status": dict(sorted(Counter(entry.status for entry in entries).items())),
        "last_built": date.today().isoformat(),
    }


def _write_csv(path: Path, records: list[dict]) -> None:
    fields = [
        "beatmapset_id",
        "artist",
        "title",
        "creator",
        "source",
        "status",
        "modes",
        "touhou_kind",
        "origin_games",
        "original_themes",
        "evidence",
        "confidence",
        "last_checked",
        "osu_last_updated",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fields)
        writer.writeheader()
        for record in records:
            row = record.copy()
            for key in ("modes", "origin_games", "original_themes", "evidence"):
                row[key] = "|".join(row[key])
            writer.writerow(row)


def build(catalog: Catalog, output: Path) -> dict:
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    accepted = [
        catalog.entries[key].to_dict()
        for key in sorted(catalog.entries)
        if catalog.entries[key].confidence in ("verified", "probable")
    ]
    review = [
        catalog.entries[key].to_dict()
        for key in sorted(catalog.entries)
        if catalog.entries[key].confidence in ("candidate", "excluded")
    ]
    stats = statistics(catalog)
    (output / "catalog.json").write_text(
        json.dumps({"schema_version": 1, "entries": accepted}, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    (output / "review.json").write_text(
        json.dumps({"schema_version": 1, "entries": review}, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    (output / "stats.json").write_text(json.dumps(stats, indent=2) + "\n", encoding="utf-8")
    _write_csv(output / "catalog.csv", accepted)

    page = (WEBSITE / "index.html").read_text(encoding="utf-8")
    page = page.replace("{{ACCEPTED_COUNT}}", str(stats["accepted"]))
    page = page.replace("{{TOTAL_COUNT}}", str(stats["total"]))
    page = page.replace("{{LAST_BUILT}}", stats["last_built"])
    (output / "index.html").write_text(page, encoding="utf-8")
    shutil.copytree(WEBSITE / "static", output / "assets")
    return stats
