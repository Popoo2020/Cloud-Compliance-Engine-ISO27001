"""Generate a compact ISO 27001 control-coverage report from JSON evidence.

This module intentionally keeps the first automation step small and auditable:
- load control definitions
- validate evidence observations against a schema
- assess evidence freshness
- aggregate control status
- emit a Markdown report suitable for portfolio demonstration and later extension
"""
from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

_VALID_STATUSES = {"implemented", "partial", "missing", "not_applicable"}
_DEFAULT_REFERENCE_DATE = date(2026, 6, 25)


@dataclass(frozen=True)
class ControlRecord:
    control_id: str
    title: str
    provider: str
    status: str
    evidence_ref: str
    evidence_date: date
    freshness_days: int
    is_fresh: bool
    age_days: int
    notes: str


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_json_schema(data: Any, schema_path: Path) -> None:
    """Validate raw evidence data against a JSON schema."""
    schema = _load_json(schema_path)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda error: error.path)
    if errors:
        details = "; ".join(error.message for error in errors)
        raise ValueError(f"Evidence schema validation failed: {details}")


def load_controls(path: Path) -> dict[str, dict[str, str]]:
    """Load control metadata indexed by control ID."""
    raw = _load_json(path)
    controls: dict[str, dict[str, str]] = {}
    for item in raw:
        control_id = str(item["control_id"]).strip()
        controls[control_id] = {
            "title": str(item["title"]).strip(),
            "objective": str(item.get("objective", "")).strip(),
        }
    return controls


def _parse_iso_date(value: str, field_name: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError(f"{field_name} must use YYYY-MM-DD format") from exc


def load_evidence(
    path: Path,
    controls: dict[str, dict[str, str]],
    schema_path: Path | None = None,
    reference_date: date = _DEFAULT_REFERENCE_DATE,
) -> list[ControlRecord]:
    """Load evidence observations and validate core fields."""
    raw = _load_json(path)
    if schema_path is not None:
        validate_json_schema(raw, schema_path)

    records: list[ControlRecord] = []
    for item in raw:
        control_id = str(item["control_id"]).strip()
        if control_id not in controls:
            raise ValueError(f"Unknown control_id in evidence file: {control_id}")

        status = str(item["status"]).strip().lower()
        if status not in _VALID_STATUSES:
            raise ValueError(
                f"Invalid status for control {control_id}: {status}. "
                f"Expected one of {sorted(_VALID_STATUSES)}"
            )

        evidence_date = _parse_iso_date(str(item["evidence_date"]).strip(), "evidence_date")
        freshness_days = int(item["freshness_days"])
        age_days = (reference_date - evidence_date).days
        is_fresh = age_days <= freshness_days

        records.append(
            ControlRecord(
                control_id=control_id,
                title=controls[control_id]["title"],
                provider=str(item.get("provider", "Unknown")).strip() or "Unknown",
                status=status,
                evidence_ref=str(item.get("evidence_ref", "N/A")).strip() or "N/A",
                evidence_date=evidence_date,
                freshness_days=freshness_days,
                is_fresh=is_fresh,
                age_days=age_days,
                notes=str(item.get("notes", "")).strip(),
            )
        )
    return records


def build_markdown_report(records: list[ControlRecord]) -> str:
    """Render a Markdown report showing status counts and evidence rows."""
    counts = Counter(record.status for record in records)
    freshness_counts = Counter("fresh" if record.is_fresh else "stale" for record in records)
    summary = "\n".join(
        [
            "# ISO 27001 Evidence Summary",
            "",
            "## Status overview",
            "",
            f"- Implemented: **{counts.get('implemented', 0)}**",
            f"- Partial: **{counts.get('partial', 0)}**",
            f"- Missing: **{counts.get('missing', 0)}**",
            f"- Not applicable: **{counts.get('not_applicable', 0)}**",
            "",
            "## Evidence freshness",
            "",
            f"- Fresh evidence: **{freshness_counts.get('fresh', 0)}**",
            f"- Stale evidence: **{freshness_counts.get('stale', 0)}**",
            "",
            "## Control evidence matrix",
            "",
            "| Control | Title | Provider | Status | Evidence reference | Evidence date | Freshness | Notes |",
            "|---|---|---|---|---|---|---|---|",
        ]
    )

    rows = []
    for record in records:
        notes = record.notes.replace("|", "\\|") if record.notes else "-"
        freshness = "fresh" if record.is_fresh else f"stale ({record.age_days} days old)"
        rows.append(
            f"| {record.control_id} | {record.title} | {record.provider} | "
            f"{record.status} | {record.evidence_ref} | {record.evidence_date.isoformat()} | "
            f"{freshness} | {notes} |"
        )
    return summary + "\n" + "\n".join(rows) + "\n"


def generate_report(controls_path: Path, evidence_path: Path, output_path: Path) -> Path:
    """Generate and write a Markdown compliance report."""
    repo_root = Path(__file__).resolve().parent.parent
    controls = load_controls(controls_path)
    records = load_evidence(
        evidence_path,
        controls,
        schema_path=repo_root / "schemas" / "evidence.schema.json",
    )
    report = build_markdown_report(records)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    return output_path


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    generate_report(
        controls_path=repo_root / "templates" / "controls.json",
        evidence_path=repo_root / "samples" / "sample_evidence.json",
        output_path=repo_root / "samples" / "generated_report.md",
    )


if __name__ == "__main__":
    main()
