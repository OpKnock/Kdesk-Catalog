---
trigger: glob
description: "Audits Python environments and requirements files for known vulnerabilities with pip-audit."
globs: ["**/*.json", "**/*.py", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

# Pip Audit

Audits Python environments and requirements files for known vulnerabilities with pip-audit.

## Instructions

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
