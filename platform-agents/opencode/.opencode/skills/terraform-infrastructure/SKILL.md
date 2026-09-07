---
name: "terraform-infrastructure"
description: "Manages infrastructure as code with Terraform: init, plan, apply, state, and modules across environments. Use when working with core, state, infrastructure or when the user mentions core, state, infrastructure."
---

Manages infrastructure as code with Terraform: init, plan, apply, state, and modules across environments.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `terraform init`, `terraform state list`
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

**Parameters:**
- `var-file` (string): Environment variable file
- `out` (string): Save plan to a file
- `target` (string): Target a specific resource/module

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

**Parameters:**
- `address` (string): Resource address like aws_instance.web[0]
- `import-id` (string): Provider resource id to import
- `rm` (string): Remove resource from state

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

## References
- [Terraform CLI](https://developer.hashicorp.com/terraform/cli/commands)
- [Terraform Language](https://developer.hashicorp.com/terraform/language)
- [Terraform Best Practices](https://developer.hashicorp.com/terraform/tutorials/configuration-language/best-practices)
