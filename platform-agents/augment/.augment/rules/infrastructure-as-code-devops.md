---
type: agent_requested
description: "Reviews and secures Infrastructure-as-Code (Terraform/OpenTofu, Ansible, CloudFormation) with static analysis, linting, and drift detection. Use when working with terraform review, iac scanning, devops or when the user mentions terraform review, iac scanning, devops."
---

Reviews and secures Infrastructure-as-Code (Terraform/OpenTofu, Ansible, CloudFormation) with static analysis, linting, and drift detection.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `terraform fmt -recursive -check`, `checkov -d . --framework terraform,ansible`
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

# Infrastructure-as-Code Quality

Keep Terraform, OpenTofu, Ansible, and CloudFormation code correct, formatted, and secure.

## What This Skill Does

- Formats and validates Terraform/OpenTofu modules
- Runs plan-time checks for drift and unintended changes
- Scans IaC for security misconfigurations (checkov/tfsec/terrascan)
- Lints Ansible playbooks and validates syntax
- Locks provider platforms for reproducible installs

## When to Use

- PR review gates for infrastructure changes
- Onboarding a repo onto proper IaC hygiene
- Investigating why a plan does things you did not expect

## Real Commands

```bash
# Terraform hygiene
terraform fmt -recursive -check
terraform validate
tofu plan -out plan.tfplan
terraform plan -detailed-exitcode   # 0=no diff 1=diff 2=error
terraform providers lock -platform=linux_amd64 -platform=darwin_arm64

# Scanning
checkov -d . --framework terraform,ansible --download-external-modules false
tfsec . --severity CRITICAL,HIGH
terrascan scan -d .
checkov -d . --skip-check CKV_AWS_123,CKV_AWS_126

# Ansible
ansible-lint playbooks/
ansible-playbook playbooks/deploy.yml --syntax-check
ansible-playbook playbooks/deploy.yml --check --diff
```

## Gate Sequence

1. terraform fmt -check
2. terraform validate
3. checkov/tfsec scan (fail on CRITICAL/HIGH)
4. ansible-lint
5. plan review with -detailed-exitcode

## Best Practices

- Enforce `terraform fmt -check` in CI; reject unformatted PRs
- Use `terraform plan -lock=false` carefully — prefer locking
- Scan IaC before apply, not after: misconfigs ship fast
- Keep modules small; test with `terraform plan` per module
- Treat provider/version pinning as part of review

## Capabilities

### terraform-review
Validate, format, and plan Terraform or OpenTofu configurations.

**Parameters:**
- `dir` (string): Module directory
- `plan-file` (string): Plan output path

**Commands:**
- `terraform fmt -recursive -check`
- `terraform validate`
- `tofu plan -out plan.tfplan`
- `terraform plan -lock=false -detailed-exitcode`
- `terraform providers lock -platform=linux_amd64 -platform=darwin_arm64`

**Examples:**
- terraform fmt -recursive -check
- tofu plan -out plan.tfplan
- terraform validate

### iac-scanning
Scan IaC for misconfigurations with checkov, tfsec, and terrascan.

**Parameters:**
- `path` (string): Directory to scan
- `severity` (string): Minimum severity to report

**Commands:**
- `checkov -d . --framework terraform,ansible`
- `checkov -d . --skip-check CKV_AWS_123`
- `tfsec . --severity CRITICAL,HIGH`
- `terrascan scan -d .`
- `ansible-lint playbooks/`
- `ansible-playbook playbooks/deploy.yml --syntax-check`

**Examples:**
- checkov -d .
- tfsec . --severity CRITICAL,HIGH
- ansible-lint playbooks/

## References
- [Terraform Docs](https://developer.hashicorp.com/terraform/docs)
- [Checkov](https://www.checkov.io/)
- [tfsec](https://github.com/aquasecurity/tfsec)
- [Ansible Lint](https://ansible.readthedocs.io/projects/lint/)