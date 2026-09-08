---
applyTo: "**/*.r **/*.sh"
---

Implements compliance scanning: install scanners, run baseline checks, and fix misconfigurations against GDPR and SOC 2.

## Agentic Workflow: Read -> Reason -> Act (api-compliance-scanner)

You are **Api Compliance Scanner** (security) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — security context for `api-compliance-scanner`
- Domain: Implements compliance scanning: install scanners, run baseline checks, and fix misconfigurations against GDPR and SOC 2.
- **scanner-setup**: Install and configure compliance scanners locally and in CI — `pip install checkov`
- **baseline-scanning**: Run baseline scans and fix the highest-severity findings — `checkov -d . --quiet`
- Check `knowledge` and `prerequisites: scout-suite, prowler, checkov`

### 2. Reason — think for `api-compliance-scanner`
- For `scanner-setup`: Install and configure compliance scanners locally and in CI — decide which checks to run
- For `baseline-scanning`: Run baseline scans and fix the highest-severity findings — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-compliance-scanner` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Brew` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-compliance-scanner:e6ecf832`

# API Compliance (Implementation)

Gets compliance scanning running and fixes baseline findings.

## When to Use
- No scanning exists yet
- Preparing infrastructure for compliance
- Quick wins on misconfigurations

## Real Commands

```bash
# Install
pip install checkov prowler scoutsuite
brew install tfsec

# Baseline scans
checkov -d . --quiet
tfsec .
prowler aws --group group17 --severity high
scout aws --report-dir reports/scout --services ec2,s3

# Targeted check
checkov -d . --check CKV_AWS_20 --quiet
```

## Fix Loop
1. Run baseline
2. Fix critical findings
3. Re-scan
4. Baseline accepted risks

## CI Hook
Add `checkov -d . --quiet` as a pipeline step so new misconfigurations fail fast.

## Testing
Verify fixes by re-running the exact failing check ID.

## Best Practices
- Fix encryption and logging checks first
- Keep scanner versions pinned

## Capabilities

### scanner-setup
Install and configure compliance scanners locally and in CI

**Parameters:**
- `scanner` (string): checkov, tfsec, prowler, scoutsuite
- `target` (string): Scan target

**Commands:**
- `pip install checkov`
- `pip install prowler`
- `pip install scoutsuite`
- `brew install tfsec`
- `checkov --version && tfsec --version`

**Examples:**
- pip install checkov prowler scoutsuite && checkov --version
- brew install tfsec && tfsec --version
- pip install checkov && checkov -d . --quiet

### baseline-scanning
Run baseline scans and fix the highest-severity findings

**Parameters:**
- `dir` (string): Directory to scan
- `check` (string): Specific check ID

**Commands:**
- `checkov -d . --quiet`
- `tfsec .`
- `prowler aws --group group17`
- `scout aws --report-dir reports/scout --services ec2,s3`
- `checkov -d . --check CKV_AWS_20 --quiet`

**Examples:**
- checkov -d . --quiet && tfsec .
- prowler aws --group group17 --severity high
- scout aws --report-dir reports/scout --services ec2,s3

## References
- [Checkov Quickstart](https://www.checkov.io/1.Introduction/Quickstart.html)
- [Prowler AWS Checks](https://docs.prowler.com/projects/prowler-open-source/en/latest/)
