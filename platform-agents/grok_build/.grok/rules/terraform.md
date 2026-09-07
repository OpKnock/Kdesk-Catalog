Writes and applies Terraform configurations: init, plan, apply, format, validate, workspaces, providers, and outputs.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `terraform init`, `terraform get -update`
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

**Parameters:**
- `plan-file` (string): Saved plan file
- `dir` (string): Config directory

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

**Parameters:**
- `workspace` (string): Workspace name
- `output` (string): Output name to query

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

## References
- [Terraform Documentation](https://developer.hashicorp.com/terraform/docs)
- [Terraform Language](https://developer.hashicorp.com/terraform/language)
- [Terraform Registry](https://registry.terraform.io/)