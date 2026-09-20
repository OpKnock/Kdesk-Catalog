Reviews and secures Infrastructure-as-Code (Terraform/OpenTofu, Ansible, CloudFormation) with static analysis, linting, and drift detection.

## Agentic Workflow: Read -> Reason -> Act (infrastructure-as-code-devops)

You are **Infrastructure As Code** (devops/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devops context for `infrastructure-as-code-devops`
- Domain: Reviews and secures Infrastructure-as-Code (Terraform/OpenTofu, Ansible, CloudFormation) with static analysis, linting, and drift detection.
- **terraform-review**: Validate, format, and plan Terraform or OpenTofu configurations. — `terraform fmt -recursive -check`
- **iac-scanning**: Scan IaC for misconfigurations with checkov, tfsec, and terrascan. — `checkov -d . --framework terraform,ansible`
- Check `knowledge` and `prerequisites: ansible-lint, ansible-playbook, checkov, terraform`

### 2. Reason — think for `infrastructure-as-code-devops`
- For `terraform-review`: Validate, format, and plan Terraform or OpenTofu configurations. — decide which checks to run
- For `iac-scanning`: Scan IaC for misconfigurations with checkov, tfsec, and terrascan. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `infrastructure-as-code-devops` tools
- Tools: `Glob`, `Grep`, `Read`, `Terraform`, `Tofu` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `infrastructure-as-code-devops:4213ed57`

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