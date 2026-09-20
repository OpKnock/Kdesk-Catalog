---
type: agent_requested
description: "Scans codebases for high-entropy strings and known secret patterns, maintaining a reviewed baseline to prevent secret leaks in CI."
---

# detect-secrets

Scans codebases for high-entropy strings and known secret patterns, maintaining a reviewed baseline to prevent secret leaks in CI.

## Instructions

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

**Commands:**
- `detect-secrets audit .secrets.baseline`
- `detect-secrets-hook --baseline .secrets.baseline .env`
- `git diff | detect-secrets-hook --baseline .secrets.baseline --stdin`
- `pre-commit install`

**Examples:**
- detect-secrets audit .secrets.baseline
- git diff | detect-secrets-hook --baseline .secrets.baseline --stdin
- pre-commit run --all-files