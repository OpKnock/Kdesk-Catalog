---
type: agent_requested
description: "Lints Kubernetes manifests with KubeLinter: security, best-practice, and reliability checks with config-driven rules. Use when working with kubelinter scan, kubelinter config, code quality or when the user mentions kubelinter scan, kubelinter config, code quality."
---

Lints Kubernetes manifests with KubeLinter: security, best-practice, and reliability checks with config-driven rules.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `kubelinter lint deploy.yaml`, `kubelinter lint --list-checks`
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

# KubeLinter

Lint Kubernetes YAML for security and reliability.

## When to Use

- Scanning manifests before apply or deploy
- CI gates on configuration drift
- Enforcing security defaults (non-root, read-only fs)
- Auditing existing cluster manifests

## Commands

```bash
# Lint a file or directory
kubelinter lint deploy.yaml
kubelinter lint k8s/

# Custom config
kubelinter lint --config .kubelinter.yaml deploy.yaml

# Fail on warnings
kubelinter lint --fail-on warning deploy.yaml

# Reports
kubelinter lint --format json -o report.json k8s/
kubelinter lint --format sarif -o report.sarif k8s/

# Check selection
kubelinter lint --list-checks
kubelinter lint --disable-checks privileged-containers deploy.yaml
kubelinter lint --only-checks no-read-only-root-fs deploy.yaml
```

## Config Example

```yaml
# .kubelinter.yaml
checks:
  addAllBuiltIn: true
  doNotAutoAddDefaults: false
  exclude:
    - privileged-containers
```

## Best Practices

- Run kubelinter in CI before every deploy
- Enable run-as-non-root and no-read-only-root-fs checks
- Use --fail-on error for blockers, warning for review
- Generate SARIF for GitHub Code Scanning
- Keep the config in the repo for consistency
- Review default checks before disabling any

## Capabilities

### kubelinter-scan
Scan manifests and directories.

**Parameters:**
- `paths` (string): Files or directories
- `fail-on` (string): warning, error
- `format` (string): text, json, sarif

**Commands:**
- `kubelinter lint deploy.yaml`
- `kubelinter lint k8s/`
- `kubelinter lint --config .kubelinter.yaml deploy.yaml`
- `kubelinter lint --fail-on warning deploy.yaml`
- `kubelinter lint --format json -o report.json k8s/`

**Examples:**
- kubelinter lint --fail-on error k8s/
- kubelinter lint --format sarif -o report.sarif k8s/
- kubelinter lint --default-checks k8s/

### kubelinter-config
Customize checks and policies.

**Parameters:**
- `checks` (string): Comma-separated checks
- `config` (string): Config file path

**Commands:**
- `kubelinter lint --list-checks`
- `kubelinter lint --disable-checks privileged-containers deploy.yaml`
- `kubelinter lint --only-checks no-read-only-root-fs deploy.yaml`
- `kubelinter version`

**Examples:**
- kubelinter lint --list-checks | grep -i "privileged"
- kubelinter lint --only-checks run-as-non-root deploy.yaml

## References
- [KubeLinter Docs](https://docs.kubelinter.io)
- [KubeLinter on GitHub](https://github.com/stackrox/kube-linter)