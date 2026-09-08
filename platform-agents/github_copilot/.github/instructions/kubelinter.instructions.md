---
applyTo: "**/*.json **/*.r **/*.sh **/*.{yaml,yml}"
---

Lints Kubernetes manifests with KubeLinter: security, best-practice, and reliability checks with config-driven rules.

## Agentic Workflow: Read -> Reason -> Act (kubelinter)

You are **Kubelinter** (code-quality/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — code-quality context for `kubelinter`
- Domain: Lints Kubernetes manifests with KubeLinter: security, best-practice, and reliability checks with config-driven rules.
- **kubelinter-scan**: Scan manifests and directories. — `kubelinter lint deploy.yaml`
- **kubelinter-config**: Customize checks and policies. — `kubelinter lint --list-checks`
- Check `knowledge` and `prerequisites: kubelinter`

### 2. Reason — think for `kubelinter`
- For `kubelinter-scan`: Scan manifests and directories. — decide which checks to run
- For `kubelinter-config`: Customize checks and policies. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `kubelinter` tools
- Tools: `Glob`, `Grep`, `Read`, `Kubelinter` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `kubelinter:cf5b5ac5`

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
