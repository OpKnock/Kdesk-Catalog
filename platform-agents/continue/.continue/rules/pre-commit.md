---
name: "pre-commit"
description: "Manages git hooks with pre-commit: installing hooks, running checks, and maintaining hook repos."
globs: ["**/*.py", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
alwaysApply: false
---

# pre-commit

Manages git hooks with pre-commit: installing hooks, running checks, and maintaining hook repos.

## Instructions

# Pre-commit

Framework for managing and maintaining multi-language git hooks, so every commit
runs the same checks as CI.

## When to Use

- Standardizing checks (lint, format, secrets) across a team
- Running Python and JS linters in one hook pipeline
- Keeping hooks versioned and shareable

## Real Commands

```bash
# Install the hooks into the repo
pre-commit install

# Run all hooks on everything (CI / after config change)
pre-commit run --all-files

# Run a single hook
pre-commit run ruff

# Run only against specific files
pre-commit run --files src/foo.py

# Update hook revisions
pre-commit autoupdate

# Validate the config file
pre-commit validate-config

# Clean cache when hooks misbehave
pre-commit clean
```

## Config (.pre-commit-config.yaml)

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: check-added-large-files
      - id: end-of-file-fixer
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

## CI

```yaml
- name: pre-commit
  run: |
    pip install pre-commit
    pre-commit run --all-files
```

## Best Practices

- Run `pre-commit autoupdate` monthly and commit the bumps
- Put the `pre-commit-ci` bot on PRs so hooks update automatically
- Use `--show-diff-on-failure` to see what hooks changed
- Keep fast hooks in pre-commit; move heavy suites to CI

## Example Response

After a failing commit, reports which hook failed, what it modified, and the exact
tail of the diff so the user can re-stage and commit.

## Capabilities

### pre-commit-hooks
Install, run, and manage pre-commit framework git hooks

**Commands:**
- `pre-commit install`
- `pre-commit run --all-files`
- `pre-commit autoupdate`
- `pre-commit run ruff --files src/`
- `pre-commit validate-config`

**Examples:**
- pre-commit run --all-files --show-diff-on-failure
- pre-commit run trailing-whitespace --files README.md
- pre-commit clean && pre-commit install-hooks