"""Generate a compact ISO 27001 control-coverage report from JSON evidence.

This module intentionally keeps the first automation step small and auditable:
- load control definitions
- load evidence observations
- aggregate control status
- emit a Markdown report suitable for portfolio demonstration and later extension
"""
from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_VALID_STATUSES = {"implemented", "partial", "missing", "not_applicable"}


@dataclass(frozen=True)
class ControlRecord:
    control_id: str
    title: str
    provider: str
    status: str
    evidence_ref: str
    notes: str


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


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


def load_evidence(path: Path, controls: dict[str, dict[str, str]]) -> list[ControlRecord]:
    """Load evidence observations and validate core fields."""
    raw = _load_json(path)
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

        records.append(
            ControlRecord(
                control_id=control_id,
                title=controls[control_id]["title"],
                provider=str(item.get("provider", "Unknown")).strip() or "Unknown",
                status=status,
                evidence_ref=str(item.get("evidence_ref", "N/A")).strip() or "N/A",
                notes=str(item.get("notes", "")).strip(),
            )
        )
    return records


def build_markdown_report(records: list[ControlRecord]) -> str:
    """Render a Markdown report showing status counts and evidence rows."""
    counts = Counter(record.status for record in records)
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
            "## Control evidence matrix",
            "",
            "| Control | Title | Provider | Status | Evidence reference | Notes |",
            "|---|---|---|---|---|---|",
        ]
    )

    rows = []
    for record in records:
        notes = record.notes.replace("|", "\\|") if record.notes else "-"
        rows.append(
            f"| {record.control_id} | {record.title} | {record.provider} | "
            f"{record.status} | {record.evidence_ref} | {notes} |"
        )
    return summary + "\n" + "\n".join(rows) + "\n"


def generate_report(controls_path: Path, evidence_path: Path, output_path: Path) -> Path:
    """Generate and write a Markdown compliance report."""
    controls = load_controls(controls_path)
    records = load_evidence(evidence_path, controls)
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
