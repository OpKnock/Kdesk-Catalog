---
type: agent_requested
description: "Author, validate, and operate GitHub Actions: workflow YAML, secrets, self-hosted runners, and run inspection via gh and actionlint. Use when working with workflow authoring, run operations, secrets and runners, devops or when the user mentions workflow authoring, run operations, secrets and runners, devops."
---

Author, validate, and operate GitHub Actions: workflow YAML, secrets, self-hosted runners, and run inspection via gh and actionlint.

## Agentic Workflow: Read -> Reason -> Act (github-actions)

You are **github-actions** (devops/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devops context for `github-actions`
- Domain: Author, validate, and operate GitHub Actions: workflow YAML, secrets, self-hosted runners, and run inspection via gh and actionlint.
- **workflow-authoring**: Create and validate workflow files with correct syntax and events. — `actionlint .github/workflows/*.yml`
- **run-operations**: Trigger runs, watch them live, and fetch failed logs. — `gh workflow run ci.yml -f environment=staging`
- **secrets-and-runners**: Manage repository secrets and self-hosted runner registration. — `gh secret set AWS_ACCESS_KEY_ID --body "value"`
- Check `knowledge` and `prerequisites: ./config.sh, actionlint`

### 2. Reason — think for `github-actions`
- For `workflow-authoring`: Create and validate workflow files with correct syntax and events. — decide which checks to run
- For `run-operations`: Trigger runs, watch them live, and fetch failed logs. — decide which checks to run
- For `secrets-and-runners`: Manage repository secrets and self-hosted runner registration. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `github-actions` tools
- Tools: `Glob`, `Grep`, `Read`, `Actionlint`, `Gh` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `github-actions:36810de0`

# GitHub Actions Engineering

Build, validate, and operate CI/CD on GitHub Actions.

## What This Skill Does

- Writes workflow YAML with correct triggers, jobs, and expressions
- Validates syntax locally with actionlint
- Triggers, watches, reruns, and debugs runs with gh
- Manages secrets, variables, environments, and runners
- Hardens workflows against injection and secret leaks

## When to Use

- Setting up CI/CD in a GitHub repo
- A workflow run failed and needs diagnosis
- Registering self-hosted runners for specific hardware

## Real Commands

```bash
# Author + validate
actionlint .github/workflows/ci.yml
yq '.on' .github/workflows/ci.yml

# Run operations
gh workflow run ci.yml -f environment=staging --ref main
gh run list --limit 10
gh run watch 4473148674 --exit-status
gh run view 4473148674 --log-failed
gh run rerun 4473148674 --failed
gh run cancel 4473148674

# Secrets / vars / runners
gh secret set DEPLOY_TOKEN --body "s3cr3t"
gh secret list
gh variable set IMAGE_TAG --body "1.2.0"
gh runner list
./config.sh --url https://github.com/org/repo --token <token> --labels prod
```

## Workflow Template

```yaml
name: ci
on:
  push: { branches: [main] }
  pull_request:
permissions:
  contents: read
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: npm }
      - run: npm ci && npm test
```

## Best Practices

- Pin actions to SHAs or major versions; audit third-party actions
- Set `permissions:` at top level to least privilege
- Never echo secrets; use env passthrough with masking
- Use `gh run watch --exit-status` in CI scripts
- Validate with actionlint in a pre-commit hook or a lint job

## Capabilities

### workflow-authoring
Create and validate workflow files with correct syntax and events.

**Parameters:**
- `workflow` (string): Workflow file name
- `owner-repo` (string): owner/repo for gh api calls

**Commands:**
- `actionlint .github/workflows/*.yml`
- `gh workflow list`
- `gh workflow disable ci.yml`
- `gh api repos/{owner}/{repo}/actions/workflows --paginate`
- `yq '.on' .github/workflows/ci.yml`

**Examples:**
- actionlint .github/workflows/deploy.yml
- gh workflow list --all
- gh api repos/{owner}/{repo}/actions/workflows

### run-operations
Trigger runs, watch them live, and fetch failed logs.

**Parameters:**
- `run-id` (string): Workflow run ID
- `inputs` (object): workflow_dispatch inputs via -f

**Commands:**
- `gh workflow run ci.yml -f environment=staging`
- `gh run list --workflow=ci.yml --limit 5`
- `gh run watch demo-run-id --exit-status`
- `gh run view demo-run-id --log-failed`
- `gh run rerun demo-run-id --failed`
- `gh run cancel demo-run-id`

**Examples:**
- gh workflow run ci.yml -f environment=staging
- gh run view 4473148674 --log-failed
- gh run rerun 4473148674 --failed

### secrets-and-runners
Manage repository secrets and self-hosted runner registration.

**Parameters:**
- `name` (string): Secret or variable name
- `body` (string): Secret value

**Commands:**
- `gh secret set AWS_ACCESS_KEY_ID --body "value"`
- `gh secret list`
- `gh variable set MY_VAR --body "value"`
- `gh runner list`
- `./config.sh --url https://github.com/org/repo --token demo-token --labels prod,arm64`
- `gh api repos/{owner}/{repo}/actions/runners`

**Examples:**
- gh secret set DEPLOY_TOKEN --body "s3cr3t"
- gh secret list
- gh runner list

## References
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [actionlint](https://github.com/rhysd/actionlint)
- [gh CLI Manual](https://cli.github.com/manual/)