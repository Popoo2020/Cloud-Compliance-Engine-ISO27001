# Control Coverage Matrix

This matrix provides a high-level overview of ISO 27001 control coverage by this engine. Each control lists the implemented evidence collector or check.

| ISO 27001 Control | Evidence Collector | Coverage Status | Notes |
|------------------|-------------------|----------------|------|
| A.5.1.1 – Information security policies | Policy document check | Implemented | Collects and verifies presence of documented policies. |
| A.12.4.1 – Event logging | Log configuration collector | Partially Implemented | Currently checks Azure/AWS logging configuration; other providers pending. |
| A.18.1.4 – Privacy and protection of personally identifiable information | Data classification check | Not Implemented | Planned for future release. |

For a comprehensive mapping to all ISO 27001 Annex A controls, please refer to the [templates/report_schema.csv](../templates/report_schema.csv) for fields and to the implementation roadmap in `CHANGELOG.md`.