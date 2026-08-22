---
applyTo: "**/*.r **/*.sh **/*.tf"
---

# terraform-infrastructure

Manages infrastructure as code with Terraform: init, plan, apply, state, and modules across environments.

## Instructions

# Terraform

Provision infrastructure as code with the standard workflow.

## When to Use

- All cloud resources defined in code
- Multi-environment parity (dev/staging/prod)
- Auditability: every change is a reviewed plan

## Core workflow

```bash
terraform init
terraform plan -out=tfplan
terraform apply tfplan
```

Never `apply -auto-approve` in production without a reviewed plan.

## Structure

```
.
├─ main.tf
├─ variables.tf
├─ outputs.tf
├─ envs/
│   ├─ prod.tfvars
│   ├─ staging.tfvars
└─ modules/
    └─ vpc/
```

```bash
terraform plan -var-file=envs/prod.tfvars -out=tfplan
```

## State management

```bash
terraform state list
terraform state show aws_instance.web[0]
terraform import aws_instance.web i-0abc123
terraform state rm aws_instance.legacy
```

Store state in a remote backend with locking:

```hcl
terraform {
  backend "s3" {
    bucket         = "tf-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "tf-locks"
    encrypt        = true
  }
}
```

## Formatting and validation

```bash
terraform fmt -recursive
terraform validate
```

## Best practices

- Use modules for vpc, ec2, rds; keep root config thin.
- Pin provider versions; plan upgrades separately.
- Never store secrets in state - use variable references to a vault.
- Run plan in CI with comment bot on every PR.

## Testing

```bash
terraform validate
terraform plan -detailed-exitcode
```

Add Terratest or tofu test suites for module behavior.

## Capabilities

### core
Run the core Terraform workflow.

**Commands:**
- `terraform init`
- `terraform plan -out=tfplan`
- `terraform apply tfplan`
- `terraform destroy -auto-approve`
- `terraform fmt -recursive`

**Examples:**
- terraform init -upgrade
- terraform plan -var-file=envs/prod.tfvars -out=tfplan
- terraform apply -auto-approve -target=module.vpc

### state
Inspect and repair Terraform state.

**Commands:**
- `terraform state list`
- `terraform state show aws_instance.web[0]`
- `terraform import aws_instance.web i-0abc123`
- `terraform state rm aws_instance.legacy`
- `terraform refresh`

**Examples:**
- terraform state list | grep module.vpc
- terraform state show aws_s3_bucket.logs
- terraform import aws_iam_user.ci ci-bot
