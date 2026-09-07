---
trigger: glob
description: "Detects deprecated Kubernetes API versions in manifests and live clusters with Fairwinds Pluto, tracking removal schedules per version. Use when working with manifest scanning, cluster scanning, devops or when the user mentions manifest scanning, cluster scanning, devops."
globs: ["**/*.json", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

Detects deprecated Kubernetes API versions in manifests and live clusters with Fairwinds Pluto, tracking removal schedules per version.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `pluto detect-files -d ./deploy`, `pluto detect-kube-context`
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

# Pluto Deprecation Scanning

Find deprecated Kubernetes APIs before they are removed by the control plane.

## What This Skill Does

- Scans manifest directories for deprecated apiVersions
- Scans live clusters through kube context
- Scans Helm chart output for deprecations
- Reports removal versions and target-version checks
- Exits nonzero to fail CI on deprecations

## When to Use

- Before a Kubernetes upgrade (v1.22 -> v1.25 removed many APIs)
- CI gate to prevent deprecated API usage from merging
- Auditing Helm charts and vendored YAML

## Real Commands

```bash
# Files
pluto detect-files -d ./deploy
pluto detect-files -d . --output json
pluto detect-files -d . --target-versions k8s=v1.25.0
pluto detect-files --glob 'k8s/**/*.yaml'

# Cluster
pluto detect-kube-context
pluto detect-kube-context -o json
helm list -A -o json > /tmp/helm.json
pluto detect-helm -o json
pluto detect-all-in-cluster

# Reference
pluto list-versions
pluto version
```

## CI Gate

```bash
pluto detect-files -d ./deploy --output json | jq '.items | length'
# exit code 1 means deprecations found
```

## Best Practices

- Run pluto in every CI pipeline, fail on deprecated APIs
- Check `pluto list-versions` before planning cluster upgrades
- Migrate deprecated APIs in the same release as their removal target
- Scan Helm charts with detect-helm; charts mask deprecations otherwise
- Keep the pluto binary updated for the latest version matrix

## Capabilities

### manifest-scanning
Scan directory trees of YAML manifests for deprecated APIs.

**Parameters:**
- `dir` (string): Directory to scan
- `target-versions` (string): Target versions, e.g. k8s=v1.25.0
- `output` (string): Output format: normal, json, yaml

**Commands:**
- `pluto detect-files -d ./deploy`
- `pluto detect-files -d . --output json`
- `pluto detect-files -d . --ignore-deprecations`
- `pluto detect-files -d . --target-versions k8s=v1.25.0`
- `pluto detect-files --glob 'k8s/**/*.yaml'`

**Examples:**
- pluto detect-files -d ./deploy
- pluto detect-files -d . --output json
- pluto detect-files -d . --target-versions k8s=v1.25.0

### cluster-scanning
Scan live clusters for in-use deprecated APIs via helm output or kube context.

**Parameters:**
- `context` (string): Kube context to scan
- `output` (string): Output format

**Commands:**
- `pluto detect-kube-context`
- `pluto detect-kube-context -o json`
- `helm list -A -o json > /tmp/helm.json && pluto detect-helm -o json`
- `pluto detect-all-in-cluster`
- `pluto list-versions`

**Examples:**
- pluto detect-kube-context
- pluto detect-helm -o json
- pluto list-versions

## References
- [Pluto GitHub](https://github.com/FairwindsOps/pluto)
- [Fairwinds Deprecated API Policy](https://www.fairwinds.com/blog/deprecated-kubernetes-apis)
