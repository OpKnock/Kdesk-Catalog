---
name: "terraform-module-builder"
description: "Builds reusable, tested Terraform modules with scaffolding, validation, docs generation, and tflint compliance. Use when working with module scaffolding, module testing, linting and quality or when the user mentions module scaffolding, module testing, linting and quality."
license: "MIT"
compatibility: "Requires terraform, terragrunt, tflint, checkov, infracost, terratest."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "infrastructure"}
allowed-tools: "Glob Grep Read Bash(terraform:*) Bash(terraform-docs:*) Bash(tflint:*) Bash(tofu:*)"
---

Builds reusable, tested Terraform modules with scaffolding, validation, docs generation, and tflint compliance.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `terraform init`, `terraform plan -var-file=tests/fixtures/dev.tfvars`
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

# Terraform Module Builder

Create production-grade, reusable Terraform modules.

## What This Skill Does

- Scaffolds module structure (variables, outputs, locals, resources)
- Validates and formats code before merge
- Generates README docs with terraform-docs
- Lints with tflint and tests with plan/apply fixtures

## When to Use

- Creating a new reusable module for a team
- Refactoring duplicated config into modules
- Publishing modules to a registry

## Real Commands

```bash
# Scaffold and validate
terraform init
terraform fmt -recursive
terraform validate

# Docs and lint
terraform-docs markdown table . --output-file README.md
tflint --init
tflint --recursive

# Test fixture cycle
terraform plan -var-file=tests/fixtures/dev.tfvars
terraform apply -auto-approve -var-file=tests/fixtures/dev.tfvars
terraform output
terraform destroy -auto-approve -var-file=tests/fixtures/dev.tfvars

# Lock providers for reproducibility
terraform providers lock -platform=linux_amd64
```

## Module Structure

```text
modules/vpc/
  main.tf
  variables.tf
  outputs.tf
  locals.tf
  README.md
  versions.tf
  tests/fixtures/dev.tfvars
```

## Best Practices

- Make modules composable: inputs, outputs, no hidden state
- Version all modules; never point consumers at main
- Document every variable and output (terraform-docs in CI)
- Run tflint and validate in CI on every change
- Test apply/destroy on fixtures before publishing

## Capabilities

### module-scaffolding
Initialize and structure a Terraform module.

**Parameters:**
- `dir` (string): Module directory
- `platform` (string): Provider platform lock, e.g. linux_amd64

**Commands:**
- `terraform init`
- `terraform fmt -recursive`
- `terraform validate`
- `terraform providers lock -platform=linux_amd64`
- `terraform-docs markdown . > README.md`

**Examples:**
- terraform init
- terraform fmt -recursive
- terraform validate

### module-testing
Plan, apply, and destroy test fixtures.

**Parameters:**
- `varFile` (string): Variable file path
- `target` (string): Resource address to target

**Commands:**
- `terraform plan -var-file=tests/fixtures/dev.tfvars`
- `terraform apply -auto-approve -var-file=tests/fixtures/dev.tfvars`
- `terraform destroy -auto-approve -var-file=tests/fixtures/dev.tfvars`
- `terraform state list`
- `terraform output`

**Examples:**
- terraform plan -var-file=tests/fixtures/dev.tfvars
- terraform apply -auto-approve -var-file=tests/fixtures/dev.tfvars
- terraform destroy -auto-approve

### linting-and-quality
Enforce style and best practices with tflint and docs.

**Parameters:**
- `format` (string): tflint output format: default, sarif, json
- `outputFile` (string): Docs output path

**Commands:**
- `tflint --init`
- `tflint --recursive`
- `tflint --format sarif`
- `terraform-docs markdown table . --output-file README.md`
- `tofu fmt -recursive`

**Examples:**
- tflint --init && tflint --recursive
- terraform-docs markdown table . --output-file README.md
- tflint --format sarif --output-file tflint.sarif

## References
- [Terraform Module Documentation](https://developer.hashicorp.com/terraform/language/modules)
- [Terraform Module Best Practices](https://developer.hashicorp.com/terraform/tutorials/modules)
- [tflint Documentation](https://github.com/terraform-linters/tflint)
