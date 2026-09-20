---
name: "terraform-validate"
description: "Validates Terraform configurations: formatting, syntax, and plan validation against real providers."
---

# Terraform Validate

Validates Terraform configurations: formatting, syntax, and plan validation against real providers.

## Instructions

# Terraform Validate

Static validation of Terraform configurations: syntax, internal consistency, and
provider schema correctness.

## When to Use

- CI checks before terraform plan
- Catching invalid resource references early
- Verifying fmt compliance without modifying files

## Real Commands

```bash
# Init without remote backend access (safe in CI)
terraform init -backend=false

# Core validation
terraform validate

# JSON output for CI parsing
terraform validate -json | jq .valid

# Format check
terraform fmt -check -recursive

# Apply formatting
terraform fmt -recursive

# Full plan (requires providers to be initialized)
terraform plan -detailed-exitcode -out=plan.tfplan

# With environment-specific variables
terraform plan -var-file=environments/dev.tfvars -input=false
```

## CI Workflow

```yaml
- name: Validate
  run: |
    terraform fmt -check -recursive
    terraform init -backend=false
    terraform validate
```

## Notes

- `terraform validate` needs initialized providers unless `-backend=false` is used
- `-json` output has `valid` and `diagnostics` fields
- Exit code 2 from `plan -detailed-exitcode` means changes are pending

## Best Practices

- Run `fmt -check` before `validate` so diffs are readable
- Never run `terraform apply` from CI without a human-approved plan
- Use `-input=false` everywhere in automation
- Validate on the CI agent with the same Terraform version as prod

## Example Response

Returns the validation verdict, any diagnostics with `path:line` (error/warning),
and the fmt compliance status.

## Capabilities

### terraform-validate
Init, validate, format-check, and plan Terraform configurations

**Commands:**
- `terraform init -backend=false`
- `terraform validate`
- `terraform validate -json`
- `terraform fmt -check -recursive`
- `terraform plan -detailed-exitcode -out=plan.tfplan`

**Examples:**
- terraform init -backend=false -upgrade
- terraform fmt -recursive
- terraform plan -var-file=environments/dev.tfvars -input=false
