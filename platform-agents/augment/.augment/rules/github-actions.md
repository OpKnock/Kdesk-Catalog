---
type: agent_requested
description: "Author, validate, and operate GitHub Actions: workflow YAML, secrets, self-hosted runners, and run inspection via gh and actionlint. Use when working with workflow authoring, run operations, secrets and runners, devops or when the user mentions workflow authoring, run operations, secrets and runners, devops."
---

Author, validate, and operate GitHub Actions: workflow YAML, secrets, self-hosted runners, and run inspection via gh and actionlint.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `actionlint .github/workflows/*.yml`, `gh workflow run ci.yml -f environment=staging`
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