"""Base-aware structural, provenance, and live osu! review for catalog changes."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

from .catalog import Catalog
from .http import get_text
from .osu_api import OsuApi, entry_from_osu
from .provenance import _report_payload, audit_entries, new_generic_verification_violations
from .sources import parse_beatmapset_page

IDENTITY_FIELDS = (
    "beatmapset_id",
    "artist",
    "title",
    "creator",
    "source",
    "status",
    "osu_last_updated",
)
AUDIT_ROW_RE = re.compile(r"^\|\s*(\d+)\s*\|")


class AuditError(RuntimeError):
    pass


@dataclass(frozen=True)
class RevisionContext:
    head: str
    base_tip: str
    merge_base: str

    @property
    def base_is_ancestor(self) -> bool:
        return self.base_tip == self.merge_base


def _git(repository: Path, *args: str, text: bool = True):
    try:
        return subprocess.check_output(
            ["git", "-C", str(repository), *args],
            text=text,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as exc:
        detail = exc.stderr.strip() if isinstance(exc.stderr, str) else ""
        raise AuditError(f"git {' '.join(args)} failed: {detail or exc}") from exc


def revision_context(repository: Path, base_ref: str) -> RevisionContext:
    repository = repository.resolve()
    head = _git(repository, "rev-parse", "HEAD").strip()
    base_tip = _git(repository, "rev-parse", "--verify", f"{base_ref}^{{commit}}").strip()
    merge_base = _git(repository, "merge-base", head, base_tip).strip()
    return RevisionContext(head=head, base_tip=base_tip, merge_base=merge_base)


def _catalog_relative_path(repository: Path, catalog_path: Path) -> Path:
    absolute = catalog_path.resolve() if catalog_path.is_absolute() else (repository / catalog_path).resolve()
    try:
        return absolute.relative_to(repository.resolve())
    except ValueError as exc:
        raise AuditError("catalog must be inside the Git repository") from exc


def load_catalog_at(repository: Path, revision: str, catalog_path: Path) -> Catalog:
    """Materialize one catalog directory from Git without checking it out."""

    relative = _catalog_relative_path(repository, catalog_path)
    paths = [
        line
        for line in _git(
            repository,
            "ls-tree",
            "-r",
            "--name-only",
            revision,
            "--",
            relative.as_posix(),
        ).splitlines()
        if line.endswith(".json")
    ]
    if not paths:
        raise AuditError(f"no catalog JSON files found at {revision}:{relative}")

    with tempfile.TemporaryDirectory(prefix="touhou-osu-audit-") as directory:
        root = Path(directory)
        for path_text in paths:
            target = root / path_text
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(_git(repository, "show", f"{revision}:{path_text}", text=False))
        return Catalog.load(root / relative)


def catalog_diff(base: Catalog, current: Catalog) -> dict:
    base_ids = set(base.entries)
    current_ids = set(current.entries)
    added = sorted(current_ids - base_ids)
    removed = sorted(base_ids - current_ids)
    changed_fields: dict[str, list[str]] = {}
    for beatmapset_id in sorted(base_ids & current_ids):
        before = base.entries[beatmapset_id].to_dict()
        after = current.entries[beatmapset_id].to_dict()
        fields = sorted(field for field in set(before) | set(after) if before.get(field) != after.get(field))
        if fields:
            changed_fields[str(beatmapset_id)] = fields
    return {
        "base_entries": len(base.entries),
        "current_entries": len(current.entries),
        "added": added,
        "removed": removed,
        "modified": [int(item) for item in changed_fields],
        "changed_fields": changed_fields,
    }


def accepted_ids_from_audit_document(path: Path) -> list[int]:
    lines = path.read_text(encoding="utf-8").splitlines()
    try:
        start = lines.index("## Accepted beatmapsets") + 1
    except ValueError as exc:
        raise AuditError(f"{path}: missing '## Accepted beatmapsets' section") from exc

    accepted: list[int] = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        match = AUDIT_ROW_RE.match(line)
        if match:
            accepted.append(int(match.group(1)))
    if not accepted:
        raise AuditError(f"{path}: accepted beatmapset table is empty")
    duplicates = sorted(item for item in set(accepted) if accepted.count(item) > 1)
    if duplicates:
        raise AuditError(f"{path}: duplicate accepted IDs: {duplicates}")
    return accepted


def structural_audit(
    diff: dict,
    *,
    audit_document: Path | None = None,
    expected_additions: int | None = None,
    allow_removals: bool = False,
    forbid_existing_changes: bool = False,
) -> dict:
    errors: list[str] = []
    if diff["removed"] and not allow_removals:
        errors.append(f"catalog removals require explicit approval: {diff['removed'][:20]}")
    if expected_additions is not None and len(diff["added"]) != expected_additions:
        errors.append(f"expected {expected_additions} additions, found {len(diff['added'])}")
    if forbid_existing_changes and diff["modified"]:
        errors.append(f"pre-existing rows changed: {diff['modified'][:20]}")

    audit_ids: list[int] | None = None
    if audit_document is not None:
        try:
            audit_ids = accepted_ids_from_audit_document(audit_document)
            if sorted(audit_ids) != diff["added"]:
                missing = sorted(set(diff["added"]) - set(audit_ids))
                extra = sorted(set(audit_ids) - set(diff["added"]))
                errors.append(
                    "audit document accepted IDs do not match catalog additions: "
                    f"missing={missing[:20]} extra={extra[:20]}"
                )
        except (AuditError, OSError) as exc:
            errors.append(str(exc))

    return {
        **diff,
        "audit_document": str(audit_document) if audit_document else None,
        "audit_document_ids": audit_ids,
        "errors": errors,
    }


def _target_ids(diff: dict, scope: str) -> list[int]:
    if scope == "added":
        return diff["added"]
    return sorted(set(diff["added"]) | set(diff["modified"]))


def provenance_audit(base: Catalog, current: Catalog, diff: dict, *, scope: str, workers: int) -> dict:
    targets = [current.entries[item] for item in _target_ids(diff, scope)]
    audits = audit_entries(targets, workers=workers)
    violations = new_generic_verification_violations(current, base)
    payload = _report_payload(audits, violations)
    review_flags = [
        audit.beatmapset_id for audit in audits if audit.verdict in {"red_flag", "ambiguous"}
    ]
    errors: list[str] = []
    if violations:
        errors.append(f"unsafe generic-source verification: {violations[:20]}")
    if review_flags:
        errors.append(f"external provenance needs review: {review_flags[:20]}")
    payload["review_flags"] = review_flags
    payload["errors"] = errors
    return payload


def _identity(entry) -> dict:
    result = {field: getattr(entry, field) for field in IDENTITY_FIELDS}
    result["modes"] = sorted(entry.modes)
    return result


def _identity_mismatches(left, right) -> list[str]:
    left_identity, right_identity = _identity(left), _identity(right)
    return [field for field in left_identity if left_identity[field] != right_identity[field]]


def live_osu_audit(current: Catalog, diff: dict, *, scope: str, workers: int) -> dict:
    ids = _target_ids(diff, scope)
    if not ids:
        return {"checked": 0, "failures": [], "errors": []}

    api = OsuApi.from_env()
    api.token()

    def verify(beatmapset_id: int) -> dict:
        stored = current.entries[beatmapset_id]
        api_entry = entry_from_osu(
            api.beatmapset(beatmapset_id),
            evidence=stored.evidence,
            confidence=stored.confidence,
        )
        stored_mismatches = _identity_mismatches(stored, api_entry)
        if stored_mismatches:
            raise AuditError("catalog/API drift: " + ", ".join(stored_mismatches))

        page_raw = parse_beatmapset_page(get_text(f"https://osu.ppy.sh/beatmapsets/{beatmapset_id}"))
        page_entry = entry_from_osu(
            page_raw,
            evidence=stored.evidence,
            confidence=stored.confidence,
        )
        page_mismatches = _identity_mismatches(api_entry, page_entry)
        if page_mismatches:
            raise AuditError("API/public-page drift: " + ", ".join(page_mismatches))
        return {"beatmapset_id": beatmapset_id, "status": "exact"}

    failures: list[dict] = []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(verify, item): item for item in ids}
        for future in as_completed(futures):
            beatmapset_id = futures[future]
            try:
                future.result()
            except Exception as exc:
                failures.append({"beatmapset_id": beatmapset_id, "error": str(exc)})
    failures.sort(key=lambda item: item["beatmapset_id"])
    errors = [f"live osu! identity failures: {[item['beatmapset_id'] for item in failures[:20]]}"] if failures else []
    return {"checked": len(ids), "failures": failures, "errors": errors}


def _write_report(path: Path | None, report: dict) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _print_summary(report: dict) -> None:
    print(f"Deep review: status={report['status']} mode={report['mode']}")
    structural = report.get("structural")
    if structural:
        print(
            "Catalog diff: "
            f"base={structural['base_entries']} current={structural['current_entries']} "
            f"added={len(structural['added'])} modified={len(structural['modified'])} "
            f"removed={len(structural['removed'])}"
        )
    provenance = report.get("provenance")
    if provenance:
        print(
            "Provenance: "
            f"checked={provenance['checked']} supported={provenance['supported']} "
            f"review_flags={len(provenance['review_flags'])} "
            f"provider_errors={provenance['provider_errors']}"
        )
    live = report.get("live_osu")
    if live:
        print(f"Live osu!: checked={live['checked']} failures={len(live['failures'])}")
    for error in report["errors"]:
        print(f"error: {error}", file=sys.stderr)


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--repository", type=Path, default=Path("."))
    result.add_argument("--catalog", type=Path, default=Path("data/catalog"))
    result.add_argument("--base-ref", default="main")
    result.add_argument("--mode", choices=("structural", "provenance", "live-osu", "all"), default="structural")
    result.add_argument("--scope", choices=("added", "changed"), default="changed")
    result.add_argument("--workers", type=int, default=4)
    result.add_argument("--audit-doc", type=Path)
    result.add_argument("--expected-additions", type=int)
    result.add_argument("--allow-removals", action="store_true")
    result.add_argument("--forbid-existing-changes", action="store_true")
    result.add_argument("--require-base-ancestor", action="store_true")
    result.add_argument("--output", type=Path)
    result.add_argument("--json", action="store_true", help="print the complete report to stdout")
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    report: dict = {"mode": args.mode, "status": "failed", "errors": []}
    try:
        if args.workers < 1:
            raise AuditError("workers must be at least 1")
        repository = args.repository.resolve()
        context = revision_context(repository, args.base_ref)
        report["revision"] = {
            "head": context.head,
            "base_tip": context.base_tip,
            "merge_base": context.merge_base,
            "base_is_ancestor": context.base_is_ancestor,
        }
        if args.require_base_ancestor and not context.base_is_ancestor:
            raise AuditError(f"{args.base_ref} is not an ancestor of HEAD; update the review branch first")

        current_path = args.catalog if args.catalog.is_absolute() else repository / args.catalog
        current = Catalog.load(current_path)
        base = load_catalog_at(repository, context.merge_base, args.catalog)
        diff = catalog_diff(base, current)

        if args.mode in {"structural", "all"}:
            audit_document = args.audit_doc
            if audit_document is not None and not audit_document.is_absolute():
                audit_document = repository / audit_document
            report["structural"] = structural_audit(
                diff,
                audit_document=audit_document,
                expected_additions=args.expected_additions,
                allow_removals=args.allow_removals,
                forbid_existing_changes=args.forbid_existing_changes,
            )
            report["errors"].extend(report["structural"]["errors"])

        if not report["errors"] and args.mode in {"provenance", "all"}:
            report["provenance"] = provenance_audit(
                base, current, diff, scope=args.scope, workers=args.workers
            )
            report["errors"].extend(report["provenance"]["errors"])

        if not report["errors"] and args.mode in {"live-osu", "all"}:
            report["live_osu"] = live_osu_audit(
                current, diff, scope=args.scope, workers=args.workers
            )
            report["errors"].extend(report["live_osu"]["errors"])
    except Exception as exc:
        report["errors"].append(str(exc))

    report["status"] = "passed" if not report["errors"] else "failed"
    _write_report(args.output, report)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        _print_summary(report)
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
