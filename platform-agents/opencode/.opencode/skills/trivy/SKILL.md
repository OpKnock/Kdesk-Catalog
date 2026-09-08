---
name: "trivy"
description: "Scan images, directories, and repos handling vulnerabilities and secrets. Scan IaC configs and manage SBOMs. Scan Kubernetes clusters handling vulnerabilities and misconfigs. IaC misconfigs, and licenses with Trivy. Use when working with image and fs scan, config and sbom, cluster scan, security or when the user mentions image and fs scan, config and sbom, cluster scan, security."
---

Scan images, directories, and repos handling vulnerabilities and secrets. Scan IaC configs and manage SBOMs. Scan Kubernetes clusters handling vulnerabilities and misconfigs. IaC misconfigs, and licenses with Trivy.

## Agentic Workflow: Read -> Reason -> Act (trivy)

You are **trivy** (security/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — security context for `trivy`
- Domain: Scan images, directories, and repos handling vulnerabilities and secrets. Scan IaC configs and manage SBOMs. Scan Kubernetes clusters handling vulnerabilities and misconfigs. IaC misconfigs, and licen
- **image-and-fs-scan**: Scan images, directories, and repos for vulnerabilities and secrets. — `trivy image nginx:latest`
- **config-and-sbom**: Scan IaC configs and manage SBOMs. — `trivy config .`
- **cluster-scan**: Scan Kubernetes clusters for vulnerabilities and misconfigs. — `trivy kubernetes --report summary cluster`
- Check `knowledge` and `prerequisites: trivy`

### 2. Reason — think for `trivy`
- For `image-and-fs-scan`: Scan images, directories, and repos for vulnerabilities and secrets. — decide which checks to run
- For `config-and-sbom`: Scan IaC configs and manage SBOMs. — decide which checks to run
- For `cluster-scan`: Scan Kubernetes clusters for vulnerabilities and misconfigs. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `trivy` tools
- Tools: `Glob`, `Grep`, `Read`, `Trivy` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `trivy:bf32a219`

# Trivy

Comprehensive scanner: images, filesystems, repos, configs, and clusters.

## What This Skill Does

- Scans container images for CVEs with SBOM awareness
- Scans filesystems for secrets, licenses, and misconfigs
- Scans Kubernetes clusters for posture issues
- Generates SBOMs and SARIF reports

## When to Use

- Image gate before deploy
- Repo-wide secret and dependency scan
- Cluster security posture reviews

## Real Commands

```bash
# Images
 trivy image nginx:latest
trivy image --severity HIGH,CRITICAL --ignore-unfixed myapp:latest
trivy image --format sarif -o scan.sarif myapp:latest

# Filesystems and repos
trivy fs --scanners vuln,secret,config .
trivy repo https://github.com/org/repo

# Configs (IaC)
trivy config terraform/

# SBOM
 trivy image --format cyclonedx -o sbom.cdx.json myapp:latest
 trivy sbom sbom.cdx.json

# Kubernetes
 trivy kubernetes --report summary cluster
trivy kubernetes cluster --severity HIGH,CRITICAL
```

## CI Gate

```yaml
- name: Trivy image scan
  run: |
    trivy image --exit-code 1 --severity CRITICAL --ignore-unfixed myapp:latest
```

## Best Practices

- Use --ignore-unfixed to focus on actionable findings
- Set --exit-code 1 with severity gates in CI
- Run secret scans on every commit; image scans on every tag
- Schedule DB updates and pin trivy versions for stable results
- Generate SBOMs at build time for later re-scanning

## Capabilities

### image-and-fs-scan
Scan images, directories, and repos for vulnerabilities and secrets.

**Parameters:**
- `target` (string): Image, directory, or repo URL to scan
- `scanners` (array): Scan types: vuln, secret, config, license
- `severity` (string): Minimum severity: LOW, MEDIUM, HIGH, CRITICAL

**Commands:**
- `trivy image nginx:latest`
- `trivy image --severity HIGH,CRITICAL --ignore-unfixed nginx:latest`
- `trivy fs --scanners vuln,secret,config .`
- `trivy repo https://github.com/org/repo`
- `trivy image --format sarif -o scan.sarif nginx:latest`

**Examples:**
- trivy image --severity HIGH,CRITICAL --ignore-unfixed myapp:latest
- trivy fs --scanners secret .
- trivy repo https://github.com/org/repo --scanners vuln

### config-and-sbom
Scan IaC configs and manage SBOMs.

**Parameters:**
- `sbomFormat` (string): SBOM format: cyclonedx, spdx
- `output` (string): Output file path

**Commands:**
- `trivy config .`
- `trivy config --severity CRITICAL terraform/`
- `trivy sbom --sbom-format cyclonedx sbom.cdx.json`
- `trivy image --format cyclonedx -o sbom.cdx.json nginx:latest`
- `trivy image --ignore-unfixed --list-all-pkgs nginx:latest`

**Examples:**
- trivy config terraform/
- trivy image --format cyclonedx -o sbom.cdx.json nginx:latest
- trivy sbom sbom.cdx.json

### cluster-scan
Scan Kubernetes clusters for vulnerabilities and misconfigs.

**Parameters:**
- `report` (string): Report scope: summary, all
- `skipImages` (boolean): Skip image scanning in cluster scans

**Commands:**
- `trivy kubernetes --report summary cluster`
- `trivy kubernetes cluster --severity HIGH,CRITICAL`
- `trivy kubernetes --report all --format sarif -o k8s.sarif`
- `trivy k8s --skip-images deployment/myapp`

**Examples:**
- trivy kubernetes --report summary cluster
- trivy kubernetes cluster --severity HIGH,CRITICAL
- trivy k8s --skip-images deployment/myapp

## References
- [Trivy Documentation](https://trivy.dev/)
- [Trivy GitHub](https://github.com/aquasecurity/trivy)
