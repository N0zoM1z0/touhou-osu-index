from __future__ import annotations

import json
from pathlib import Path


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if text.count(old) != 1:
        raise SystemExit(f"{path}: expected one target, got {text.count(old)}")
    path.write_text(text.replace(old, new), encoding="utf-8")


# A manually reviewed candidate is a real policy state: it means the item is
# intentionally kept reviewable/out of the accepted index even if a broad
# automated source (for example a Touhou-only tournament) later reappears.
replace_once(
    Path("touhou_osu/classifier.py"),
    '''    if "manual:verified" in evidence:
        return Classification("verified", tuple(sorted(evidence)))

    if any(
''',
    '''    if "manual:verified" in evidence:
        return Classification("verified", tuple(sorted(evidence)))
    if "manual:candidate" in evidence:
        return Classification("candidate", tuple(sorted(evidence)))

    if any(
''',
)

replace_once(
    Path("touhou_osu/catalog.py"),
    '''        if "manual:excluded" in manual:
            current.confidence = "excluded"
        elif "manual:verified" in manual:
            current.confidence = "verified"
        elif CONFIDENCE_RANK[incoming.confidence] > CONFIDENCE_RANK[current.confidence]:
''',
    '''        if "manual:excluded" in manual:
            current.confidence = "excluded"
        elif "manual:verified" in manual:
            current.confidence = "verified"
        elif "manual:candidate" in manual:
            current.confidence = "candidate"
        elif CONFIDENCE_RANK[incoming.confidence] > CONFIDENCE_RANK[current.confidence]:
''',
)

# Freeze the already-reviewed Seihou boundary so the trusted Gensokyo Cup 2
# membership cannot silently promote it on every source refresh.
path = Path("data/catalog.json")
catalog = json.loads(path.read_text(encoding="utf-8"))
by_id = {int(item["beatmapset_id"]): item for item in catalog["entries"]}
item = by_id[495283]
if item.get("confidence") != "candidate":
    raise SystemExit(f"495283 baseline changed before sticky candidate patch: {item.get('confidence')}")
item["evidence"] = sorted(set(item.get("evidence", [])) | {"manual:candidate"}, key=str.casefold)
item["confidence"] = "candidate"
path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Catalog-level regression: incoming verified evidence must not beat a reviewed
# candidate boundary.
path = Path("tests/test_catalog.py")
text = path.read_text(encoding="utf-8")
marker = "    def test_evidence_is_required(self):\n"
test = '''    def test_manual_candidate_is_sticky(self):\n        catalog = Catalog([entry(evidence=["manual:candidate"], confidence="candidate")])\n        merged, _ = catalog.merge(entry(evidence=["tournament:google_sheet:fixture"], confidence="verified"))\n        self.assertEqual(merged.confidence, "candidate")\n        self.assertIn("manual:candidate", merged.evidence)\n        self.assertIn("tournament:google_sheet:fixture", merged.evidence)\n\n'''
if text.count(marker) != 1:
    raise SystemExit("test_catalog insertion marker changed")
path.write_text(text.replace(marker, test + marker), encoding="utf-8")

# Classifier-level regression covers reconcile/hydrate paths that rebuild an
# Entry from public metadata before the Catalog merge happens.
path = Path("tests/test_classifier.py")
text = path.read_text(encoding="utf-8")
marker = "    def test_known_artist_alone_stays_candidate(self):\n"
test = '''    def test_manual_candidate_beats_trusted_tournament(self):\n        item = Entry(1, evidence=["manual:candidate", "tournament:google_sheet:fixture"], confidence="verified")\n        apply_classification(item)\n        self.assertEqual(item.confidence, "candidate")\n\n'''
if text.count(marker) != 1:
    raise SystemExit("test_classifier manual-candidate marker changed")
path.write_text(text.replace(marker, test + marker), encoding="utf-8")

replace_once(
    Path("CONTRIBUTING.md"),
    "Manual evidence is sticky: automated refreshes update osu! metadata but do not override a manual inclusion or exclusion.\n",
    "Manual evidence is sticky: automated refreshes update osu! metadata but do not override `manual:verified`, `manual:excluded`, or a reviewed `manual:candidate` boundary. Use `manual:candidate` when an item is relevant enough to retain for review but repository scope intentionally prevents automatic acceptance (for example a ZUN-composed Seihou track).\n",
)

# Record why this new state is needed in the wave audit itself.
path = Path("docs/source-audit-2026-08-official-packs-wave3.md")
text = path.read_text(encoding="utf-8")
marker = "## Reproduction\n"
addition = '''## Sticky Seihou boundary discovered during full merge\n\nThe complete seed-merge simulation exposed a pre-existing interaction that a\npack-only test would miss: beatmapset `495283` (`Zouka de Arou to Shita Mono`)\nwas correctly stored as a Seihou candidate in the canonical catalog, but the\ntrusted Gensokyo Cup 2 membership (`tournament:google_sheet:gensokyo-cup-2`)\npromoted it back to verified during every full source refresh. The track is an\narrangement of `二色蓮花蝶 ～ Ancients` from Seihou / Shuusou Gyoku, so the\nrepository's existing Seihou rule says it must remain candidate.\n\nThis wave therefore adds a narrow `manual:candidate` sticky override. It keeps\nall discovery/tournament provenance, remains reviewable, and outranks automatic\npack/tournament promotion without mislabeling the track as unrelated. Both the\nclassifier and catalog merge path have regression tests for this state.\n\n'''
if text.count(marker) != 1:
    raise SystemExit("wave3 audit reproduction marker changed")
path.write_text(text.replace(marker, addition + marker), encoding="utf-8")
