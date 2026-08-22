---
type: agent_requested
description: "Writes and applies Terraform configurations: init, plan, apply, format, validate, workspaces, providers, and outputs."
---

# Terraform

Writes and applies Terraform configurations: init, plan, apply, format, validate, workspaces, providers, and outputs.

## Instructions

# Terraform Operations

Provision cloud infrastructure with Terraform: plan, apply, modules, and workspaces.

## What This Skill Does

- Initializes providers and module dependencies
- Plans and applies infrastructure safely
- Formats and validates HCL
- Manages workspaces and provider locking
- Reads outputs for CI consumption

## When to Use

- Provisioning cloud resources reproducibly
- Evolving infrastructure with reviewable diffs
- Building reusable modules

## Real Commands

```bash
# Core loop
terraform init
terraform fmt -recursive
terraform validate
terraform plan -out plan.tfplan
terraform apply plan.tfplan
terraform destroy -auto-approve -target=aws_instance.web

# Modules and workspaces
terraform get -update
terraform workspace new prod
terraform workspace select dev
terraform workspace list

# Outputs and providers
terraform output -json
terraform providers
terraform providers lock -platform=linux_amd64 -platform=darwin_arm64
terraform console
```

## Best Practices

- Always plan with -out and apply that exact plan
- Use -detailed-exitcode in CI to detect diffs
- Pin provider versions in required_providers
- Keep state in remote backends with locking
- Store terraform.tfvars in CI secret storage, not git
- Structure with modules: root modules per environment

## Capabilities

### core-workflow
Initialize, plan, apply, and destroy infrastructure.

**Commands:**
- `terraform init`
- `terraform plan -out plan.tfplan`
- `terraform apply plan.tfplan`
- `terraform destroy -auto-approve`
- `terraform fmt -recursive`
- `terraform validate`

**Examples:**
- terraform init
- terraform plan -out plan.tfplan
- terraform apply plan.tfplan

### modules-and-workspaces
Work with modules, workspaces, outputs, and provider configs.

**Commands:**
- `terraform get -update`
- `terraform workspace new prod`
- `terraform workspace select dev`
- `terraform output -json`
- `terraform providers`
- `terraform providers lock -platform=linux_amd64`

**Examples:**
- terraform get -update
- terraform workspace select prod
- terraform output -json