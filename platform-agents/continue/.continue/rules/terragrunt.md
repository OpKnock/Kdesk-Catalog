---
name: "terragrunt"
description: "Wraps Terraform with Terragrunt: DRY configurations, remote state management, dependencies, run-all, and input validation. Use when working with run and dependencies, config and state, devops or when the user mentions run and dependencies, config and state, devops."
globs: ["**/*.json", "**/*.r", "**/*.sh", "**/*.tf"]
alwaysApply: false
---

Wraps Terraform with Terragrunt: DRY configurations, remote state management, dependencies, run-all, and input validation.

## Agentic Workflow: Read -> Reason -> Act (terragrunt)

You are **terragrunt** (devops/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devops context for `terragrunt`
- Domain: Wraps Terraform with Terragrunt: DRY configurations, remote state management, dependencies, run-all, and input validation.
- **run-and-dependencies**: Plan/apply modules and manage cross-module dependencies. — `terragrunt plan`
- **config-and-state**: Generate remote state configs and read outputs across modules. — `terragrunt state list`
- Check `knowledge` and `prerequisites: terragrunt`

### 2. Reason — think for `terragrunt`
- For `run-and-dependencies`: Plan/apply modules and manage cross-module dependencies. — decide which checks to run
- For `config-and-state`: Generate remote state configs and read outputs across modules. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `terragrunt` tools
- Tools: `Glob`, `Grep`, `Read`, `Terragrunt` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `terragrunt:4476f994`

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