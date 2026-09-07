Scan directories, files, and modules against policy packs. Emit reports and apply automatic fixes.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `terrascan init`, `terrascan scan -d . -o sarif`
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

# Terrascan

Static IaC security scanning with deep cloud policy coverage.

## What This Skill Does

- Scans Terraform, Kubernetes, Helm, and cloudformation
- Applies 1500+ policies across AWS, Azure, GCP
- Auto-fixes supported violations with --fix
- Emits SARIF/JSON/HTML reports for CI

## When to Use

- Terraform module review before merge
- Cloud misconfiguration auditing at scale
- Kubernetes manifest checks with a single tool

## Real Commands

```bash
# First-time policy download
terrascan init

# Scans
terrascan scan -d .
terrascan scan -f main.tf
terrascan scan -d . --policy-type aws --severity high

# Reports
terrascan scan -d . -o sarif --output-file scan.sarif
terrascan scan -d . -o json --output-file results.json

# Fixes and exclusions
terrascan scan -d . --fix
terrascan scan -d . --skip-rules AWS.S3Bucket.DS.High.1043
```

## Best Practices

- Run terrascan init in CI before scanning
- Scan modules and root configs separately for clarity
- Review auto-fixes (--fix) before merging
- Skip rules with a documented reason, tracked in a config file
- Combine with checkov for overlapping but complementary coverage

## Capabilities

### terrascan-scan
Scan directories, files, and modules against policy packs.

**Parameters:**
- `directory` (string): Directory to scan recursively
- `file` (string): Single file to scan
- `policyType` (string): Cloud policy type: aws, azure, gcp, k8s

**Commands:**
- `terrascan init`
- `terrascan scan -d .`
- `terrascan scan -f main.tf`
- `terrascan scan -i terraform`
- `terrascan scan -d . --policy-type aws`

**Examples:**
- terrascan init && terrascan scan -d .
- terrascan scan -f main.tf -i terraform
- terrascan scan -d . --policy-type aws --severity high

### reporting-and-fixing
Emit reports and apply automatic fixes.

**Parameters:**
- `output` (string): Format: yaml, json, xml, html, sarif
- `fix` (boolean): Auto-fix supported violations
- `skipRules` (array): Rule IDs to skip

**Commands:**
- `terrascan scan -d . -o sarif`
- `terrascan scan -d . -o json --output-file results.json`
- `terrascan scan -d . --fix`
- `terrascan scan -d . --skip-rules AWS.S3Bucket.DS.High.1043`
- `terrascan scan -d . --severity critical`

**Examples:**
- terrascan scan -d . -o sarif --output-file scan.sarif
- terrascan scan -d . --fix
- terrascan scan -d . --skip-rules AWS.S3Bucket.DS.High.1043

## References
- [Terrascan Documentation](https://docs.tenable.com/terrascan/)
- [Terrascan GitHub](https://github.com/tenable/terrascan)