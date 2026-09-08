---
name: "kics"
description: "Scan directories or files across supported platforms. Emit reports and control exit codes handling CI integration. queries for cloud misconfigurations. Use when working with kics scan, reporting and gating, security or when the user mentions kics scan, reporting and gating, security."
---

Scan directories or files across supported platforms. Emit reports and control exit codes handling CI integration. queries for cloud misconfigurations.

## Agentic Workflow: Read -> Reason -> Act (kics)

You are **kics** (security/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — security context for `kics`
- Domain: Scan directories or files across supported platforms. Emit reports and control exit codes handling CI integration. queries for cloud misconfigurations.
- **kics-scan**: Scan directories or files across supported platforms. — `kics scan -p .`
- **reporting-and-gating**: Emit reports and control exit codes for CI integration. — `kics scan -p . -o results.json --output-path results/`
- Check `knowledge` and `prerequisites: kics`

### 2. Reason — think for `kics`
- For `kics-scan`: Scan directories or files across supported platforms. — decide which checks to run
- For `reporting-and-gating`: Emit reports and control exit codes for CI integration. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `kics` tools
- Tools: `Glob`, `Grep`, `Read`, `Kics` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `kics:a886eb7e`

# KICS

Keep Infrastructure as Code Secure with static query scanning.

## What This Skill Does

- Scans Terraform, Kubernetes, Docker, Ansible, CloudFormation, and more
- Applies 2000+ security, compliance, and best-practice queries
- Emits SARIF, JSON, HTML, and GitLab SAST reports
- Supports custom query packs written in Rego-like syntax

## When to Use

- Pre-merge IaC misconfiguration checks
- Multi-platform IaC repos where one tool should cover everything
- Compliance evidence for CSPM baselines

## Real Commands

```bash
# Basic scan
kics scan -p .

# Platform-scoped scan
kics scan -p terraform/ -i terraform
kics scan -p k8s/ -i kubernetes

# Custom queries and exclusions
kics scan -p . -q ./custom-queries
kics scan -p . --exclude-queries 0684d1ba-9253-4bc1-8f1f-6d1c8e8b5e00

# Reports
kics scan -p . --report-formats json,sarif --output-path ./reports

# CI gating
kics scan -p . --fail-on high
```

## Best Practices

- Pin KICS version in CI to keep query results stable
- Start with --fail-on high and relax after reviewing noise
- Track exclusions in config rather than hiding output
- Feed SARIF into GitHub code scanning for inline PR annotations
- Pair with runtime scanning (Falco/Gatekeeper) for defense in depth

## Capabilities

### kics-scan
Scan directories or files across supported platforms.

**Parameters:**
- `path` (string): Path to scan (file or directory)
- `inputType` (string): IaC type: terraform, dockerfile, kubernetes, ansible, cloudformation
- `queries` (string): Custom queries path

**Commands:**
- `kics scan -p .`
- `kics scan -p terraform/ -i terraform`
- `kics scan -p Dockerfile -q ./queries`
- `kics scan -p . --exclude-queries 0684d1ba-9253-4bc1-8f1f-6d1c8e8b5e00`
- `kics scan -p . --ignore-on-exit results`

**Examples:**
- kics scan -p .
- kics scan -p terraform/ -i terraform
- kics scan -p k8s/ -i kubernetes

### reporting-and-gating
Emit reports and control exit codes for CI integration.

**Parameters:**
- `output` (string): Report format: json, sarif, html, glsast
- `failOn` (string): Exit nonzero on findings at or above severity: low, medium, high, critical

**Commands:**
- `kics scan -p . -o results.json --output-path results/`
- `kics scan -p . -o sarif`
- `kics scan -p . --report-formats json,html`
- `kics list-platforms`
- `kics scan -p . --disable-full-descriptions`

**Examples:**
- kics scan -p . --report-formats json,sarif --output-path ./reports
- kics scan -p . --fail-on high
- kics list-platforms

## References
- [KICS Documentation](https://docs.kics.io/)
- [KICS GitHub](https://github.com/Checkmarx/kics)
