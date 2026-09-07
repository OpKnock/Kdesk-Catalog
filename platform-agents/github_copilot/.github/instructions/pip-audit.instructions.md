---
applyTo: "**/*.json **/*.py **/*.r **/*.sh **/*.{yaml,yml}"
---

Audits Python environments and requirements files for known vulnerabilities with pip-audit.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `pip-audit`
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

# pip Audit

Audits Python packages for known vulnerabilities using the OSV database, covering
installed environments, requirements files, and lock files.

## When to Use

- Pre-release check of a Python app
- Scanning a requirements.txt before a Docker build
- CI security gate for Python projects

## Real Commands

```bash
# Install
pip install pip-audit

# Audit the current environment
pip-audit

# Audit a requirements file
pip-audit -r requirements.txt

# Audit only direct deps, skip editable installs
pip-audit -l --skip-editable --no-deps

# JSON output for CI
pip-audit -r requirements.txt --format json > audit.json

# Auto-fix by upgrading (review with --dry-run first)
pip-audit --fix -r requirements.txt --dry-run
pip-audit --fix -r requirements.txt
```

## Exit Codes

- `0` no vulnerabilities, `1` vulnerabilities found, `2` audit failed

## CI

```yaml
- name: pip audit
  run: pip-audit -r requirements.txt --no-deps
```

## Best Practices

- Use `--no-deps -r requirements.txt` in CI for speed and determinism
- Audit the lock file used by the deployment (constraints.txt / pip-tools output)
- Prefer `--fix` with `--dry-run` first, then run tests
- Pin pip-audit itself in CI

## Example Response

Lists each vulnerable package as `pkg==ver` with CVE ID, severity, and the patched
version; then proposes the upgrade command.

## Capabilities

### pip-audit
Scan installed or declared Python dependencies against the OSV database

**Parameters:**
- `format` (string): Output format: columns, json, cyclonedx-json, cyclonedx-xml, markdown
- `fix` (boolean): Attempt to fix vulnerabilities by upgrading packages
- `vuln-service` (string): Vulnerability service: osv or pypi

**Commands:**
- `pip-audit`
- `pip-audit -r requirements.txt`
- `pip-audit -l --format json`
- `pip-audit --fix`
- `pip-audit --skip-editable --no-deps`

**Examples:**
- pip-audit -r requirements.txt --format markdown
- pip-audit -l | grep -i critical
- pip-audit --fix --dry-run -r requirements.txt

## References
- [pip-audit GitHub](https://github.com/pypa/pip-audit)
- [pip-audit PyPI](https://pypi.org/project/pip-audit/)
