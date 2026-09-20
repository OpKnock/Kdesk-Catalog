---
applyTo: "**/*.json **/*.r **/*.sh **/*.tf"
---

# tflint

Install plugins, lint Terraform modules recursively, and output in CI formats. deprecations.'

## Instructions

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
