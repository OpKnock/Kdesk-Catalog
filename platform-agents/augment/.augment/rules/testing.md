---
type: agent_requested
description: "General testing workflow: plan, write, run, and report tests across languages with coverage and CI integration. Use when working with test planning, coverage and reports, ci integration, testing or when the user mentions test planning, coverage and reports, ci integration, testing."
---

General testing workflow: plan, write, run, and report tests across languages with coverage and CI integration.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `pytest --collect-only`, `pytest --cov=src --cov-report=xml`
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

**Parameters:**
- `framework` (string): Test framework: pytest, jest, go, mvn, dotnet
- `filter` (string): Expression filter for collected tests, e.g. -k for pytest.

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

**Parameters:**
- `coverageReport` (string): Coverage report format
- `threshold` (number): Coverage gate percentage

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

**Parameters:**
- `ciMode` (boolean): CI-friendly deterministic flags
- `junit` (string): Path for JUnit XML results output.

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

## References
- [pytest Documentation](https://docs.pytest.org/)
- [Jest Documentation](https://jestjs.io/docs/getting-started)
- [Go Testing](https://go.dev/doc/effective_go#testing)