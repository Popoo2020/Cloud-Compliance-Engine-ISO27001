from pathlib import Path

from src.report_generator import build_markdown_report, load_controls, load_evidence


def test_build_report_from_sample_data() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    controls = load_controls(repo_root / "templates" / "controls.json")
    records = load_evidence(repo_root / "samples" / "sample_evidence.json", controls)
    report = build_markdown_report(records)

    assert "# ISO 27001 Evidence Summary" in report
    assert "Implemented: **1**" in report
    assert "Partial: **1**" in report
    assert "Missing: **1**" in report
    assert "A.5.15" in report
    assert "A.8.15" in report
    assert "A.8.16" in report
