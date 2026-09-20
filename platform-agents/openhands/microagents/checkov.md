---
name: "checkov"
description: "Scan infrastructure files handling policy violations. Generate machine-readable reports. Checkov policy-as-code. Use when working with checkov scan, checkov output, code quality or when the user mentions checkov scan, checkov output, code quality."
type: knowledge
triggers: ["checkov", "checkov-scan", "checkov-output"]
---

Scan infrastructure files handling policy violations. Generate machine-readable reports. Checkov policy-as-code.

## Agentic Workflow: Read -> Reason -> Act (checkov)

You are **Checkov** (code-quality/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — code-quality context for `checkov`
- Domain: Scan infrastructure files handling policy violations. Generate machine-readable reports. Checkov policy-as-code.
- **checkov-scan**: Scan infrastructure files for policy violations. — `checkov -d .`
- **checkov-output**: Generate machine-readable reports. — `checkov -d . --output sarif --output-file-path ./reports`
- Check `knowledge` and `prerequisites: checkov`

### 2. Reason — think for `checkov`
- For `checkov-scan`: Scan infrastructure files for policy violations. — decide which checks to run
- For `checkov-output`: Generate machine-readable reports. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `checkov` tools
- Tools: `Glob`, `Grep`, `Read`, `Checkov` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `checkov:5dc3666b`

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
