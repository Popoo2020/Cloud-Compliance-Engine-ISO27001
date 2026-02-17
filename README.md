# Cloud‑Compliance‑Engine‑ISO27001

**Continuous cloud audit and compliance reporting for ISO/IEC 27001**

## Introduction
Organisations operating in regulated industries need to demonstrate compliance with information security standards like ISO/IEC 27001. Traditional manual audits are time‑consuming and error‑prone. Cloud‑Compliance‑Engine‑ISO27001 automates the evidence collection process by continuously auditing Azure and AWS resources and mapping findings directly to ISO 27001 control requirements.

### Key Features
* **Multi‑Cloud Support:** Audits both Azure and AWS using the official SDKs (`azure‑mgmt‑resource`, `boto3`).
* **Control Mapping:** Each check corresponds to a specific ISO 27001 control. Results are compiled into CSV/JSON matrices for audit readiness.
* **Customisable Rules:** Rules are modular Python functions; you can enable, disable or create new rules to fit your environment.
* **Reporting:** Generates human‑readable reports and machine‑readable evidence packages. Future versions will integrate with GRC platforms.

### Directory Structure
```
Cloud-Compliance-Engine-ISO27001/
├── README.md
├── requirements.txt
├── src/
│   ├── azure_checks.py      # Azure resource assessments
│   ├── aws_checks.py        # AWS resource assessments
│   ├── iso_mapping.py       # Maps results to ISO 27001 controls
│   ├── reporter.py          # Compiles CSV/JSON reports
│   └── utils.py
└── data/
    └── iso27001_controls.csv # Reference list of controls
```

### Getting Started
1. Install dependencies: `pip install -r requirements.txt`.
2. Configure authentication for Azure and AWS. Follow the Azure Identity guidance to store service principal credentials as environment variables【987667603810256†L428-L433】. For AWS, configure your `~/.aws/credentials` file.
3. Run `python src/azure_checks.py` and `python src/aws_checks.py` to collect data.
4. Use `python src/iso_mapping.py` to correlate data to control IDs and `python src/reporter.py` to generate reports.

### Roadmap
* ISO 27017 and ISO 27018 control mappings
* GCP support
* Integration with continuous compliance platforms (e.g., Wiz, Drata)
