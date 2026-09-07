---
name: "checkov"
description: "Scan infrastructure files handling policy violations. Generate machine-readable reports. Checkov policy-as-code. Use when working with checkov scan, checkov output, code quality or when the user mentions checkov scan, checkov output, code quality."
license: "MIT"
compatibility: "Requires checkov."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "code-quality"}
allowed-tools: "Glob Grep Read Bash(checkov:*)"
---

Scan infrastructure files handling policy violations. Generate machine-readable reports. Checkov policy-as-code.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `checkov -d .`, `checkov -d . --output sarif --output-file-path ./reports`
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

# Checkov

Policy-as-code scanning for infrastructure.

## When to Use

- Terraform and CloudFormation misconfiguration checks
- Kubernetes manifest security
- Dockerfile best-practice violations
- Shift-left IaC security in CI

## Commands

```bash
# Scan a directory
checkov -d .

# Scan a single file
checkov -f main.tf

# Limit frameworks
checkov -d . --framework terraform,kubernetes

# Skip a known check
checkov -d . --skip-check CKV_AWS_1

# Quiet output (failures only)
checkov -d . --quiet

# Machine-readable reports
checkov -d . --output sarif --output-file-path ./reports
checkov -d . --output junitxml --output-file-path ./reports

# Baseline existing findings
checkov -d . --create-baseline
checkov -d . --baseline .checkov.baseline
```

## Best Practices

- Run checkov in CI on every IaC change
- Use --baseline to track existing debt without blocking
- Fail builds on new findings: use --check or sarif severity
- Scan the plan output, not just the code
- Customize with skip-check only after documented review
- Pin the Checkov version in CI

## Capabilities

### checkov-scan
Scan infrastructure files for policy violations.

**Parameters:**
- `directory` (string): Directory to scan
- `framework` (string): Comma-separated frameworks
- `skip-check` (string): Check ids to skip

**Commands:**
- `checkov -d .`
- `checkov -f main.tf`
- `checkov -d . --framework terraform`
- `checkov -d . --skip-check CKV_AWS_1`
- `checkov -d . --quiet`

**Examples:**
- checkov -d . --framework kubernetes,terraform
- checkov -f main.tf --compact
- checkov -d . --output sarif

### checkov-output
Generate machine-readable reports.

**Parameters:**
- `output` (string): sarif, junitxml, json, cli
- `output-file-path` (string): Report directory

**Commands:**
- `checkov -d . --output sarif --output-file-path ./reports`
- `checkov -d . --output junitxml --output-file-path ./reports`
- `checkov -d . --output json --output-file-path ./reports`
- `checkov -d . --baseline .checkov.baseline`

**Examples:**
- checkov -d . --output sarif --output-file-path ./reports --quiet
- checkov -d . --create-baseline

## References
- [Checkov Docs](https://www.checkov.io)
- [Checkov on GitHub](https://github.com/bridgecrewio/checkov)
