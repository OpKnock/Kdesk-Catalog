---
type: agent_requested
description: "Scan directories or files across supported platforms. Emit reports and control exit codes handling CI integration. queries for cloud misconfigurations."
---

# kics

Scan directories or files across supported platforms. Emit reports and control exit codes handling CI integration. queries for cloud misconfigurations.

## Instructions

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