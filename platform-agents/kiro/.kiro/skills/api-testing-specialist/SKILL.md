---
name: "api-testing-specialist"
description: "Orchestrates API testing in CI: GitHub Actions workflows, local testing with act, test splitting, and result reporting to pull requests."
---

# api-testing-specialist

Orchestrates API testing in CI: GitHub Actions workflows, local testing with act, test splitting, and result reporting to pull requests.

## Instructions

# API Testing Specialist

CI orchestration for API tests.

## What This Skill Does
- Runs API tests in pipelines
- Replicates workflows locally
- Reports results to PRs

## When to Use
- New CI pipelines for APIs
- Debugging flaky CI runs
- Enforcing test gates

## Real Commands

```bash
gh workflow run api-tests.yml
gh run view --log-failed
act -l
act -W .github/workflows/api-tests.yml -j test
```

## Workflow Example

```yaml
name: api-tests
on: [push, workflow_dispatch]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npx jest --ci --coverage
```

## Testing
- Run act locally before pushing
- Split long suites across jobs
- Upload reports as artifacts


## Best Practices
- Cache dependencies in CI
- Pin action versions
- Fail fast on critical suites

## Capabilities

### ci-orchestration
Run API tests in GitHub Actions

**Commands:**
- `gh workflow run api-tests.yml`
- `gh run list --workflow=api-tests.yml --limit 5`
- `gh run view --log-failed`
- `gh run watch`

**Examples:**
- gh workflow run triggers tests on demand
- gh run view --log-failed shows failures
- gh run watch tails the run

### local-execution
Run CI workflows locally with act

**Commands:**
- `act -l`
- `act -W .github/workflows/api-tests.yml`
- `act -W .github/workflows/api-tests.yml -j test`
- `act --secret-file .secrets --pull=false`

**Examples:**
- -cli --help
- -api --help
