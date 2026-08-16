from __future__ import annotations

import json
from pathlib import Path

from touhou_osu.sources import import_all, import_official_pack

PROPOSALS = [
    {"tag": "A2", "name": "Gojou Kai - Secret Seven", "raw": 7, "ids": [3573, 3847, 3862, 3875, 4077, 4134]},
    {"tag": "FQ70", "name": "BLANKFIELD high tempo mini-pack", "raw": 4, "ids": [1171995, 1175382, 1185325, 1201974]},
    {"tag": "FQ66", "name": "A-One Pack", "raw": 6, "ids": [1474048, 1480185, 1499636, 1543564, 1633053, 1644488]},
    {"tag": "FQ40", "name": "LeaF mini-pack", "raw": 3, "ids": [1128939]},
    {"tag": "R341", "name": "Beatmap Spotlights: Winter 2026 (osu!catch)", "raw": 27, "ids": [1980463, 2020128]},
    {"tag": "R340", "name": "Beatmap Spotlights: Winter 2026 (osu!taiko)", "raw": 27, "ids": [2159203]},
    {"tag": "R339", "name": "Beatmap Spotlights: Winter 2026 (osu!)", "raw": 27, "ids": [304022, 462878, 1924253]},
    {"tag": "R338", "name": "Beatmap Spotlights: Summer 2025 (osu!mania)", "raw": 27, "ids": [2288990]},
    {"tag": "R337", "name": "Beatmap Spotlights: Summer 2025 (osu!catch)", "raw": 27, "ids": [1220848, 1531490, 2221973, 2281583]},
    {"tag": "R336", "name": "Beatmap Spotlights: Summer 2025 (osu!taiko)", "raw": 27, "ids": [2049581]},
    {"tag": "R335", "name": "Beatmap Spotlights: Summer 2025 (osu!)", "raw": 27, "ids": [2282492]},
    {"tag": "R334", "name": "Beatmap Spotlights: Spring 2025 (osu!mania)", "raw": 27, "ids": [2141740]},
    {"tag": "R333", "name": "Beatmap Spotlights: Spring 2025 (osu!catch)", "raw": 27, "ids": [2000358, 2019552, 2151953]},
    {"tag": "R332", "name": "Beatmap Spotlights: Spring 2025 (osu!taiko)", "raw": 27, "ids": [1919687, 2220709]},
    {"tag": "R331", "name": "Beatmap Spotlights: Spring 2025 (osu!)", "raw": 27, "ids": [1842664, 1942555, 2239541]},
    {"tag": "R328", "name": "Beatmap Spotlights: Autumn 2023 (osu!taiko)", "raw": 26, "ids": [1590156]},
    {"tag": "R327", "name": "Beatmap Spotlights: Autumn 2023 (osu!)", "raw": 27, "ids": [1381715]},
    {"tag": "R326", "name": "Beatmap Spotlights: Spring 2023 (osu!mania)", "raw": 27, "ids": [572338]},
    {"tag": "R325", "name": "Beatmap Spotlights: Spring 2023 (osu!catch)", "raw": 27, "ids": [253969, 307818, 1872426]},
    {"tag": "R324", "name": "Beatmap Spotlights: Spring 2023 (osu!taiko)", "raw": 27, "ids": [96103]},
    {"tag": "R323", "name": "Beatmap Spotlights: Spring 2023 (osu!)", "raw": 27, "ids": [29044, 41974, 1638844, 1898383]},
    {"tag": "R322", "name": "Beatmap Spotlights: Winter 2023 (osu!mania)", "raw": 21, "ids": [1324800, 1670404]},
    {"tag": "R319", "name": "Beatmap Spotlights: Winter 2023 (osu!)", "raw": 27, "ids": [1024028, 1575475]},
    {"tag": "R318", "name": "Beatmap Spotlights: Summer 2022 (osu!mania)", "raw": 27, "ids": [166146]},
    {"tag": "R317", "name": "Beatmap Spotlights: Summer 2022 (osu!catch)", "raw": 27, "ids": [114741, 1110955]},
    {"tag": "R316", "name": "Beatmap Spotlights: Summer 2022 (osu!taiko)", "raw": 27, "ids": [1155202, 1630732, 1762719]},
    {"tag": "R315", "name": "Beatmap Spotlights: Summer 2022 (osu!)", "raw": 27, "ids": [1742131, 1774999]},
    {"tag": "R314", "name": "Beatmap Spotlights: Spring 2022 (osu!mania)", "raw": 27, "ids": [400078, 1656541]},
    {"tag": "R312", "name": "Beatmap Spotlights: Spring 2022 (osu!taiko)", "raw": 26, "ids": [452051, 1506936, 1526077]},
    {"tag": "R311", "name": "Beatmap Spotlights: Spring 2022 (osu!)", "raw": 27, "ids": [795140, 1004248, 1670776]},
    {"tag": "R309", "name": "Beatmap Spotlights: Winter 2022 (osu!catch)", "raw": 27, "ids": [1023485, 1480185, 1644488]},
    {"tag": "R308", "name": "Beatmap Spotlights: Winter 2022 (osu!taiko)", "raw": 27, "ids": [1013884, 1263550]},
    {"tag": "R305", "name": "Beatmap Spotlights: Spring 2021 (osu!catch)", "raw": 20, "ids": [633255]},
    {"tag": "R304", "name": "Beatmap Spotlights: Spring 2021 (osu!taiko)", "raw": 20, "ids": [405516]},
    {"tag": "R303", "name": "Beatmap Spotlights: Spring 2021 (osu!)", "raw": 20, "ids": [198034, 1132649]},
    {"tag": "R301", "name": "Beatmap Spotlights: Winter 2021 (osu!catch)", "raw": 20, "ids": [204927]},
    {"tag": "R300", "name": "Beatmap Spotlights: Winter 2021 (osu!taiko)", "raw": 20, "ids": [96103, 812992]},
    {"tag": "R297", "name": "Beatmap Spotlights: Autumn 2020 (osu!catch)", "raw": 19, "ids": [972764]},
    {"tag": "R296", "name": "Beatmap Spotlights: Autumn 2020 (osu!taiko)", "raw": 20, "ids": [812992]},
    {"tag": "R293", "name": "Beatmap Spotlights: Summer 2020 (osu!catch)", "raw": 20, "ids": [48874, 204927, 998578, 1023485]},
    {"tag": "R291", "name": "Beatmap Spotlights: Summer 2020 (osu!)", "raw": 20, "ids": [37292, 145976]},
    {"tag": "R288", "name": "Seasonal Spotlights: Winter 2020 (osu!taiko)", "raw": 4, "ids": [1013884]},
]

config = json.loads(Path("config/seeds.json").read_text(encoding="utf-8"))
baseline_entries, baseline_reports = import_all(config, workers=4)
baseline_ids = {entry.beatmapset_id for entry in baseline_entries}
catalog = json.loads(Path("data/catalog.json").read_text(encoding="utf-8"))
by_id = {int(item["beatmapset_id"]): item for item in catalog["entries"]}

all_ids: set[int] = set()
total_records = 0
rows = []
for item in PROPOSALS:
    source = {
        "tag": item["tag"],
        "name": item["name"],
        "verified_ids": item["ids"],
        "minimum_source_entries": item["raw"],
        "minimum_entries": len(item["ids"]),
    }
    entries = import_official_pack(source)
    ids = [entry.beatmapset_id for entry in entries]
    if ids != item["ids"]:
        raise SystemExit(f"{item['tag']} live output drift: {ids} != {item['ids']}")
    total_records += len(ids)
    all_ids.update(ids)
    rows.append({
        "tag": item["tag"],
        "raw": item["raw"],
        "verified": len(ids),
        "novel_source_ids": [i for i in ids if i not in baseline_ids],
        "catalog_missing_ids": [i for i in ids if i not in by_id],
        "catalog_candidate_ids": [i for i in ids if by_id.get(i, {}).get("confidence") in {"candidate", "probable"}],
        "catalog_verified_ids": [i for i in ids if by_id.get(i, {}).get("confidence") == "verified"],
    })

result = {
    "baseline_source_records": len(baseline_entries),
    "baseline_source_count": len(baseline_reports),
    "baseline_unique_beatmapsets": len(baseline_ids),
    "proposal_source_count": len(PROPOSALS),
    "proposal_records": total_records,
    "proposal_unique_ids": len(all_ids),
    "novel_source_ids": sorted(all_ids - baseline_ids),
    "catalog_missing_ids": sorted(i for i in all_ids if i not in by_id),
    "catalog_candidate_ids": sorted(i for i in all_ids if by_id.get(i, {}).get("confidence") in {"candidate", "probable"}),
    "catalog_verified_ids": sorted(i for i in all_ids if by_id.get(i, {}).get("confidence") == "verified"),
    "packs": rows,
}
Path("wave3-proposal-audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))
