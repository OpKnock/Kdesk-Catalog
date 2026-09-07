---
trigger: glob
description: "Prepares APIs for audits: scans infrastructure and code for GDPR and SOC 2 gaps, prioritizes findings, and drives remediation. Use when working with compliance scanning, remediation or when the user mentions compliance scanning, remediation."
globs: ["**/*.html", "**/*.json", "**/*.r", "**/*.sh", "**/*.tf"]
---

Prepares APIs for audits: scans infrastructure and code for GDPR and SOC 2 gaps, prioritizes findings, and drives remediation.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `checkov -d . --framework terraform --quiet`, `checkov -d . --quiet | grep -E 'FAILED|PASSED' | awk '{print`
- Check `knowledge` references and prerequisites before proceeding

### 2. Reason
Analyze and plan:
- Compare current state vs desired state (drift, checksums, policy)
- Evaluate trust, compatibility, and risk: use `kdesk trust` and `kdesk doctor` patterns
- Decide: which capabilities/tools are needed, which can be skipped

### 3. Act
Execute with guards:
- Run only `allowed-tools` (see frontmatter); use `safe_path` for writes
- Prefer `Bash` with explicit binaries (`curl`, `kubectl`, `kdesk`) over generic shell
- Record evidence: file paths, checksums, and tool outputs for verification

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

**Parameters:**
- `framework` (string): IaC framework to scan
- `output` (string): Report directory or file

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

**Parameters:**
- `severity` (string): Severity filter
- `reportFormat` (string): csv, html, json

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

## References
- [Checkov Docs](https://www.checkov.io/documentation)
- [Prowler Docs](https://docs.prowler.com/)
- [tfsec](https://github.com/aquasecurity/tfsec)
