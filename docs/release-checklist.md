# Release Checklist

Use this checklist before publishing a GitHub release such as `v0.1.0`.

## Release title

`v0.1.0 - Portfolio Readiness Release`

## Pre-release validation

- [ ] Pull request is merged into `main`.
- [ ] CI workflow passed.
- [ ] CodeQL workflow passed.
- [ ] `make validate` runs successfully.
- [ ] `samples/generated_report.md` is generated successfully.
- [ ] README links work.
- [ ] Architecture document is present.
- [ ] Threat model is present.
- [ ] Demo output document is present.
- [ ] Quality and security checklist is present.
- [ ] Changelog and version notes are present.

## Security and governance review

- [ ] No real client evidence is included.
- [ ] No secrets or credentials are included.
- [ ] Sample data is suitable for public portfolio review.
- [ ] README does not claim certification or audit approval.
- [ ] Generated reports are positioned as examples for human review.

## Suggested release description

```text
Portfolio readiness release of Cloud-Compliance-Engine-ISO27001.

This release demonstrates a lightweight ISO 27001-oriented compliance automation workflow that turns structured control and evidence data into a generated Markdown report.

Included:
- Control templates
- Sample evidence records
- Report generator
- Tests and CI validation
- Architecture documentation
- Threat model
- Demo output documentation
- Quality and security checklist
- Recruiter summary
```

## Post-release actions

- [ ] Add the release link to the README or GitHub profile.
- [ ] Mention the release in LinkedIn/GitHub portfolio updates.
- [ ] Add screenshots of generated report output.
