---
name: "testing-pyramid-architect"
description: "Architects test strategies across the pyramid with tiered suites, coverage budgets, and CI orchestration. Use when working with tier strategy, coverage budgets, ci orchestration or when the user mentions tier strategy, coverage budgets, ci orchestration."
globs: ["**/*.go", "**/*.json", "**/*.r", "**/*.rs", "**/*.sh", "**/*.{yaml,yml}"]
alwaysApply: false
---

Architects test strategies across the pyramid with tiered suites, coverage budgets, and CI orchestration.

## Agentic Workflow: Read -> Reason -> Act (testing-pyramid-architect)

You are **testing-pyramid-architect** (testing) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — testing context for `testing-pyramid-architect`
- Domain: Architects test strategies across the pyramid with tiered suites, coverage budgets, and CI orchestration.
- **tier-strategy**: Define and enforce tiered test suites. — `pytest tests/unit -n 4`
- **coverage-budgets**: Enforce coverage budgets per tier. — `pytest --cov=src --cov-fail-under=80 tests/unit`
- **ci-orchestration**: Orchestrate tiers across CI stages. — `npm run test:unit && npm run test:api`
- Check `knowledge` and `prerequisites: jest, pytest, cypress, playwright`

### 2. Reason — think for `testing-pyramid-architect`
- For `tier-strategy`: Define and enforce tiered test suites. — decide which checks to run
- For `coverage-budgets`: Enforce coverage budgets per tier. — decide which checks to run
- For `ci-orchestration`: Orchestrate tiers across CI stages. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `testing-pyramid-architect` tools
- Tools: `Glob`, `Grep`, `Read`, `Pytest`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `testing-pyramid-architect:02e38404`

# Testing Pyramid Architecture

Design test suites that are fast, trustworthy, and maintainable.

## What This Skill Does

- Defines unit/integration/E2E tiers with tools per tier
- Sets coverage budgets per tier
- Orchestrates CI stages for fast feedback
- Uses smoke tests and sharding to control runtime

## When to Use

- Redesigning a slow, all-E2E suite
- Onboarding testing standards for a team
- Balancing speed and confidence in CI

## Real Commands

```bash
# Tiers
pytest tests/unit -n 4
pytest tests/integration --cov=src
npx jest --testPathPattern=tests/unit
npx playwright test tests/e2e --grep @critical

# Budgets
pytest --cov=src --cov-fail-under=80 tests/unit
npx jest --coverage --coverageThreshold='{"global":{"lines":80}}'

# CI stages
npm run test:unit && npm run test:api
npx playwright test tests/e2e --shard=1/4
pytest -m smoke tests/
```

## Target Distribution

```text
Unit (60%):      jest/pytest/go test - ms feedback
Integration (30%): testcontainers/supertest - seconds
E2E (10%):      playwright/cypress - minutes
```

## CI Stage Design

```yaml
stages:
  unit:    pytest -n 4 tests/unit && npx jest tests/unit
  api:     pytest tests/integration && newman run collection.json
  e2e:     npx playwright test tests/e2e --shard=1/4
```

## Best Practices

- Push tests down the pyramid; E2E is the last resort
- Budgets per tier prevent coverage theater
- Run unit tests on every push; e2e on merge and nightly
- Shard E2E; keep each stage under 15 minutes
- Review the pyramid quarterly as the app evolves

## Capabilities

### tier-strategy
Define and enforce tiered test suites.

**Parameters:**
- `tier` (string): Tier directory: unit, integration, e2e
- `framework` (string): Framework per tier

**Commands:**
- `pytest tests/unit -n 4`
- `pytest tests/integration --cov=src`
- `npx jest --testPathPattern=tests/unit`
- `npx playwright test tests/e2e --grep @critical`
- `mvn verify -Dit.test=*IT`

**Examples:**
- pytest tests/unit -n 4
- npx jest --testPathPattern=tests/unit
- npx playwright test tests/e2e --grep @critical

### coverage-budgets
Enforce coverage budgets per tier.

**Parameters:**
- `threshold` (number): Minimum coverage percentage
- `covFailUnder` (number): pytest fail threshold

**Commands:**
- `pytest --cov=src --cov-fail-under=80 tests/unit`
- `npx jest --coverage --coverageThreshold='{"global":{"lines":80}}'`
- `go test -coverprofile=coverage.out ./... && awk '/total:/{print $3}' coverage.out`
- `dotnet test --collect:"XPlat Code Coverage" --threshold=80`

**Examples:**
- pytest --cov=src --cov-fail-under=80 tests/unit
- npx jest --coverage --coverageThreshold='{"global":{"lines":80}}'
- go test -coverprofile=coverage.out ./...

### ci-orchestration
Orchestrate tiers across CI stages.

**Parameters:**
- `stage` (string): CI stage for the tier
- `shards` (integer): Total shards for e2e parallelization, e.g. 4 for 1/4.

**Commands:**
- `npm run test:unit && npm run test:api`
- `pytest tests/unit -m 'not e2e'`
- `npx playwright test tests/e2e --shard=1/4`
- `pytest -m smoke tests/`
- `npx jest --ci --changedSince=main`

**Examples:**
- npm run test:unit && npm run test:api
- npx playwright test tests/e2e --shard=1/4
- pytest -m smoke tests/

## References
- [Test Pyramid - Martin Fowler](https://martinfowler.com/bliki/TestPyramid.html)
- [Google Testing Blog](https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html)
- [pyramid by Vladimir Khorikov](https://enterprisecraftsmanship.com/posts/test-pyramid-anti-patterns/)