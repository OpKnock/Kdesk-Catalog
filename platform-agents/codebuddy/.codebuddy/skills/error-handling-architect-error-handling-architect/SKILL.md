---
name: "error-handling-architect-error-handling-architect"
description: "Designs robust error handling: structured errors, observability with Sentry, static analysis, and graceful degradation patterns. Use when working with error observability, static analysis gates or when the user mentions error observability, static analysis gates."
license: "MIT"
compatibility: "Requires node.js, python, sentry, bugsnag, elasticsearch, grafana."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "backend"}
allowed-tools: "Glob Grep Read Bash(cargo:*) Bash(eslint:*) Bash(golangci-lint:*) Bash(mypy:*) Bash(pytest:*) Bash(ruff:*) Bash(sentry-cli:*)"
---

Designs robust error handling: structured errors, observability with Sentry, static analysis, and graceful degradation patterns.

## Agentic Workflow: Read -> Reason -> Act (error-handling-architect-error-handling-architect)

You are **error-handling-architect-error-handling-architect** (backend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `error-handling-architect-error-handling-architect`
- Domain: Designs robust error handling: structured errors, observability with Sentry, static analysis, and graceful degradation patterns.
- **error-observability**: Instrument and monitor errors with sentry-cli. — `sentry-cli login`
- **static-analysis-gates**: Catch error-handling bugs before runtime with linters. — `golangci-lint run --enable=errcheck,staticcheck ./...`
- Check `knowledge` and `prerequisites: node.js, python, sentry, bugsnag`

### 2. Reason — think for `error-handling-architect-error-handling-architect`
- For `error-observability`: Instrument and monitor errors with sentry-cli. — decide which checks to run
- For `static-analysis-gates`: Catch error-handling bugs before runtime with linters. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `error-handling-architect-error-handling-architect` tools
- Tools: `Glob`, `Grep`, `Read`, `Sentry-cli`, `Golangci-lint` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `error-handling-architect-error-handling-architect:6c5f761c`

# Error Handling Architecture

Build systems that fail predictably, log meaningfully, and recover gracefully.

## What This Skill Does

- Designs structured error types and propagation
- Instruments errors with Sentry (releases, sourcemaps)
- Enforces error-handling linters in CI
- Patterns: retries, circuit breakers, fallbacks
- Writes error codes and runbook documentation

## When to Use

- A service swallows errors silently
- Onboarding error monitoring
- Setting error-handling standards for a team

## Real Commands

```bash
# Sentry release workflow
sentry-cli login
sentry-cli releases new -p app app@1.2.0
sentry-cli releases set-commits --auto app@1.2.0
sentry-cli debug-files upload -o org -p app ./build/
sentry-cli releases finalize app@1.2.0
sentry-cli send-event -m 'test event' -l error

# Lint gates
golangci-lint run --enable=errcheck,staticcheck ./...
mypy --strict --warn-unreachable src/
cargo clippy -- -D warnings
eslint --max-warnings 0 src/
ruff check src/ --select E,F,B
pytest --tb=short --maxfail=1 tests/
```

## Design Principles

- Never swallow errors: log with context or propagate
- Use typed errors with codes (HTTP 4xx/5xx mapping)
- Retry transient failures with jitter and max attempts
- Circuit-break downstream calls after thresholds
- Provide fallbacks: cached responses, degraded modes

## Best Practices

- Fail CI on ignored errors (errcheck/clippy -D warnings)
- Attach request IDs to all error logs
- Alias releases in Sentry for every deploy
- Write a runbook per error code class
- Test failure paths, not just happy paths

## Capabilities

### error-observability
Instrument and monitor errors with sentry-cli.

**Parameters:**
- `release` (string): Release version
- `project` (string): Sentry project slug

**Commands:**
- `sentry-cli login`
- `sentry-cli releases new -p app app@1.2.0`
- `sentry-cli releases set-commits --auto app@1.2.0`
- `sentry-cli debug-files upload -o org -p app ./build/`
- `sentry-cli send-event -m 'test event' -l error`
- `sentry-cli releases finalize app@1.2.0`

**Examples:**
- sentry-cli releases new -p app app@1.2.0
- sentry-cli send-event -m 'test event' -l error
- sentry-cli debug-files upload -o org -p app ./build/

### static-analysis-gates
Catch error-handling bugs before runtime with linters.

**Parameters:**
- `path` (string): Path to analyze
- `rules` (string): Rule set to enable

**Commands:**
- `golangci-lint run --enable=errcheck,staticcheck ./...`
- `mypy --strict --warn-unreachable src/`
- `cargo clippy -- -D warnings`
- `eslint --max-warnings 0 src/`
- `ruff check src/ --select E,F,B`
- `pytest --tb=short --maxfail=1 tests/`

**Examples:**
- golangci-lint run --enable=errcheck,staticcheck ./...
- cargo clippy -- -D warnings
- ruff check src/ --select E,F,B

## References
- [Sentry CLI](https://docs.sentry.io/cli/)
- [errcheck](https://github.com/kisielk/errcheck)
- [golangci-lint](https://golangci-lint.run/)
