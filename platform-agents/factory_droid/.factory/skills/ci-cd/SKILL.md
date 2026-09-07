---
name: "ci-cd"
description: "Sets up and maintains CI/CD pipelines with GitHub Actions and GitLab CI, including workflow authoring, secrets handling, and run debugging. Use when working with github actions, gitlab ci, devops or when the user mentions github actions, gitlab ci, devops."
license: "MIT"
compatibility: "Requires actionlint, glab."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "devops"}
allowed-tools: "Glob Grep Read Bash(actionlint:*) Bash(gh:*) Bash(glab:*)"
---

Sets up and maintains CI/CD pipelines with GitHub Actions and GitLab CI, including workflow authoring, secrets handling, and run debugging.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `gh workflow list`, `glab ci status`
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

# CI/CD Pipeline Engineering

Design, author, and debug continuous integration and delivery pipelines for GitHub Actions and GitLab CI.

## What This Skill Does

- Writes valid `.github/workflows/*.yml` and `.gitlab-ci.yml` configs
- Validates pipeline syntax locally before pushing
- Debugs failing runs using the gh and glab CLIs
- Manages environment secrets, caches, and artifact passing between jobs
- Implements caching, matrix builds, and deployment gates

## When to Use

- A user asks to set up CI for a repository
- A pipeline run fails and needs diagnosis
- Adding deploy steps, artifact publishing, or test coverage gates

## Real Commands

```bash
# Validate workflows before pushing (GitHub)
actionlint .github/workflows/deploy.yml
actionlint -shellcheck= /usr/bin/shellcheck -pyflakes= /usr/bin/pyflakes .github/workflows/*.yml

# Trigger and watch runs (GitHub)
gh workflow run deploy.yml -f environment=staging --ref main
gh run list --workflow=deploy.yml --limit 5
gh run watch 4473148674
gh run view 4473148674 --log-failed

# Validate and run (GitLab)
glab ci lint .gitlab-ci.yml
glab pipeline run -b main
glab ci trace 2846210
glab ci retry 2846210
```

## Sample Workflow

```yaml
name: deploy
on:
  push:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: npm }
      - run: npm ci && npm test
      - uses: actions/upload-artifact@v4
        with: { name: dist, path: dist/ }
  deploy:
    needs: test
    runs-on: ubuntu-latest
    environment: staging
    env:
      STAGING_TOKEN: ${{ secrets.STAGING_TOKEN }}
    steps:
      - run: ./deploy.sh
```

## Best Practices

- Pin action versions to full SHAs in security-sensitive repos
- Use `needs` for job ordering and `if:` guards for conditional steps
- Pass artifacts between jobs with upload/download-artifact
- Cache package managers (npm, pip, maven) with `cache` inputs
- Put long-lived credentials in repository secrets, never in workflow YAML
- Fail fast: keep each job under ~10 minutes and parallelize with matrix

## Capabilities

### github-actions
Create, trigger, and inspect GitHub Actions workflows via the gh CLI and YAML configs.

**Parameters:**
- `workflow` (string): Workflow file name or ID to run, e.g. deploy.yml
- `run-id` (string): Workflow run ID for inspection (gh run view)
- `inputs` (object): Key-value inputs passed with -f, e.g. environment=staging

**Commands:**
- `gh workflow list`
- `gh workflow run deploy.yml -f environment=staging`
- `gh run list --limit 10`
- `gh run watch 1234567890`
- `gh run view 1234567890 --log-failed`
- `actionlint .github/workflows/deploy.yml`

**Examples:**
- gh workflow run release.yml -f version=1.2.3
- gh run view 4473148674 --log-failed
- actionlint .github/workflows/*.yml

### gitlab-ci
Manage GitLab CI pipelines, runners, and pipeline schedules.

**Parameters:**
- `pipeline-id` (string): Pipeline ID to trace, retry, or inspect
- `branch` (string): Branch to run the pipeline on

**Commands:**
- `glab ci status`
- `glab ci lint .gitlab-ci.yml`
- `glab pipeline run`
- `glab ci trace 1234567`
- `glab runner list`
- `glab ci retry 1234567`

**Examples:**
- glab ci lint .gitlab-ci.yml
- glab pipeline run -b main
- glab ci trace 2846210

## References
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitLab CI/CD Documentation](https://docs.gitlab.com/ci/)
- [actionlint](https://github.com/rhysd/actionlint)
