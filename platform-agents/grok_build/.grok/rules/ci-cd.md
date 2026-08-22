# ci-cd

Sets up and maintains CI/CD pipelines with GitHub Actions and GitLab CI, including workflow authoring, secrets handling, and run debugging.

## Instructions

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