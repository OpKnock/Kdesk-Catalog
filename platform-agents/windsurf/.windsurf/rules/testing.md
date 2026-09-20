---
trigger: glob
description: "General testing workflow: plan, write, run, and report tests across languages with coverage and CI integration."
globs: ["**/*.go", "**/*.html", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

# testing

General testing workflow: plan, write, run, and report tests across languages with coverage and CI integration.

## Instructions

# Testing Workflows

Plan, run, and report tests across any stack.

## What This Skill Does

- Discovers and scopes test suites per framework
- Runs tests with filters, parallel workers, and CI flags
- Measures coverage with framework-native tools
- Produces JUnit/XML/HTML artifacts

## When to Use

- Setting up testing from scratch
- Standardizing CI test steps across services
- Debugging why suites fail in CI

## Real Commands

```bash
# Discover
pytest --collect-only
npx jest --listTests
dotnet test --list-tests

# Run
pytest -n 4 --junitxml=results.xml
npx jest --ci --coverage --maxWorkers=50%
go test -race ./...
mvn -B verify

# Coverage
pytest --cov=src --cov-report=xml
npx jest --coverage --coverageReporters=lcov
go test -coverprofile=coverage.out ./... && go tool cover -func=coverage.out
```

## CI Gate Template

```yaml
test:
  steps:
    - run: pytest -n 4 --cov=src --junitxml=results.xml
    - run: npx jest --ci --coverage --maxWorkers=50%
    - run: go test -race -coverprofile=coverage.out ./...
```

## Best Practices

- Fail fast locally (-x / --maxfail=1)
- Gate merges on coverage thresholds
- Run unit tests on PRs, full suites nightly
- Archive test reports as CI artifacts
- Fix flakes at the source with retries as a stopgap

## Capabilities

### test-planning
Discover test structure and configuration.

**Commands:**
- `pytest --collect-only`
- `npx jest --listTests`
- `go test -list . ./...`
- `mvn test -Dtest='*Test' -DskipTests=false -q test-compile`
- `dotnet test --list-tests`

**Examples:**
- pytest --collect-only
- npx jest --listTests
- dotnet test --list-tests

### coverage-and-reports
Measure coverage and produce reports.

**Commands:**
- `pytest --cov=src --cov-report=xml`
- `npx jest --coverage --coverageReporters=lcov`
- `go test -coverprofile=coverage.out ./... && go tool cover -func=coverage.out`
- `mvn verify jacoco:report`
- `dotnet test --collect:"XPlat Code Coverage"`

**Examples:**
- pytest --cov=src --cov-report=xml
- npx jest --coverage --coverageReporters=lcov
- go test -coverprofile=coverage.out ./... && go tool cover -func=coverage.out

### ci-integration
Run suites in CI with gates and retries.

**Commands:**
- `npm ci && npm test -- --ci`
- `pytest -n 4 --junitxml=results.xml`
- `npx jest --ci --coverage --maxWorkers=50%`
- `mvn -B verify -DskipITs=false`
- `go test -race ./...`

**Examples:**
- npm ci && npm test -- --ci
- pytest -n 4 --junitxml=results.xml
- go test -race ./...
