# Changelog

This file documents notable changes to **Cloud-Compliance-Engine-ISO27001**.

## [Unreleased] - 2026-06-24

### Added
- Release checklist for creating a GitHub `v0.1.0` portfolio release.
- Architecture documentation.
- Threat model.
- Demo output documentation.
- Quality and security checklist.
- Version notes.
- Makefile validation target.
- CI validation through `make validate`.
- Recruiter summary for hiring-manager review.
- Bandit review, dependency review and CodeQL analysis in the portfolio hardening workflow.

### Changed
- CI validation now runs linting, tests, static review, dependency review and sample report generation through a single validation target.
- Documentation now presents the project as a portfolio-grade compliance automation baseline, not a certification or audit tool.

## [0.1.0] - 2026-03-01

### Added
- Report schema templates for ISO 27001-oriented control mapping, evidence fields, status, owner and notes.
- Control coverage matrix documentation describing how controls map to cloud services and compliance checks.
- Sample sanitized report to illustrate compliance-assessment output without exposing sensitive customer data.
- Initial best-practice files including license, security policy, code of conduct and contributing guidelines.
- Initial public release marker for collaborator and portfolio review.
