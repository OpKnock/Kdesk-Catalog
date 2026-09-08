---
name: "regression-testing"
description: "Expert reference using pytest focused reruns, flaky test triage, git bisect to locate bug introduction, and CI gating with JUnit XML reports. Use when working with regression guard, api or when the user mentions regression guard, api."
license: "MIT"
compatibility: "Requires git, pytest."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(git:*) Bash(pytest:*)"
---

Expert reference using pytest focused reruns, flaky test triage, git bisect to locate bug introduction, and CI gating with JUnit XML reports.

## Agentic Workflow: Read -> Reason -> Act (regression-testing)

You are **Regression Testing** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `regression-testing`
- Domain: Expert reference using pytest focused reruns, flaky test triage, git bisect to locate bug introduction, and CI gating with JUnit XML reports.
- **regression-guard**: Find and prevent regressions with pytest and git bisect — `pytest tests/ -q`
- Check `knowledge` and `prerequisites: git, pytest`

### 2. Reason — think for `regression-testing`
- For `regression-guard`: Find and prevent regressions with pytest and git bisect — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `regression-testing` tools
- Tools: `Glob`, `Grep`, `Read`, `Pytest`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `regression-testing:8cd2d2ed`

# Regression Testing

Expert skill for catching and diagnosing regressions in API codebases.

## What this skill does

- Runs the full suite and reruns only last-failed tests after a fix
- Isolates tests with -k expressions for fast local iteration
- Uses git bisect to pinpoint the commit that introduced a regression

## When to use

- A feature change broke unrelated behavior
- A flaky test is blocking CI
- You need to identify exactly which commit broke an endpoint

## Real commands

```bash
# Full suite, quiet
pytest tests/ -q

# Rerun only the tests that failed last time
pytest tests/ --lf --tb=short

# Targeted subset with JUnit output for CI
pytest tests/ -k 'auth or billing' --junitxml=report.xml

# Slowest tests to spot perf regressions
pytest tests/ --durations=10 -q

# Find the breaking commit
git bisect start
git bisect bad            # current HEAD is broken
git bisect good v1.2.0    # this tag was fine
git bisect run pytest tests/ -q
```

## Flaky test triage

```bash
# Repeat a single test many times
pytest tests/test_auth.py::test_login -x --count=20
```

## Testing in CI

```yaml
- name: Regression suite
  run: pytest tests/ -q --junitxml=junit.xml --maxfail=3
```

## Best practices

- Keep the suite green on main; --lf makes local reruns fast
- JUnit XML lets CI dashboards track flakiness over time
- Automate git bisect with `git bisect run` so no manual builds are needed

## Capabilities

### regression-guard
Find and prevent regressions with pytest and git bisect

**Parameters:**
- `last_failed` (boolean): pytest --lf: only rerun tests that failed last run
- `junitxml` (string): Path to write JUnit XML for CI
- `expression` (string): pytest -k expression to select tests

**Commands:**
- `pytest tests/ -q`
- `pytest tests/ --lf --tb=short`
- `pytest tests/ -k 'auth or billing' --junitxml=report.xml`
- `git bisect start && git bisect bad && git bisect good v1.2.0`
- `git log --oneline -15`

**Examples:**
- pytest tests/ --lf -x
- git bisect run pytest tests/ -q
- pytest tests/ --durations=10 -q

## References
- [pytest usage docs](https://docs.pytest.org/en/stable/how-to/usage.html)
- [git bisect docs](https://git-scm.com/docs/git-bisect)
