#!/usr/bin/env python3
"""Generate the README catalog statistics card from the canonical catalog."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "data" / "catalog.json"
OUTPUT_PATH = ROOT / "assets" / "catalog-stats.svg"


def fmt(value: int) -> str:
    return f"{value:,}"


def load_stats() -> dict[str, int]:
    raw = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    entries = raw.get("entries")
    if not isinstance(entries, list):
        raise ValueError("catalog entries must be a list")

    counts = Counter(entry.get("confidence") for entry in entries)
    verified = counts["verified"]
    probable = counts["probable"]

    return {
        "accepted": verified + probable,
        "verified": verified,
        "probable": probable,
        "candidate": counts["candidate"],
        "excluded": counts["excluded"],
        "total": len(entries),
    }


def render_svg(stats: dict[str, int]) -> str:
    accepted = stats["accepted"]
    verified = stats["verified"]
    verified_ratio = (verified / accepted * 100) if accepted else 0

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="760" height="150" viewBox="0 0 760 150" role="img" aria-labelledby="title desc">
  <title id="title">Touhou osu! Index catalog statistics</title>
  <desc id="desc">{fmt(accepted)} accepted beatmapsets, {fmt(verified)} verified, {fmt(stats["probable"])} probable, {fmt(stats["candidate"])} candidates, {fmt(stats["excluded"])} excluded.</desc>
  <style>
    text {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; }}
    .heading {{ fill: #f0f6fc; font-size: 15px; font-weight: 700; }}
    .eyebrow {{ fill: #8b949e; font-size: 10px; font-weight: 700; letter-spacing: 1.2px; }}
    .label {{ fill: #8b949e; font-size: 11px; font-weight: 600; }}
    .value {{ fill: #f0f6fc; font-size: 30px; font-weight: 700; }}
    .meta {{ fill: #8b949e; font-size: 11px; }}
    .accent {{ fill: #ff66aa; }}
  </style>
  <rect width="760" height="150" rx="14" fill="#0d1117"/>
  <rect x="0.5" y="0.5" width="759" height="149" rx="13.5" fill="none" stroke="#30363d"/>
  <rect x="0" y="0" width="5" height="150" rx="2.5" class="accent"/>

  <text x="28" y="29" class="eyebrow">CATALOG STATUS</text>
  <text x="28" y="49" class="heading">Touhou osu! Index</text>

  <line x1="226" y1="22" x2="226" y2="116" stroke="#21262d"/>
  <line x1="480" y1="22" x2="480" y2="116" stroke="#21262d"/>

  <text x="258" y="43" class="label">ACCEPTED BEATMAPSETS</text>
  <text x="258" y="78" class="value">{fmt(accepted)}</text>
  <text x="258" y="99" class="meta">verified + probable</text>

  <text x="512" y="43" class="label">VERIFIED BEATMAPSETS</text>
  <text x="512" y="78" class="value">{fmt(verified)}</text>
  <text x="512" y="99" class="meta">{verified_ratio:.1f}% of accepted</text>

  <line x1="28" y1="116" x2="732" y2="116" stroke="#21262d"/>
  <text x="28" y="137" class="meta">{fmt(stats["probable"])} probable  ·  {fmt(stats["candidate"])} in review queue  ·  {fmt(stats["excluded"])} excluded  ·  {fmt(stats["total"])} total tracked</text>
</svg>
'''


def main() -> None:
    stats = load_stats()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(render_svg(stats), encoding="utf-8")
    print(
        "Generated catalog stats: "
        f"accepted={stats['accepted']} verified={stats['verified']} total={stats['total']}"
    )


if __name__ == "__main__":
    main()
