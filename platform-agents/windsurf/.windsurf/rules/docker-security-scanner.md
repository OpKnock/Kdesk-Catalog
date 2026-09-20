---
trigger: glob
description: "Scans container images, filesystems, IaC, and clusters for vulnerabilities with Trivy, Grype, Syft, and Docker Scout."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
---

# docker-security-scanner

Scans container images, filesystems, IaC, and clusters for vulnerabilities with Trivy, Grype, Syft, and Docker Scout.

## Instructions

# Container Security Scanning

Find vulnerabilities in images, code, and clusters before attackers do.

## What This Skill Does

- Scans images for OS and language CVEs (Trivy/Grype)
- Generates SBOMs with Syft
- Scans IaC, filesystems, and git repos
- Scans clusters with trivy k8s
- Emits SARIF/JSON for CI gates

## When to Use

- CI gate before image push
- Auditing running clusters
- Checking base image upgrades

## Real Commands

```bash
# Images
trivy image nginx:latest
trivy image --severity CRITICAL,HIGH --ignore-unfixed nginx:1.26
trivy image --format sarif -o results.sarif nginx:latest
docker scout cves nginx:latest
docker scout quickview nginx:latest
grype nginx:latest -o table

# Code and config
trivy fs --severity HIGH,CRITICAL .
trivy config --severity CRITICAL .
trivy repo --scanners vuln,secret git@github.com:org/app.git

# Clusters
trivy k8s --report summary cluster

# SBOM
syft nginx:latest -o spdx-json > sbom.json
trivy sbom sbom.json
```

## CI Gate Pattern

```bash
trivy image --exit-code 1 --severity CRITICAL --ignore-unfixed $IMAGE
```

## Best Practices

- Fail on CRITICAL with --ignore-unfixed to focus on fixable
- Track SBOMs per release for provenance
- Scan at build time and in nightly regressions
- Combine image scans with trivy k8s for runtime context
- Pin base images and rebuild on advisory updates

## Capabilities

### image-scanning
Scan container images for CVEs and misconfigurations.

**Commands:**
- `trivy image nginx:latest`
- `trivy image --severity CRITICAL,HIGH --ignore-unfixed nginx:1.26`
- `trivy image --format sarif -o results.sarif nginx:latest`
- `docker scout cves nginx:latest`
- `docker scout quickview nginx:latest`
- `grype nginx:latest -o table`

**Examples:**
- trivy image --severity CRITICAL,HIGH --ignore-unfixed nginx:1.26
- docker scout cves nginx:latest
- trivy image --format sarif -o results.sarif nginx:latest

### filesystem-and-ci
Scan repos, IaC, and Kubernetes clusters in pipelines.

**Commands:**
- `trivy fs --severity HIGH,CRITICAL .`
- `trivy config --severity CRITICAL .`
- `trivy repo --scanners vuln,secret git@github.com:org/app.git`
- `trivy k8s --report summary cluster`
- `syft nginx:latest -o spdx-json > sbom.json`
- `trivy sbom sbom.json`

**Examples:**
- trivy fs --severity HIGH,CRITICAL .
- trivy k8s --report summary cluster
- syft nginx:latest -o spdx-json > sbom.json
