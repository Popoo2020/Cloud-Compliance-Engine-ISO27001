from datetime import date
from pathlib import Path

import pytest

from src.report_generator import (
    build_markdown_report,
    load_controls,
    load_evidence,
    validate_json_schema,
)


def test_build_report_from_sample_data() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    controls = load_controls(repo_root / "templates" / "controls.json")
    records = load_evidence(
        repo_root / "samples" / "sample_evidence.json",
        controls,
        schema_path=repo_root / "schemas" / "evidence.schema.json",
        reference_date=date(2026, 6, 25),
    )
    report = build_markdown_report(records)

    assert "# ISO 27001 Evidence Summary" in report
    assert "Implemented: **1**" in report
    assert "Partial: **1**" in report
    assert "Missing: **1**" in report
    assert "Fresh evidence: **2**" in report
    assert "Stale evidence: **1**" in report
    assert "A.5.15" in report
    assert "A.8.15" in report
    assert "A.8.16" in report


def test_schema_validation_rejects_missing_required_fields() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    bad_data = [
        {
            "control_id": "A.5.15",
            "provider": "Azure",
            "status": "implemented",
            "evidence_ref": "sample-ref",
            "notes": "missing freshness metadata",
        }
    ]

    with pytest.raises(ValueError, match="Evidence schema validation failed"):
        validate_json_schema(bad_data, repo_root / "schemas" / "evidence.schema.json")


def test_freshness_uses_configured_reference_date() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    controls = load_controls(repo_root / "templates" / "controls.json")
    records = load_evidence(
        repo_root / "samples" / "sample_evidence.json",
        controls,
        schema_path=repo_root / "schemas" / "evidence.schema.json",
        reference_date=date(2026, 6, 25),
    )

    stale = [record for record in records if not record.is_fresh]
    assert len(stale) == 1
    assert stale[0].control_id == "A.8.16"
