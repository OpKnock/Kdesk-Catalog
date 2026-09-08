---
name: "detect-secrets"
description: "Scans codebases for high-entropy strings and known secret patterns, maintaining a reviewed baseline to prevent secret leaks in CI. Use when working with baseline scanning, audit and hooks, security or when the user mentions baseline scanning, audit and hooks, security."
globs: ["**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
alwaysApply: false
---

Scans codebases for high-entropy strings and known secret patterns, maintaining a reviewed baseline to prevent secret leaks in CI.

## Agentic Workflow: Read -> Reason -> Act (detect-secrets)

You are **detect-secrets** (security/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — security context for `detect-secrets`
- Domain: Scans codebases for high-entropy strings and known secret patterns, maintaining a reviewed baseline to prevent secret leaks in CI.
- **baseline-scanning**: Scan repositories and manage the .secrets.baseline allowlist. — `detect-secrets scan . > .secrets.baseline`
- **audit-and-hooks**: Audit findings, resolve them as true/false positives, and run pre-commit hooks. — `detect-secrets audit .secrets.baseline`
- Check `knowledge` and `prerequisites: detect-secrets, detect-secrets-hook, git, pre-commit`

### 2. Reason — think for `detect-secrets`
- For `baseline-scanning`: Scan repositories and manage the .secrets.baseline allowlist. — decide which checks to run
- For `audit-and-hooks`: Audit findings, resolve them as true/false positives, and run pre-commit hooks. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `detect-secrets` tools
- Tools: `Glob`, `Grep`, `Read`, `Detect-secrets`, `Detect-secrets-hook` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `detect-secrets:391b7d79`

# detect-secrets

Find and manage secrets in code with entropy detection and baseline workflows.

## What This Skill Does

- Scans for AWS keys, tokens, private keys, and high-entropy strings
- Generates a reviewed baseline so legacy findings are tracked, not hidden
- Runs as a pre-commit hook to block new secrets
- Audits findings interactively and updates the baseline

## When to Use

- Onboarding a repo that may contain committed secrets
- Enforcing a no-secrets-in-diffs policy in CI
- Investigating a potential secret leak

## Real Commands

```bash
# Initial baseline
cd repo
detect-secrets scan . > .secrets.baseline

# Audit the baseline (mark true/false positives)
detect-secrets audit .secrets.baseline

# CI: fail only on NEW secrets
detect-secrets scan --baseline .secrets.baseline .

# Pre-commit hook on staged content
pre-commit install
git diff | detect-secrets-hook --baseline .secrets.baseline --stdin

# Update baseline after removing a secret
detect-secrets scan --update .secrets.baseline
```

## .pre-commit-config.yaml

```yaml
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.5.0
    hooks:
      - id: detect-secrets
        args: ["--baseline", ".secrets.baseline"]
```

## Best Practices

- Never delete the baseline without auditing it first
- Rotate any secret that already leaked before removing it from the repo
- Keep the hook fast by excluding vendored code and generated files
- Run a full scan in CI weekly, hook on every commit
- Audit with two reviewers for new baselines in sensitive repos

## Capabilities

### baseline-scanning
Scan repositories and manage the .secrets.baseline allowlist.

**Parameters:**
- `baseline` (string): Path to the baseline JSON file
- `excludeFiles` (string): Regex of files to exclude

**Commands:**
- `detect-secrets scan . > .secrets.baseline`
- `detect-secrets scan --baseline .secrets.baseline .`
- `detect-secrets scan --exclude-files 'tests/*' .`
- `detect-secrets scan --update .secrets.baseline`

**Examples:**
- detect-secrets scan . > .secrets.baseline
- detect-secrets scan --baseline .secrets.baseline .
- detect-secrets scan --update .secrets.baseline

### audit-and-hooks
Audit findings, resolve them as true/false positives, and run pre-commit hooks.

**Parameters:**
- `stdin` (boolean): Read content from stdin (used with git diff)
- `baseline` (string): Baseline file used by the hook

**Commands:**
- `detect-secrets audit .secrets.baseline`
- `detect-secrets-hook --baseline .secrets.baseline .env`
- `git diff | detect-secrets-hook --baseline .secrets.baseline --stdin`
- `pre-commit install`

**Examples:**
- detect-secrets audit .secrets.baseline
- git diff | detect-secrets-hook --baseline .secrets.baseline --stdin
- pre-commit run --all-files

## References
- [detect-secrets GitHub](https://github.com/Yelp/detect-secrets)
- [pre-commit Framework](https://pre-commit.com/)