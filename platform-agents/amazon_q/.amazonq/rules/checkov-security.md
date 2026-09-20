Scans Terraform, CloudFormation, Kubernetes, Dockerfile, and other IaC for misconfigurations with 1000+ built-in policies and SARIF/JUnit output.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `checkov -d .`, `checkov -d . -o sarif --output-file-path scan.sarif`
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

# Checkov

Static analysis for infrastructure-as-code with a broad policy library.

## What This Skill Does

- Scans Terraform, CloudFormation, Kubernetes, Helm, Dockerfile, Bicep, ARM, and secrets
- Fails CI on HIGH/CRITICAL misconfigurations
- Outputs SARIF for GitHub code scanning and JUnit XML for CI dashboards
- Supports custom policies written in Python or YAML
- Skips noisy checks while tracking baseline suppressions

## When to Use

- Pre-merge IaC review for cloud misconfigurations
- Container image and Dockerfile security scanning
- Compliance evidence for CIS and cloud best-practice baselines

## Real Commands

```bash
# Full recursive scan
checkov -d .

# Framework-scoped, quiet, compact
checkov -d terraform/ --framework terraform --quiet --compact

# Single file
checkov -f main.tf

# SARIF for GitHub code scanning
checkov -d . -o sarif --output-file-path results/

# JUnit XML for CI
checkov -d . -o junitxml --output-file-path test-results/

# Skip a known-false-positive
checkov -d . --skip-check CKV_AWS_123

# Only high severity and soft-fail in dev
checkov -d . --skip-check CKV_AWS_* --soft-fail --quiet
```

## Custom Policy (YAML)

```yaml
metadata:
  id: CKV2_CUSTOM_001
  name: No public S3 buckets
category: S3
check:
  - resource_types:
      - aws_s3_bucket
    conditions:
      - cond_type: attribute
        resource_types: [aws_s3_bucket]
        attribute: acl
        operator: not_equals
        value: public-read
```

## Best Practices

- Scan at PR time, not just nightly, to catch drift early
- Use --compact and --quiet to keep logs actionable
- Route SARIF output to GitHub code scanning for inline annotations
- Exclude the .terraform directory unless reviewing modules
- Track suppressions in checkov's baseline file to make them reviewable

## Capabilities

### iac-scanning
Scan directories, files, and frameworks for policy violations.

**Parameters:**
- `directory` (string): Root directory to scan recursively
- `framework` (string): Framework filter: terraform, cloudformation, kubernetes, dockerfile, secrets, all
- `check` (string): Comma-separated check IDs to include or skip

**Commands:**
- `checkov -d .`
- `checkov -f main.tf`
- `checkov -d . --framework terraform`
- `checkov -d . --skip-check CKV_AWS_123`
- `checkov -d . --check CKV_AWS_* --compact`

**Examples:**
- checkov -d terraform/ --framework terraform
- checkov -f kubernetes/deployment.yaml --framework kubernetes
- checkov -d . --check CKV_AWS_126

### reporting
Emit reports in CI-friendly formats and enforce severity gates.

**Parameters:**
- `output` (string): Output format: cli, json, sarif, junitxml, github_failed_only
- `softFail` (boolean): Return exit code 0 even if checks fail

**Commands:**
- `checkov -d . -o sarif --output-file-path scan.sarif`
- `checkov -d . -o junitxml --output-file-path reports/`
- `checkov -d . --soft-fail --skip-framework secrets`
- `checkov -d . --quiet`

**Examples:**
- checkov -d . -o sarif --output-file-path results/scan.sarif
- checkov -d . -o junitxml --output-file-path test-results/
- checkov -d . --soft-fail

## References
- [Checkov Documentation](https://www.checkov.io/)
- [Checkov GitHub](https://github.com/bridgecrewio/checkov)