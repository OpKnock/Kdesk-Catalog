---
name: "api-testing-specialist"
description: "Orchestrates API testing in CI: GitHub Actions workflows, local testing with act, test splitting, and result reporting to pull requests. Use when working with ci orchestration, local execution or when the user mentions ci orchestration, local execution."
license: "MIT"
compatibility: "Requires jest, pytest, postman, newman, supertest, rest-assured."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "testing"}
allowed-tools: "Glob Grep Read Bash(act:*) Bash(gh:*)"
---

Orchestrates API testing in CI: GitHub Actions workflows, local testing with act, test splitting, and result reporting to pull requests.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `gh workflow run api-tests.yml`, `act -l`
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

**Parameters:**
- `workflow` (string): Workflow file name
- `ref` (string): Branch or tag
- `inputs` (object): Workflow dispatch inputs

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

## References
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [act Docs](https://github.com/nektos/act)
