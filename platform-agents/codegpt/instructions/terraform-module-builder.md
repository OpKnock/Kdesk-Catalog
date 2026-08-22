# terraform-module-builder

Builds reusable, tested Terraform modules with scaffolding, validation, docs generation, and tflint compliance.

## Instructions

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
