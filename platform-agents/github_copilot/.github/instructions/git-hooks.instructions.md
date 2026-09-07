---
applyTo: "**/*.r **/*.sh **/*.{yaml,yml}"
---

Automates git hooks with pre-commit, Husky, and core.hooksPath: linting, formatting, secret scanning, and commit message checks.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `pre-commit install`, `npx husky init`
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
