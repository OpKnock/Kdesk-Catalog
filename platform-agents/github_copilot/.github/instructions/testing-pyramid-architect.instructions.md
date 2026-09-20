---
applyTo: "**/*.go **/*.json **/*.r **/*.rs **/*.sh **/*.{yaml,yml}"
---

# testing-pyramid-architect

Architects test strategies across the pyramid with tiered suites, coverage budgets, and CI orchestration.

## Instructions

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
