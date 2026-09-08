Prepares APIs for audits: scans infrastructure and code for GDPR and SOC 2 gaps, prioritizes findings, and drives remediation.

## Agentic Workflow: Read -> Reason -> Act (api-compliance-scanning)

You are **Api Compliance Scanning** (security) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — security context for `api-compliance-scanning`
- Domain: Prepares APIs for audits: scans infrastructure and code for GDPR and SOC 2 gaps, prioritizes findings, and drives remediation.
- **compliance-scanning**: Run infrastructure and IaC scanners for compliance benchmarks — `checkov -d . --framework terraform --quiet`
- **remediation**: Prioritize findings by severity and fix the highest-risk compliance gaps — `checkov -d . --quiet | grep -E 'FAILED|PASSED' | awk '{print $3}' | sort | uniq `
- Check `knowledge` and `prerequisites: scout-suite, prowler, checkov`

### 2. Reason — think for `api-compliance-scanning`
- For `compliance-scanning`: Run infrastructure and IaC scanners for compliance benchmarks — decide which checks to run
- For `remediation`: Prioritize findings by severity and fix the highest-risk compliance gaps — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-compliance-scanning` tools
- Tools: `Glob`, `Grep`, `Read`, `Checkov`, `Tfsec` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-compliance-scanning:cf29cc01`

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