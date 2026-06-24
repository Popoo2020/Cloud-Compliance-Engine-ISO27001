# Quality and Security Checklist

## CI quality gates

Before merge or external presentation, confirm:

- [ ] Ruff linting passes.
- [ ] Pytest passes.
- [ ] Bandit review passes.
- [ ] Dependency review passes.
- [ ] Sample report generation succeeds.
- [ ] CodeQL completes successfully.

## Security and governance gates

- [ ] No real client evidence is committed.
- [ ] No private values are committed.
- [ ] Sample data is clearly fictional.
- [ ] README does not claim certification or audit approval.
- [ ] Report output is reviewed before external use.
- [ ] Limitations are visible to readers.

## Portfolio readiness gates

- [ ] Architecture document is present.
- [ ] Threat model is present.
- [ ] Demo output is documented.
- [ ] Recruiter summary is present.
- [ ] Version notes are present.
- [ ] Makefile validation target is present.

## Future readiness gates

- [ ] Add JSON schema validation.
- [ ] Add evidence freshness fields.
- [ ] Add owner sign-off fields.
- [ ] Add exception expiry fields.
- [ ] Add PDF/HTML report export.
