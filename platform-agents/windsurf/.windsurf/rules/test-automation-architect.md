---
trigger: glob
description: "Designs and implements test automation strategies across unit, integration, and E2E layers with coverage gates and parallel execution. Use when working with pytest strategy, jest strategy, e2e strategy or when the user mentions pytest strategy, jest strategy, e2e strategy."
globs: ["**/*.html", "**/*.py", "**/*.r", "**/*.scala", "**/*.sh"]
---

Designs and implements test automation strategies across unit, integration, and E2E layers with coverage gates and parallel execution.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `pytest --maxfail=1 -q`, `npx jest --ci --coverage`
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

# Test Automation Architecture

Design scalable, reliable test suites across the pyramid.

## What This Skill Does

- Lays out unit/integration/E2E test structures
- Configures coverage gates and parallel execution
- Implements tagging for smoke vs full suites
- Handles flakiness with retries and sharding

## When to Use

- Setting up testing from scratch for a service
- Speeding up a slow test suite
- Enforcing coverage policies in CI

## Real Commands

```bash
# Python
pytest -n 4 --cov=src --cov-report=term-missing tests/
pytest --junitxml=results.xml

# Node
npx jest --ci --coverage --maxWorkers=50%
npx jest --projects src/api src/ui

# E2E
npx playwright test --project=chromium --grep @smoke
npx playwright test --shard=1/3 --retries=2 --reporter=html
```

## Pyramid Shape

```text
E2E:    10%  - Playwright, few, slow, business-critical
API:    30%  - supertest/pytest, fast, contract-level
Unit:   60%  - jest/pytest, instant, logic-level
```

## Best Practices

- Keep unit tests deterministic; no network or clocks
- Tag smoke tests and run them on every PR
- Shard E2E across CI runners to keep feedback fast
- Set coverage gates (e.g. 80% lines) that fail the build
- Treat flaky tests as defects: quarantine or fix, never ignore

## Capabilities

### pytest-strategy
Structure Python test suites with parallelism and coverage.

**Parameters:**
- `workers` (number): Parallel workers (-n)
- `coverage` (string): Package to measure coverage

**Commands:**
- `pytest --maxfail=1 -q`
- `pytest -n 4 tests/unit`
- `pytest --cov=src --cov-report=term-missing`
- `pytest --junitxml=results.xml`
- `pytest --lf --last-failed-no-failures=all`

**Examples:**
- pytest -n 4 --cov=src tests/
- pytest --junitxml=results.xml
- pytest --lf

### jest-strategy
Organize JS/TS unit and integration tests with jest.

**Parameters:**
- `maxWorkers` (string): Worker limit, e.g. 50% or 2
- `coverageThreshold` (object): Coverage gate config

**Commands:**
- `npx jest --ci --coverage`
- `npx jest --runInBand`
- `npx jest --maxWorkers=50%`
- `npx jest --projects src/api src/ui`
- `npx jest --silent --testPathIgnorePatterns=e2e`

**Examples:**
- npx jest --ci --coverage
- npx jest --maxWorkers=50%
- npx jest --projects src/api src/ui

### e2e-strategy
Orchestrate end-to-end suites with Playwright.

**Parameters:**
- `grep` (string): Tag or name filter, e.g. @smoke
- `shard` (string): Shard identifier, e.g. 1/3
- `retries` (number): Retry count for flaky tests

**Commands:**
- `npx playwright test --project=chromium`
- `npx playwright test --grep @smoke`
- `npx playwright test --workers=4`
- `npx playwright test --retries=2 --reporter=html`
- `npx playwright test --shard=1/3`

**Examples:**
- npx playwright test --grep @smoke
- npx playwright test --shard=1/3
- npx playwright test --retries=2

## References
- [pytest Documentation](https://docs.pytest.org/)
- [Jest Documentation](https://jestjs.io/docs/getting-started)
- [Playwright Test Docs](https://playwright.dev/docs/test-intro)
