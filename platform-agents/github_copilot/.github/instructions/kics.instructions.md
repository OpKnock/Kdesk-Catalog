---
applyTo: "**/*.go **/*.html **/*.json **/*.r **/*.sh **/*.tf **/Dockerfile*"
---

Scan directories or files across supported platforms. Emit reports and control exit codes handling CI integration. queries for cloud misconfigurations.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `kics scan -p .`, `kics scan -p . -o results.json --output-path results/`
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
