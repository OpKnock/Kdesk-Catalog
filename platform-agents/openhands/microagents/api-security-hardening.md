---
name: "api-security-hardening"
description: "Hardens API deployments: container scanning with trivy, secret detection with gitleaks, dependency upgrades, and least-privilege configuration checks."
type: knowledge
triggers: ["api-security-hardening", "container-scanning", "secret-detection"]
---

# api-security-hardening

Hardens API deployments: container scanning with trivy, secret detection with gitleaks, dependency upgrades, and least-privilege configuration checks.

## Instructions

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
