---
applyTo: "**/*.html **/*.json **/*.r **/*.sh **/*.{yaml,yml}"
---

# kubescape

Scans Kubernetes clusters, manifests, and images against NSA/CISA, MITRE, and other hardening frameworks with kubescape.

## Instructions

# Kubescape

Kubernetes posture scanning against industry hardening frameworks.

## What This Skill Does

- Scans live clusters, manifests, and images
- Checks against NSA/CISA, MITRE ATT&CK, and CIS frameworks
- Reports compliance scores per control
- Exports SARIF, JSON, HTML, and JUnit for CI

## When to Use

- Cluster hardening baseline before production
- Compliance gate in CI for manifest changes
- Image scanning before deployment

## Real Commands

```bash
# Framework scans
kubescape scan framework nsa
kubescape scan framework all --verbose
kubescape scan framework mitre-attack

# Manifest and image scans
kubescape scan workload nginx.yaml
kubescape scan image ubuntu:latest
kubescape scan framework nsa --file-path manifests/

# Downloads and reports
kubescape download framework nsa
kubescape scan framework nsa --format sarif --output scan.sarif
kubescape scan framework nsa --format html --output report.html
```

## CI Gate

```yaml
- name: Kubescape scan
  run: |
    kubescape scan framework nsa --file-path . --format sarif --output scan.sarif \
      --set-exit-code 3 --fail-threshold 80
```

## Best Practices

- Run live scans after upgrades; manifest scans on every PR
- Start with the NSA framework, add MITRE for threat mapping
- Use --fail-threshold as a compliance score gate, not hard deny
- Store SARIF in code scanning for inline findings
- Remediate by control: RBAC, resource limits, and securityContext first

## Capabilities

### framework-scans
Scan clusters or files against security frameworks.

**Commands:**
- `kubescape scan framework nsa`
- `kubescape scan framework all`
- `kubescape scan framework mitre-attack`
- `kubescape scan framework cis-aks-t1.2.0`
- `kubescape scan framework nsa --verbose`

**Examples:**
- kubescape scan framework nsa
- kubescape scan framework all
- kubescape scan framework mitre-attack --verbose

### workload-and-image-scan
Scan manifest files and container images directly.

**Commands:**
- `kubescape scan workload nginx.yaml`
- `kubescape scan image ubuntu:latest`
- `kubescape scan framework nsa --file-path manifests/`
- `kubescape download framework nsa`

**Examples:**
- kubescape scan workload deploy.yaml
- kubescape scan image nginx:1.25
- kubescape download framework cis-eks-t1.2.0

### reporting
Export scan results in CI and audit formats.

**Commands:**
- `kubescape scan framework nsa --format sarif --output scan.sarif`
- `kubescape scan framework all --format json --output scan.json`
- `kubescape scan framework nsa --format html --output report.html`
- `kubescape scan framework nsa --set-exit-code 3 --fail-threshold 70`

**Examples:**
- kubescape scan framework nsa --format sarif --output scan.sarif
- kubescape scan framework nsa --format html --output report.html
- kubescape scan framework all --set-exit-code 3 --fail-threshold 80
