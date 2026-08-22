---
type: agent_requested
description: "Scans container images for vulnerabilities and supply-chain risks with Docker Scout, trivy, and grype, then hardens Dockerfiles."
---

# Container Security

Scans container images for vulnerabilities and supply-chain risks with Docker Scout, trivy, and grype, then hardens Dockerfiles.

## Instructions

# Container Security

Scan, triage, and harden container images across the delivery pipeline.

## What This Skill Does

- Scans images with Docker Scout, trivy, and grype
- Triages CVEs by severity, fixability, and exploitability
- Produces SARIF/JSON reports for CI and dashboards
- Reviews Dockerfiles for base-image, user, and layer hygiene
- Blocks deploys on critical unfixed CVEs

## When to Use

- Before pushing an image to production
- A CVE advisory hits a base image in use
- CI needs a container security gate

## Real Commands

```bash
# Docker Scout analysis
scout login
 docker scout quickview myapp:latest
docker scout cves myapp:latest --only-severity critical --only-fixed
docker scout recommendations myapp:latest

# Trivy
 trivy image --severity HIGH,CRITICAL --ignore-unfixed myapp:latest
trivy image -o scan.sarif -f sarif myapp:latest

# Grype
 grype myapp:latest --only-fixed

# Filesystem scan including secrets
trivy fs --scanners vuln,secret .
```

## Hardening Checklist

- Pin base image digests, not tags
- Run as a non-root user and drop capabilities
- Copy only build output; multi-stage builds shrink attack surface
- Scan the final image, not the build stage
- Keep a signed SBOM alongside each released image

## Best Practices

- Fail CI on CRITICAL unfixed CVEs; use --ignore-unfixed to focus on actionable
- Triage with Docker Scout's policy evaluation for package priorities
- Automate scanning at every image push, not just at release
- Pair scanning with runtime hardening (seccomp, read-only rootfs, non-root UID)

## Capabilities

### docker-scout
Analyze images with Docker Scout for CVEs and remediation guidance.

**Commands:**
- `docker scout quickview nginx:latest`
- `docker scout cves nginx:latest`
- `docker scout recommendations nginx:latest`
- `docker scout compare --to registry.local/app:old app:new`
- `docker scout cves nginx:latest --only-severity critical`

**Examples:**
- docker scout quickview myapp:latest
- docker scout cves myapp:latest --only-severity critical --only-fixed
- docker scout recommendations myapp:latest

### image-scanning
Scan images and filesystems with trivy and grype for CVE coverage.

**Commands:**
- `trivy image nginx:latest`
- `trivy image --severity CRITICAL --ignore-unfixed nginx:latest`
- `grype nginx:latest`
- `trivy fs --scanners vuln,secret .`
- `docker scan myapp:latest`

**Examples:**
- trivy image --severity HIGH,CRITICAL --ignore-unfixed myapp:latest
- grype --only-fixed myapp:latest
- docker scout cves myapp:latest --format sarif --output scout.sarif