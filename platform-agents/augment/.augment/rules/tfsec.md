---
type: agent_requested
description: "Scans Terraform configurations with tfsec's focused security checks, severity gating, and SARIF/JUnit output. Use when working with tfsec scan, reporting and config, security or when the user mentions tfsec scan, reporting and config, security."
---

Scans Terraform configurations with tfsec's focused security checks, severity gating, and SARIF/JUnit output.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `tfsec .`, `tfsec . --format sarif --out scan.sarif`
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

# tfsec

Terraform-focused static security scanning.

## What This Skill Does

- Scans Terraform and Terragrunt for known bad patterns
- Filters by severity and excludes noisy checks
- Emits SARIF, JUnit, JSON, CSV, and HTML reports
- Supports custom config for team policies

## When to Use

- Terraform module CI gates
- Pre-apply security review of plan code
- Auditing existing infrastructure repos

## Real Commands

```bash
# Basic scans
tfsec .
tfsec ./modules

# Severity and exclusions
tfsec . --minimum-severity HIGH
tfsec . --exclude-check AWS089,AWS096

# Reports
tfsec . --format sarif --out scan.sarif
tfsec . --format json --out results.json
tfsec . --no-colour --format junit --out junit.xml

# Custom config
tfsec . --config-file tfsec.yml
```

## tfsec.yml

```yaml
minimum_severity: HIGH
exclude:
  - check: AWS089
    paths:
      - modules/legacy/**
```

## Best Practices

- Gate CI on HIGH+; keep CRITICAL as hard fail
- Exclude checks per path, not globally
- Pair with plan-time tools for context-dependent findings
- Use SARIF for GitHub code scanning annotations
- Keep tfsec.yml in the repo for team consistency

## Capabilities

### tfsec-scan
Scan directories and files with severity and check filters.

**Parameters:**
- `path` (string): Directory or file to scan
- `minimumSeverity` (string): Minimum severity: LOW, MEDIUM, HIGH, CRITICAL
- `excludeCheck` (string): Comma-separated check IDs to exclude

**Commands:**
- `tfsec .`
- `tfsec ./modules`
- `tfsec main.tf`
- `tfsec . --minimum-severity CRITICAL`
- `tfsec . --exclude-check AWS089`

**Examples:**
- tfsec .
- tfsec ./modules --minimum-severity HIGH
- tfsec . --exclude-check AWS089,AWS096

### reporting-and-config
Emit CI reports and manage custom configuration.

**Parameters:**
- `format` (string): Output: standard, json, sarif, junit, csv, html
- `out` (string): Report output file
- `configFile` (string): tfsec config YAML path

**Commands:**
- `tfsec . --format sarif --out scan.sarif`
- `tfsec . --format json --out results.json`
- `tfsec . --config-file tfsec.yml`
- `tfsec . --concise-output`
- `tfsec . --no-colour --format junit --out junit.xml`

**Examples:**
- tfsec . --format sarif --out scan.sarif
- tfsec . --config-file tfsec.yml
- tfsec . --no-colour --format junit --out junit.xml

## References
- [tfsec GitHub](https://github.com/aquasecurity/tfsec)
- [tfsec Documentation](https://aquasecurity.github.io/tfsec/)