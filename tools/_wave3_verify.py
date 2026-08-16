from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

from touhou_osu.sources import import_official_pack_batch

NOVEL_IDS = {
    4134, 253969, 307818, 400078, 452051, 572338, 812992, 972764, 998578,
    1013884, 1023485, 1110955, 1128939, 1155202, 1220848, 1263550, 1324800,
    1474048, 1480185, 1499636, 1506936, 1526077, 1531490, 1543564, 1590156,
    1630732, 1633053, 1644488, 1656541, 1670404, 1762719, 1872426, 1919687,
    1924253, 1942555, 1980463, 2000358, 2019552, 2020128, 2049581, 2141740,
    2151953, 2159203, 2220709, 2221973, 2281583, 2288990,
}
PROMOTION_IDS = {
    29044, 37292, 41974, 48874, 114741, 145976, 166146, 198034, 204927,
    304022, 405516, 633255, 1004248, 1132649, 1171995, 1201974, 1381715,
    1575475, 1742131, 1774999, 1898383,
}


def load_proposals() -> list[dict]:
    tree = ast.parse(Path("tools/_wave3_proposal_audit.py").read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "PROPOSALS" for target in node.targets
        ):
            return ast.literal_eval(node.value)
    raise SystemExit("PROPOSALS assignment not found")


def expected_evidence(proposals: list[dict]) -> dict[int, set[str]]:
    expected: dict[int, set[str]] = {}
    for pack in proposals:
        for beatmapset_id in pack["ids"]:
            expected.setdefault(int(beatmapset_id), set()).add(f"official_pack_item:{pack['tag']}")
    return expected


def verify_live() -> None:
    config = json.loads(Path("config/seeds.json").read_text(encoding="utf-8"))
    batches = config.get("official_pack_batches", [])
    if len(batches) != 1:
        raise SystemExit(f"expected exactly one official_pack_batches source, got {len(batches)}")
    source = batches[0]
    if source.get("id") != "official-pack-wave3":
        raise SystemExit(f"unexpected batch id: {source.get('id')}")

    proposals = load_proposals()
    expected = expected_evidence(proposals)
    entries = import_official_pack_batch(source)
    if len(entries) != 84:
        raise SystemExit(f"live batch returned {len(entries)} unique entries; expected 84")
    by_id = {entry.beatmapset_id: entry for entry in entries}
    if set(by_id) != set(expected):
        raise SystemExit(
            f"live batch ID drift: missing={sorted(set(expected)-set(by_id))} "
            f"extra={sorted(set(by_id)-set(expected))}"
        )
    for beatmapset_id, evidence in expected.items():
        if set(by_id[beatmapset_id].evidence) != evidence:
            raise SystemExit(
                f"{beatmapset_id} evidence drift: {by_id[beatmapset_id].evidence} != {sorted(evidence)}"
            )
        if by_id[beatmapset_id].confidence != "verified":
            raise SystemExit(f"{beatmapset_id} is not verified")
    print("Live wave3 batch: 42 canonical packs, 91 memberships, 84 unique verified IDs")


def verify_post_import() -> None:
    catalog = json.loads(Path("data/catalog.json").read_text(encoding="utf-8"))
    by_id = {int(item["beatmapset_id"]): item for item in catalog["entries"]}

    for beatmapset_id in NOVEL_IDS | PROMOTION_IDS:
        item = by_id.get(beatmapset_id)
        if item is None:
            raise SystemExit(f"expected imported beatmapset {beatmapset_id} is missing")
        if item.get("confidence") != "verified":
            raise SystemExit(f"beatmapset {beatmapset_id} did not become verified: {item.get('confidence')}")
        if not any(ev.startswith("official_pack_item:") for ev in item.get("evidence", [])):
            raise SystemExit(f"beatmapset {beatmapset_id} lacks official pack item evidence")

    false_source = by_id.get(4135)
    if false_source is None or false_source.get("confidence") != "excluded":
        raise SystemExit("4135 I Will did not remain excluded")
    if "manual:excluded" not in false_source.get("evidence", []):
        raise SystemExit("4135 lacks manual:excluded")
    if any(ev == "official_pack_item:A2" for ev in false_source.get("evidence", [])):
        raise SystemExit("4135 incorrectly received A2 audited evidence")

    prior_false_positive = by_id.get(605290)
    if prior_false_positive is None or prior_false_positive.get("confidence") != "excluded":
        raise SystemExit("605290 previous false-positive exclusion regressed")

    seihou = by_id.get(495283)
    if seihou is None or seihou.get("confidence") != "candidate":
        raise SystemExit(f"495283 Seihou boundary regressed: {None if seihou is None else seihou.get('confidence')}")

    for withheld in (1058394, 1125217):
        item = by_id.get(withheld)
        if item and any(ev == "official_pack_item:FQ40" for ev in item.get("evidence", [])):
            raise SystemExit(f"withheld FQ40 beatmapset {withheld} incorrectly received audited evidence")

    print(
        "Full source merge preserved 4135/605290 exclusions and 495283 Seihou boundary; "
        f"verified {len(NOVEL_IDS)} novel IDs and {len(PROMOTION_IDS)} promotions"
    )


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in {"live", "post-import"}:
        raise SystemExit("usage: _wave3_verify.py live|post-import")
    if sys.argv[1] == "live":
        verify_live()
    else:
        verify_post_import()


if __name__ == "__main__":
    main()
