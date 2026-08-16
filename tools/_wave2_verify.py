from __future__ import annotations

import json
import sys
from pathlib import Path

from touhou_osu.sources import import_official_pack

WITHHELD = {
    154056,
    206284,
    223048,
    234999,
    242360,
    247319,
    250337,
    288997,
    320155,
    347460,
    349810,
    352351,
    491057,
    495283,
    562169,
    605290,
    1463878,
    1621390,
}


def verify_live() -> None:
    config = json.loads(Path("config/seeds.json").read_text(encoding="utf-8"))
    audited = [source for source in config["official_packs"] if "verified_ids" in source]
    if len(audited) != 9:
        raise SystemExit(f"expected 9 audited artist packs, found {len(audited)}")

    emitted: set[int] = set()
    for source in audited:
        entries = import_official_pack(source)
        actual = [entry.beatmapset_id for entry in entries]
        expected = [int(value) for value in source["verified_ids"]]
        if actual != expected:
            raise SystemExit(f"{source['tag']} emitted IDs differ from its audited allowlist")
        expected_evidence = [f"official_pack_item:{source['tag']}"]
        if any(entry.evidence != expected_evidence for entry in entries):
            raise SystemExit(f"{source['tag']} emitted unexpected evidence")
        if any(entry.confidence != "verified" for entry in entries):
            raise SystemExit(f"{source['tag']} emitted non-verified audited entries")
        overlap = emitted & set(actual)
        if overlap:
            raise SystemExit(f"duplicate audited IDs across packs: {sorted(overlap)}")
        emitted.update(actual)
        print(f"{source['tag']}: {len(actual)} audited Touhou beatmapsets")

    if len(emitted) != 170:
        raise SystemExit(f"expected 170 unique audited IDs, got {len(emitted)}")
    leaked = emitted & WITHHELD
    if leaked:
        raise SystemExit(f"withheld IDs leaked into trusted evidence: {sorted(leaked)}")
    print("Audited artist packs: 170 unique verified IDs; 18 reviewed exclusions withheld")


def verify_post_import() -> None:
    catalog = json.loads(Path("data/catalog.json").read_text(encoding="utf-8"))
    by_id = {int(item["beatmapset_id"]): item for item in catalog["entries"]}

    false_positive = by_id[605290]
    if false_positive["confidence"] != "excluded":
        raise SystemExit("605290 lost excluded confidence after import-seeds")
    if "manual:excluded" not in false_positive["evidence"]:
        raise SystemExit("605290 lost manual:excluded after import-seeds")
    if "tournament:1432" not in false_positive["evidence"]:
        raise SystemExit("605290 lost historical tournament provenance")

    seihou = by_id[495283]
    if seihou["confidence"] not in {"candidate", "excluded"}:
        raise SystemExit(f"495283 was incorrectly promoted from the Seihou boundary: {seihou['confidence']}")
    if any(evidence.startswith("official_pack_item:") for evidence in seihou["evidence"]):
        raise SystemExit("495283 received audited Touhou pack evidence despite being withheld")

    for beatmapset_id in WITHHELD - {495283, 605290}:
        item = by_id.get(beatmapset_id)
        if item and any(evidence.startswith("official_pack_item:") for evidence in item["evidence"]):
            raise SystemExit(f"withheld {beatmapset_id} received audited pack evidence")

    print("Sticky exclusion and withheld-item boundaries survived the full source merge")


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in {"live", "post-import"}:
        raise SystemExit("usage: _wave2_verify.py {live|post-import}")
    if sys.argv[1] == "live":
        verify_live()
    else:
        verify_post_import()


if __name__ == "__main__":
    main()
