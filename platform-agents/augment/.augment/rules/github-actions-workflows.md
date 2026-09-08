---
type: agent_requested
description: "CI/CD with GitHub Actions: run workflows locally with act, manage secrets and runners via gh, and debug workflow runs. Use when working with actions workflows, api or when the user mentions actions workflows, api."
---

CI/CD with GitHub Actions: run workflows locally with act, manage secrets and runners via gh, and debug workflow runs.

## Agentic Workflow: Read -> Reason -> Act (github-actions-workflows)

You are **Github Actions Workflows** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `github-actions-workflows`
- Domain: CI/CD with GitHub Actions: run workflows locally with act, manage secrets and runners via gh, and debug workflow runs.
- **actions-workflows**: Run, validate, and debug GitHub Actions workflows. — `gh workflow run ci.yml --ref main`
- Check `knowledge` and `prerequisites: act`

### 2. Reason — think for `github-actions-workflows`
- For `actions-workflows`: Run, validate, and debug GitHub Actions workflows. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `github-actions-workflows` tools
- Tools: `Glob`, `Grep`, `Read`, `Gh`, `Act` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `github-actions-workflows:1d92e0e2`

# GitHub Actions v2

## What this skill does

GitHub Actions automates CI/CD from .github/workflows/*.yml. The gh CLI triggers and inspects runs; act executes workflows locally; secrets are managed per repo/environment.

## When to use

- Triggering and monitoring pipeline runs
- Reproducing a failing job locally with act
- Managing secrets and environments

## Real commands

```bash
# Trigger a workflow
 gh workflow run ci.yml --ref main

# Watch the run
 gh run list --workflow=ci.yml --limit=5
 gh run watch $(gh run list -w ci.yml -L 1 --json databaseId -q '.[0].databaseId')

# Run locally with act
 act -W .github/workflows/ci.yml --pull=false

# Download artifacts
 gh run download $(gh run list -w ci.yml -L 1 --json databaseId -q '.[0].databaseId') -n artifacts

# Secrets
 gh secret set DEPLOY_TOKEN --body=secret123
 gh secret list
```

## Workflow example

```yaml
name: ci
on:
  push:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npm test
```

## Testing

```bash
# Debug expressions locally
 gh workflow run ci.yml --ref main --json '{"debug":true}'
# Inspect failure logs
 gh run view $(gh run list -w ci.yml -L 1 --json databaseId -q '.[0].databaseId') --log-failed | head -50
```

## Best practices

- Pin action versions by tag/commit; never @main for third parties.
- Use `actions/cache` for dependency caches across runs.
- Store secrets in GitHub, never inline in YAML.
- Validate YAML locally with act before pushing.
- Use concurrency groups to cancel stale duplicate runs.

## Capabilities

### actions-workflows
Run, validate, and debug GitHub Actions workflows.

**Parameters:**
- `workflow-file` (string): Workflow YAML path like .github/workflows/ci.yml
- `ref` (string): Branch or tag to run the workflow on
- `secret-name` (string): Repository secret to set

**Commands:**
- `gh workflow run ci.yml --ref main`
- `gh run list --workflow=ci.yml --limit=5`
- `gh run watch $(gh run list -w ci.yml -L 1 --json databaseId -q '.[0].databaseId')`
- `act -W .github/workflows/ci.yml --pull=false`
- `gh run download $(gh run list -w ci.yml -L 1 --json databaseId -q '.[0].databaseId') -n artifacts`
- `gh secret set DEPLOY_TOKEN --body=secret123`

**Examples:**
- gh workflow run ci.yml --ref main && gh run watch
- act -W .github/workflows/ci.yml --pull=false
- gh run download $(gh run list -w ci.yml -L 1 --json databaseId -q '.[0].databaseId') -n artifacts

## References
- [GitHub Actions docs](https://docs.github.com/en/actions)
- [act](https://github.com/nektos/act)