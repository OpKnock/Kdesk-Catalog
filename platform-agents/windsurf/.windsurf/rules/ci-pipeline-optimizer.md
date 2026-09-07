---
trigger: glob
description: "Optimizes CI pipelines: caching, job parallelization, matrix builds, flaky test handling, and cost reduction on GitHub Actions and GitLab CI. Use when working with github actions, pipeline tuning or when the user mentions github actions, pipeline tuning."
globs: ["**/*.json", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

Optimizes CI pipelines: caching, job parallelization, matrix builds, flaky test handling, and cost reduction on GitHub Actions and GitLab CI.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `gh workflow run ci.yml`, `npm ci --cache .npm --prefer-offline`
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

# CI Pipeline Optimizer

Make CI fast, reliable, and cheap.

## When to Use

- Pipelines slower than 5 minutes on every push
- Flaky tests breaking merges
- High CI costs from repeated work
- Matrix builds that run identical work

## Strategies

- Cache dependencies (npm ci cache, pip cache, gradle build cache)
- Parallelize independent jobs and shard test suites
- Use matrix builds only for true configuration differences
- Split build vs test into separate stages/jobs
- Fix flaky tests instead of re-running them

## Commands

```bash
# GitHub Actions inspection
gh workflow run ci.yml
gh run list --workflow ci.yml --limit 10
gh run view 1234 --log-failed
gh cache list --json key,sizeInBytes
gh cache delete --all

# Caching and parallel tests
npm ci --cache .npm --prefer-offline
pytest -n auto
pytest -n 4 --dist=loadscope
mvn -T 4 test
gradle --build-cache test
```

## Caching Example

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('package-lock.json') }}
```

## Best Practices

- Target under 5 minutes for PR checks
- Shard unit tests by file or by load balance
- Retry only known flaky tests; quarantine the rest
- Cache keys must include lockfile hashes
- Fail fast: lint first, then unit tests, then e2e
- Cancel superseded runs to save parallel minutes

## Capabilities

### github-actions
Optimize GitHub Actions workflows.

**Parameters:**
- `workflow` (string): Workflow file name
- `run-id` (integer): Run id

**Commands:**
- `gh workflow run ci.yml`
- `gh run list`
- `gh run view --log-failed 1234`
- `gh cache list`
- `gh cache delete --all`

**Examples:**
- gh run list --workflow ci.yml --limit 10
- gh run view 1234 --log-failed | head -100
- gh cache list --json key,sizeInBytes

### pipeline-tuning
Cache deps, parallelize, and fix flaky tests.

**Parameters:**
- `parallelism` (integer): Parallel jobs
- `cache` (string): Cache strategy: npm, pip, gradle

**Commands:**
- `npm ci --cache .npm --prefer-offline`
- `pip cache dir`
- `pytest -n auto`
- `pytest --flaky -p no:cacheprovider`
- `gradle --build-cache test`

**Examples:**
- npm ci --cache .npm && npm cache verify
- pytest -n 4 --dist=loadscope
- mvn -T 4 test

## References
- [GitHub Actions Docs](https://docs.github.com/actions)
- [GitLab CI Docs](https://docs.gitlab.com/ci/)
