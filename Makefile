.PHONY: lint test security audit report validate

lint:
	ruff check src tests

test:
	pytest -q tests

security:
	bandit -r src -ll

audit:
	pip-audit -r requirements.txt

report:
	python -m src.report_generator
	test -f samples/generated_report.md

validate: lint test security audit report
