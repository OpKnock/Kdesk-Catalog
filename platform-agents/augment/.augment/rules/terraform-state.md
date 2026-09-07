---
type: agent_requested
description: "Manages Terraform state: list/show/mv/rm operations, state pull/push, replace-provider, and workspace-safe state surgery. Use when working with state inspection, state surgery, devops or when the user mentions state inspection, state surgery, devops."
---

Manages Terraform state: list/show/mv/rm operations, state pull/push, replace-provider, and workspace-safe state surgery.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `terraform state list`, `terraform state mv aws_instance.web aws_instance.web2`
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

# Terraform State Management

Inspect and repair Terraform state without losing resources.

## What This Skill Does

- Lists and shows resources in state
- Moves resources when refactoring modules
- Removes orphans safely (state-only, no destroy)
- Replaces provider sources during provider migration
- Pulls/pushes state for backup and repair

## When to Use

- Renaming resources or refactoring into modules
- Removing resources no longer managed but still running
- Migrating providers (hashicorp/aws -> custom registry)
- Recovering from corrupt or lost state

## Real Commands

```bash
# Inspect
terraform state list
terraform state list -state=envs/prod/terraform.tfstate
terraform state show aws_instance.web

# Backup
terraform state pull > backup-$(date +%F).tfstate

# Surgery
terraform state mv aws_instance.web aws_instance.web2
terraform state mv 'module.app.aws_s3_bucket.b' 'module.core.aws_s3_bucket.b'
terraform state rm aws_instance.orphan

# Provider replacement
terraform state replace-provider -auto-approve   hashicorp/aws public.ecr.aws/acme/aws

# Restore
terraform state push backup.tfstate
```

## Safety Rules

1. Always `terraform state pull` a backup before surgery
2. Run `terraform plan` after mv to confirm no destroy
3. `state rm` detaches — it does not destroy infrastructure
4. Lock remote state (Terraform Cloud/backend locking) during moves
5. Push state only after validating it locally

## Best Practices

- Prefer `moved {}` blocks for refactors going forward (0.13+)
- Use exact addresses in state commands; verify with list first
- Never edit raw state JSON by hand — use the CLI
- Keep state backups outside the state backend (S3 bucket versioning)
- Review plan after any state change

## Capabilities

### state-inspection
List and inspect resources in Terraform state.

**Parameters:**
- `resource` (string): Resource address, e.g. aws_instance.web
- `state-file` (string): Explicit state file path

**Commands:**
- `terraform state list`
- `terraform state list -state=envs/prod/terraform.tfstate`
- `terraform state show aws_instance.web`
- `terraform state pull > backup.tfstate`
- `terraform state list -id=i-0abc123`

**Examples:**
- terraform state list
- terraform state show aws_instance.web
- terraform state pull > backup.tfstate

### state-surgery
Move, remove, and replace resources in state safely.

**Parameters:**
- `from` (string): Source resource address
- `to` (string): Destination resource address

**Commands:**
- `terraform state mv aws_instance.web aws_instance.web2`
- `terraform state mv 'module.app.aws_s3_bucket.b' 'module.core.aws_s3_bucket.b'`
- `terraform state rm aws_instance.orphan`
- `terraform state replace-provider -auto-approve hashicorp/aws public.ecr.aws/acme/aws`
- `terraform state push backup.tfstate`
- `terraform state list -state-out=renamed.tfstate`

**Examples:**
- terraform state mv aws_instance.web aws_instance.web2
- terraform state rm aws_instance.orphan
- terraform state replace-provider -auto-approve hashicorp/aws public.ecr.aws/acme/aws

## References
- [Terraform State](https://developer.hashicorp.com/terraform/language/state)
- [terraform state Command](https://developer.hashicorp.com/terraform/cli/commands/state)