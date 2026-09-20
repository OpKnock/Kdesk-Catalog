---
applyTo: "**/*.html **/*.json **/*.r **/*.sh **/*.tf"
---

# Api Compliance Scanning

Prepares APIs for audits: scans infrastructure and code for GDPR and SOC 2 gaps, prioritizes findings, and drives remediation.

## Instructions

# API Compliance (Audit & Remediation)

Runs compliance scanners, builds evidence packages, and drives remediation to close GDPR/SOC 2 gaps.

## When to Use
- Pre-audit evidence collection
- Detecting security misconfigurations
- Continuous compliance in CI

## Real Commands

```bash
# Install scanners
pip install checkov
brew install tfsec
pip install prowler
pip install scoutsuite

# Scan everything
checkov -d . --framework terraform --quiet
prowler aws -M csv -o reports/
scout aws --report-dir reports/scout

# Rank findings
tfsec . --format csv --out tfsec.csv && sort -t, -k4 -r tfsec.csv | head -20
```

## Audit Checklist
- Encryption in transit (TLS 1.2+)
- Logging and access records retained
- Data minimization in API responses
- Subprocessor contracts documented

## Testing
Re-run scanners after each remediation and track FAILED counts down to zero for critical checks.

## Best Practices
- Scan in CI on every change
- Keep a baseline for known-accepted risks
- Produce HTML reports for auditors

## Capabilities

### compliance-scanning
Run infrastructure and IaC scanners for compliance benchmarks

**Commands:**
- `checkov -d . --framework terraform --quiet`
- `tfsec . --format json --out tfsec.json`
- `prowler aws -M csv -o reports/`
- `scout aws --report-dir reports/scout`
- `checkov -d . --check CKV_AWS_115 --compact`

**Examples:**
- checkov -d . --framework terraform --quiet --baseline .checkov.baseline
- prowler aws -M csv -o reports/ && head -5 reports/*.csv
- tfsec . --format json --out tfsec.json && jq '.results[0:3]' tfsec.json

### remediation
Prioritize findings by severity and fix the highest-risk compliance gaps

**Commands:**
- `checkov -d . --quiet | grep -E 'FAILED|PASSED' | awk '{print $3}' | sort | uniq -c`
- `tfsec . --format csv --out tfsec.csv && sort -t, -k4 -r tfsec.csv | head`
- `prowler aws -M html -o reports/`
- `scout aws --report-dir reports/scout --rebase`
- `checkov -d . --download-external-modules --quiet`

**Examples:**
- tfsec . --format csv --out tfsec.csv && sort -t, -k4 -r tfsec.csv | head -20
- prowler aws -M html -o reports/ && open reports/report.html
- checkov -d . --quiet | grep FAILED | wc -l
