# Demo Output

This file documents expected demo behaviour for portfolio review.

## Generate sample report

```bash
python -m src.report_generator
```

Expected output:

```text
Wrote samples/generated_report.md
```

## Expected report sections

```text
# ISO 27001 Evidence Summary
## Status overview
## Control evidence details
```

## Example management snapshot

```text
Implemented: 1
Partial: 1
Missing: 1
```

## Quality checks

CI validates that:

- Python imports work,
- report-generation tests pass,
- static review runs,
- dependency review runs,
- a generated sample report exists.
