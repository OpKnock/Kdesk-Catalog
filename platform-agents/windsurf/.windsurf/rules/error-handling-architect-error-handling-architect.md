---
trigger: glob
description: "Designs robust error handling: structured errors, observability with Sentry, static analysis, and graceful degradation patterns."
globs: ["**/*.go", "**/*.r", "**/*.sh"]
---

# error-handling-architect-error-handling-architect

Designs robust error handling: structured errors, observability with Sentry, static analysis, and graceful degradation patterns.

## Instructions

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
