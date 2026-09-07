Hardens API deployments: container scanning with trivy, secret detection with gitleaks, dependency upgrades, and least-privilege configuration checks.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `trivy image --severity HIGH,CRITICAL myapi:1.0.0`, `gitleaks detect -v`
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

# API Security Hardening

Hardening scans for API deployments.

## What This Skill Does
- Scans images and repos for vulnerabilities
- Detects secrets before merge
- Validates infrastructure config

## When to Use
- Pre-production hardening gates
- Rotation and exposure audits
- Container supply-chain checks

## Real Commands

```bash
trivy image --severity HIGH,CRITICAL myapi:1.0.0
trivy fs --severity HIGH,CRITICAL .
gitleaks detect -v
gitleaks protect -v
```

## Hardening Checklist
- No critical CVEs in base images
- No secrets in git history
- Least-privilege IAM/roles
- Immutable image tags

## Testing
- Fail CI on critical findings
- Verify secret rotation after leaks
- Scan the lockfile changes in PRs

## Best Practices
- Scan images at build time
- Use distroless base images
- Enforce gitleaks on pre-commit

## Capabilities

### container-scanning
Scan container images and filesystems for vulnerabilities

**Parameters:**
- `target` (string): Image name or path
- `severity` (string): Severity filter
- `exit-code` (integer): Fail threshold

**Commands:**
- `trivy image --severity HIGH,CRITICAL myapi:1.0.0`
- `trivy image --ignore-unfixed --exit-code 1 --severity CRITICAL myapi:1.0.0`
- `trivy fs --severity HIGH,CRITICAL .`
- `trivy config --exit-code 1 Dockerfile`
- `trivy image --format sarif -o trivy.sarif myapi:1.0.0`

**Examples:**
- trivy image scans OS and app dependencies
- --exit-code 1 fails CI on findings
- --format sarif exports to code scanning

### secret-detection
Detect leaked secrets in repositories

**Commands:**
- `gitleaks detect -v`
- `gitleaks detect --report-format json --report-path gitleaks.json`
- `gitleaks detect --source . --no-git`
- `gitleaks protect -v`

**Examples:**
- -cli --help
- -api --help

## References
- [Trivy Docs](https://aquasecurity.github.io/trivy/)
- [Gitleaks](https://github.com/gitleaks/gitleaks)