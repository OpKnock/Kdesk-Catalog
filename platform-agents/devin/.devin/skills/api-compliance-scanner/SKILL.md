---
name: "api-compliance-scanner"
description: "Implements compliance scanning: install scanners, run baseline checks, and fix misconfigurations against GDPR and SOC 2. Use when working with scanner setup, baseline scanning or when the user mentions scanner setup, baseline scanning."
license: "MIT"
compatibility: "Requires scout-suite, prowler, checkov, tfsec, node.js, python."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "security"}
allowed-tools: "Glob Grep Read Bash(brew:*) Bash(checkov:*) Bash(pip:*) Bash(prowler:*) Bash(scout:*) Bash(tfsec:*)"
---

Implements compliance scanning: install scanners, run baseline checks, and fix misconfigurations against GDPR and SOC 2.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `pip install checkov`, `checkov -d . --quiet`
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
