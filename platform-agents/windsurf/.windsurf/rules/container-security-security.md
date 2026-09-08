---
trigger: glob
description: "Scans container images for vulnerabilities and supply-chain risks with Docker Scout, trivy, and grype, then hardens Dockerfiles. Use when working with docker scout, image scanning, security or when the user mentions docker scout, image scanning, security."
globs: ["**/*.json", "**/*.r", "**/*.sh", "**/Dockerfile*"]
---

Scans container images for vulnerabilities and supply-chain risks with Docker Scout, trivy, and grype, then hardens Dockerfiles.

## Agentic Workflow: Read -> Reason -> Act (container-security-security)

You are **Container Security** (security/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — security context for `container-security-security`
- Domain: Scans container images for vulnerabilities and supply-chain risks with Docker Scout, trivy, and grype, then hardens Dockerfiles.
- **docker-scout**: Analyze images with Docker Scout for CVEs and remediation guidance. — `docker scout quickview nginx:latest`
- **image-scanning**: Scan images and filesystems with trivy and grype for CVE coverage. — `trivy image nginx:latest`
- Check `knowledge` and `prerequisites: docker, grype, trivy`

### 2. Reason — think for `container-security-security`
- For `docker-scout`: Analyze images with Docker Scout for CVEs and remediation guidance. — decide which checks to run
- For `image-scanning`: Scan images and filesystems with trivy and grype for CVE coverage. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `container-security-security` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Trivy` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `container-security-security:724885cd`

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

**Parameters:**
- `image` (string): Image reference, e.g. nginx:latest
- `severity` (string): Minimum severity filter: low, medium, high, critical

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

**Parameters:**
- `image` (string): Image to scan
- `scanners` (array): trivy scanner types: vuln, secret, config, license

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

## References
- [Docker Scout Documentation](https://docs.docker.com/scout/)
- [Trivy Documentation](https://trivy.dev/)
- [Grype GitHub](https://github.com/anchore/grype)
