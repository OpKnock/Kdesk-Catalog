---
name: "tfsec"
description: "Scans Terraform configurations with tfsec's focused security checks, severity gating, and SARIF/JUnit output."
---

# tfsec

Scans Terraform configurations with tfsec's focused security checks, severity gating, and SARIF/JUnit output.

## Instructions

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
