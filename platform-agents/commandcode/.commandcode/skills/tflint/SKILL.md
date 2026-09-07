---
name: "tflint"
description: "Install plugins, lint Terraform modules recursively, and output in CI formats. deprecations.'. Use when working with tflint linting, code quality or when the user mentions tflint linting, code quality."
license: "MIT"
compatibility: "Requires tflint."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "code-quality"}
allowed-tools: "Glob Grep Read Bash(tflint:*)"
---

Install plugins, lint Terraform modules recursively, and output in CI formats. deprecations.'

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `tflint --init`
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

# TFLint

Linter for Terraform that catches mistakes terraform validate misses: deprecated
syntax, provider-specific issues, and module problems.

## When to Use

- Enforcing AWS/Azure/GCP best practices in Terraform
- Finding deprecated attributes before they break
- CI lint gate alongside terraform validate

## Real Commands

```bash
# Install
brew install tflint   # or scoop/choco on Windows

# Install configured plugins
cp .tflint.hcl.example .tflint.hcl
tflint --init

# Lint the current directory
tflint

# Lint recursively
tflint --recursive

# JSON output
sudo tflint --format=json . | jq

# Only warn+ findings
sudo tflint --minimum-severity warning

# Specific config
sudo tflint --config .tflint.hcl --chdir=environments/prod
```

## Config (.tflint.hcl)

```hcl
plugin "aws" {
  enabled = true
  version = "0.34.0"
  source  = "github.com/terraform-linters/tflint-ruleset-aws"
}

rule "aws_instance_invalid_type" {
  enabled = true
}
```

## Best Practices

- Commit `.tflint.hcl` and run `tflint --init` in CI before linting
- Pin plugin versions in the config
- Run with `--recursive` in module-heavy repos
- Feed `--format=sarif` into GitHub code scanning

## Example Response

Returns findings as `path:line,col: message (rule)` with severity, then the agent
applies the suggested attribute/configuration fixes.

## Capabilities

### tflint-linting
Install plugins, lint Terraform modules recursively, and output in CI formats

**Parameters:**
- `format` (string): Output format: default, json, checkstyle, sarif
- `minimum-severity` (string): Only report findings at or above: error, warning, notice
- `recursive` (boolean): Lint all .tf files in subdirectories too

**Commands:**
- `tflint --init`
- `tflint`
- `tflint --recursive`
- `tflint --config .tflint.hcl --format json`
- `tflint --minimum-severity warning`

**Examples:**
- tflint --init --chdir=modules/eks
- tflint --call-module-type=all
- tflint --force --format=checkstyle .

## References
- [tflint GitHub](https://github.com/terraform-linters/tflint)
- [tflint plugin docs](https://github.com/terraform-linters/tflint/tree/master/docs)
