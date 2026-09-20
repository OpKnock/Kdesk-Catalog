# Golangci Lint

Runs aggregated Go linting with golangci-lint: dozens of linters, fast parallel runs, config, and CI integration.

## Instructions

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

**Commands:**
- `golangci-lint linters`
- `golangci-lint version`
- `golangci-lint run --print-resources-usage`
- `golangci-lint cache clean`

**Examples:**
- golangci-lint linters | grep enabled
- golangci-lint run --disable errcheck