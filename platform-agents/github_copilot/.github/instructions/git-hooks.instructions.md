---
applyTo: "**/*.r **/*.sh **/*.{yaml,yml}"
---

Automates git hooks with pre-commit, Husky, and core.hooksPath: linting, formatting, secret scanning, and commit message checks.

## Agentic Workflow: Read -> Reason -> Act (git-hooks)

You are **git-hooks** (devtools/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devtools context for `git-hooks`
- Domain: Automates git hooks with pre-commit, Husky, and core.hooksPath: linting, formatting, secret scanning, and commit message checks.
- **pre-commit-framework**: Install and configure pre-commit hooks for Python/any-repo workflows. — `pre-commit install`
- **husky-and-custom-hooks**: Set up Husky hooks and custom scripts for Node projects. — `npx husky init`
- Check `knowledge` and `prerequisites: git, npx, pre-commit`

### 2. Reason — think for `git-hooks`
- For `pre-commit-framework`: Install and configure pre-commit hooks for Python/any-repo workflows. — decide which checks to run
- For `husky-and-custom-hooks`: Set up Husky hooks and custom scripts for Node projects. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `git-hooks` tools
- Tools: `Glob`, `Grep`, `Read`, `Pre-commit`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `git-hooks:f67ccaf7`

# Git Hooks Automation

Enforce code quality at commit time with git hooks.

## What This Skill Does

- Installs pre-commit framework hooks (lint, format, secrets)
- Configures Husky hooks for Node projects
- Adds commit-msg linting (conventional commits)
- Sets core.hooksPath for team-wide hooks
- Runs hooks across all files or changed files only

## When to Use

- Enforcing lint/format on every commit
- Blocking secrets and large files from entering history
- Standardizing commit message formats

## Real Commands

```bash
# pre-commit
pre-commit install
pre-commit install --hook-type pre-push
pre-commit run --all-files
pre-commit run ruff
pre-commit autoupdate
pre-commit uninstall

# Husky (Node)
npx husky init
npx husky add .husky/pre-commit 'npx lint-staged'
npx husky add .husky/commit-msg 'npx commitlint --edit $1'
git config core.hooksPath .husky
```

## .pre-commit-config.yaml Sketch

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: check-added-large-files
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.0
    hooks:
      - id: ruff
      - id: ruff-format
```

## Best Practices

- Keep hooks fast (<10s); slow hooks get bypassed
- Use pre-commit.ci to enforce on PRs without local installs
- Add secret scanning (gitleaks/trufflehog) as a hook
- Never use hooks for secrets or processes that belong in CI
- Version hook repos with rev pins, run autoupdate monthly

## Capabilities

### pre-commit-framework
Install and configure pre-commit hooks for Python/any-repo workflows.

**Parameters:**
- `hook` (string): Hook ID to run
- `hook-type` (string): Hook type to install, e.g. pre-push

**Commands:**
- `pre-commit install`
- `pre-commit install --hook-type pre-push`
- `pre-commit run --all-files`
- `pre-commit run ruff`
- `pre-commit autoupdate`
- `pre-commit uninstall`

**Examples:**
- pre-commit install
- pre-commit run --all-files
- pre-commit autoupdate

### husky-and-custom-hooks
Set up Husky hooks and custom scripts for Node projects.

**Parameters:**
- `hook-file` (string): Hook file path, e.g. .husky/pre-commit
- `command` (string): Command the hook runs

**Commands:**
- `npx husky init`
- `npx husky add .husky/pre-commit 'npx lint-staged'`
- `npx husky add .husky/commit-msg 'npx commitlint --edit $1'`
- `git config core.hooksPath .husky`
- `npx lint-staged`
- `git commit -m 'chore: trigger hooks'`

**Examples:**
- npx husky add .husky/pre-commit 'npx lint-staged'
- npx husky add .husky/commit-msg 'npx commitlint --edit $1'
- git config core.hooksPath .husky

## References
- [pre-commit Documentation](https://pre-commit.com/)
- [Git Hooks (git-scm)](https://git-scm.com/docs/githooks)
- [Husky](https://typicode.github.io/husky/)
- [commitlint](https://commitlint.js.org/)
