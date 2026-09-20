---
applyTo: "**/*.json **/*.r **/*.sh **/*.tf"
---

Wraps Terraform with Terragrunt: DRY configurations, remote state management, dependencies, run-all, and input validation.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `terragrunt plan`, `terragrunt state list`
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

# Terragrunt

Keep Terraform DRY across environments: shared backend configs, module versions, and orchestrated runs.

## What This Skill Does

- Generates consistent remote state backends from terragrunt.hcl
- Runs multiple modules in dependency order (run-all)
- Reads outputs from one module into another
- Validates inputs before apply
- Formats terragrunt HCL

## When to Use

- Many environments (dev/staging/prod) with the same modules
- Orchestrating multi-module applies in one command
- Centralizing state and provider config

## Real Commands

```bash
# Single module
terragrunt plan
terragrunt apply -auto-approve
terragrunt destroy
terragrunt validate-inputs

# Multi-module orchestration
terragrunt run-all plan
terragrunt run-all apply --terragrunt-non-interactive
terragrunt run-all destroy

# State and outputs
terragrunt state list
terragrunt output -json
terragrunt init --backend-config backend.tfvars
terragrunt hclfmt

# Targeting
terragrunt apply -target=module.vpc
```

## terragrunt.hcl Example

```hcl
terraform {
  source = "git::git@github.com:acme/infra-modules.git//vpc?ref=v1.2.0"
}
remote_state {
  backend = "s3"
  config = {
    bucket = "acme-tfstate"
    key    = "${path_relative_to_include()}/terraform.tfstate"
    region = "us-east-1"
  }
}
inputs = {
  environment = local.environment
}
```

## Best Practices

- Use `run-all` for environment-wide operations in dependency order
- Keep one root terragrunt.hcl with locals for paths and regions
- Version module sources with git refs/tags
- Validate inputs before big applies
- Lock Terragrunt version in CI to match developer versions

## Capabilities

### run-and-dependencies
Plan/apply modules and manage cross-module dependencies.

**Parameters:**
- `command` (string): Terraform command to wrap
- `run-all` (boolean): Run across all modules in dependency order

**Commands:**
- `terragrunt plan`
- `terragrunt apply -auto-approve`
- `terragrunt run-all plan`
- `terragrunt run-all apply --terragrunt-non-interactive`
- `terragrunt run-all destroy`
- `terragrunt validate-inputs`

**Examples:**
- terragrunt plan
- terragrunt run-all plan
- terragrunt validate-inputs

### config-and-state
Generate remote state configs and read outputs across modules.

**Parameters:**
- `backend-config` (string): Backend config file
- `target` (string): Resource or module target

**Commands:**
- `terragrunt state list`
- `terragrunt output`
- `terragrunt output -json`
- `terragrunt init --backend-config backend.tfvars`
- `terragrunt apply -target=module.vpc`
- `terragrunt hclfmt`

**Examples:**
- terragrunt output -json
- terragrunt init --backend-config backend.tfvars
- terragrunt hclfmt

## References
- [Terragrunt Documentation](https://terragrunt.gruntwork.io/docs/)
- [Terragrunt Configuration](https://terragrunt.gruntwork.io/docs/reference/config-blocks-and-attributes/)
