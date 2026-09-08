Scan directories, files, and modules against policy packs. Emit reports and apply automatic fixes.

## Agentic Workflow: Read -> Reason -> Act (terrascan)

You are **terrascan** (security/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — security context for `terrascan`
- Domain: Scan directories, files, and modules against policy packs. Emit reports and apply automatic fixes.
- **terrascan-scan**: Scan directories, files, and modules against policy packs. — `terrascan init`
- **reporting-and-fixing**: Emit reports and apply automatic fixes. — `terrascan scan -d . -o sarif`
- Check `knowledge` and `prerequisites: terrascan`

### 2. Reason — think for `terrascan`
- For `terrascan-scan`: Scan directories, files, and modules against policy packs. — decide which checks to run
- For `reporting-and-fixing`: Emit reports and apply automatic fixes. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `terrascan` tools
- Tools: `Glob`, `Grep`, `Read`, `Terrascan` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `terrascan:c0af20d9`

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
