from __future__ import annotations

import json
import subprocess
from pathlib import Path

path = Path("config/seeds.json")
current = json.loads(path.read_text(encoding="utf-8"))
audited = [source for source in current["official_packs"] if "verified_ids" in source]
if len(audited) != 9:
    raise SystemExit(f"expected 9 audited artist packs, found {len(audited)}")

base = subprocess.check_output(
    ["git", "show", "origin/main:config/seeds.json"],
    text=True,
    encoding="utf-8",
)
anchor = '    {"tag": "FQ35", "name": "UNDEAD CORPORATION Touhou pack", "minimum_entries": 8}\n'
if base.count(anchor) != 1:
    raise SystemExit("main official-pack anchor changed")

blocks = []
for index, source in enumerate(audited):
    ids = ", ".join(str(int(value)) for value in source["verified_ids"])
    comma = "," if index < len(audited) - 1 else ""
    blocks.append(
        "\n".join(
            [
                "    {",
                f'      "tag": {json.dumps(source["tag"])},',
                f'      "name": {json.dumps(source["name"])},',
                f'      "verified_ids": [{ids}],',
                f'      "minimum_source_entries": {int(source["minimum_source_entries"])},',
                f'      "minimum_entries": {int(source["minimum_entries"])}',
                f"    }}{comma}",
            ]
        )
    )
replacement = anchor.rstrip("\n") + ",\n" + "\n".join(blocks) + "\n"
path.write_text(base.replace(anchor, replacement), encoding="utf-8")

reloaded = json.loads(path.read_text(encoding="utf-8"))
reloaded_audited = [source for source in reloaded["official_packs"] if "verified_ids" in source]
if reloaded_audited != audited:
    raise SystemExit("config cleanup changed audited pack semantics")
