---
name: "golangci-lint"
description: "Runs aggregated Go linting with golangci-lint: dozens of linters, fast parallel runs, config, and CI integration. Use when working with golangci run, golangci config, code quality or when the user mentions golangci run, golangci config, code quality."
license: "MIT"
compatibility: "Requires golangci-lint."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "code-quality"}
allowed-tools: "Glob Grep Read Bash(golangci-lint:*)"
---

Runs aggregated Go linting with golangci-lint: dozens of linters, fast parallel runs, config, and CI integration.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `golangci-lint run`, `golangci-lint linters`
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

# golangci-lint

Fast aggregated Go linting.

## When to Use

- Enforcing multiple linters with one command
- CI lint gates that stay fast
- Catching style, bugs, and security issues together
- Diff-only linting on PRs

## Commands

```bash
# Install
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest

# Run
golangci-lint run
golangci-lint run ./...
golangci-lint run --fix

# Only new issues on a PR
golangci-lint run --new-from-rev HEAD~1

# GitHub Actions output
golangci-lint run --out-format github-actions

# Fast mode (skip slower linters)
golangci-lint run --fast

# Inspect
golangci-lint linters
golangci-lint version
```

## Config Example

```yaml
# .golangci.yml
run:
  timeout: 5m
linters:
  enable:
    - errcheck
    - govet
    - staticcheck
    - gosec
    - revive
issues:
  exclude-rules:
    - path: _test\.go
      linters: [gosec]
```

## Best Practices

- Enable errcheck, govet, staticcheck, gosec at minimum
- Use --new-from-rev for PR-only findings
- Cache builds; golangci-lint caches by default
- Run --fix locally, verify-only in CI
- Keep the config in the repo for consistent runs
- Pin the golangci-lint version in CI

## Capabilities

### golangci-run
Run golangci-lint with linter selection.

**Parameters:**
- `paths` (string): Packages to lint
- `fix` (boolean): Apply fixes
- `out-format` (string): colored-line-number, github-actions, json

**Commands:**
- `golangci-lint run`
- `golangci-lint run ./...`
- `golangci-lint run --fix`
- `golangci-lint run --enable-all --max-issues-per-linter 0`
- `golangci-lint run --fast`

**Examples:**
- golangci-lint run --timeout 5m ./...
- golangci-lint run --new-from-rev HEAD~1
- golangci-lint run --out-format github-actions

### golangci-config
Manage linter configuration.

**Parameters:**
- `enable` (string): Linters to enable
- `disable` (string): Linters to disable

**Commands:**
- `golangci-lint linters`
- `golangci-lint version`
- `golangci-lint run --print-resources-usage`
- `golangci-lint cache clean`

**Examples:**
- golangci-lint linters | grep enabled
- golangci-lint run --disable errcheck

## References
- [golangci-lint Docs](https://golangci-lint.run)
- [golangci-lint on GitHub](https://github.com/golangci/golangci-lint)
