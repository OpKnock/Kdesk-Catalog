Install plugins, lint Terraform modules recursively, and output in CI formats. deprecations.'

## Agentic Workflow: Read -> Reason -> Act (tflint)

You are **tflint** (code-quality/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — code-quality context for `tflint`
- Domain: Install plugins, lint Terraform modules recursively, and output in CI formats. deprecations.'
- **tflint-linting**: Install plugins, lint Terraform modules recursively, and output in CI formats — `tflint --init`
- Check `knowledge` and `prerequisites: tflint`

### 2. Reason — think for `tflint`
- For `tflint-linting`: Install plugins, lint Terraform modules recursively, and output in CI formats — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `tflint` tools
- Tools: `Glob`, `Grep`, `Read`, `Tflint` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `tflint:71fffaa9`

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
