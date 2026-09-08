---
name: "api-security-hardening"
description: "Hardens API deployments: container scanning with trivy, secret detection with gitleaks, dependency upgrades, and least-privilege configuration checks. Use when working with container scanning, secret detection or when the user mentions container scanning, secret detection."
---

Hardens API deployments: container scanning with trivy, secret detection with gitleaks, dependency upgrades, and least-privilege configuration checks.

## Agentic Workflow: Read -> Reason -> Act (api-security-hardening)

You are **api-security-hardening** (security) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — security context for `api-security-hardening`
- Domain: Hardens API deployments: container scanning with trivy, secret detection with gitleaks, dependency upgrades, and least-privilege configuration checks.
- **container-scanning**: Scan container images and filesystems for vulnerabilities — `trivy image --severity HIGH,CRITICAL myapi:1.0.0`
- **secret-detection**: Detect leaked secrets in repositories — `gitleaks detect -v`
- Check `knowledge` and `prerequisites: node.js, python, owasp-zap, burp-suite`

### 2. Reason — think for `api-security-hardening`
- For `container-scanning`: Scan container images and filesystems for vulnerabilities — decide which checks to run
- For `secret-detection`: Detect leaked secrets in repositories — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-security-hardening` tools
- Tools: `Glob`, `Grep`, `Read`, `Trivy`, `Gitleaks` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-security-hardening:92d1d92e`

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
