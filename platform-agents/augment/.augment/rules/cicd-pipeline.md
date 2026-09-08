---
type: agent_requested
description: "Designs pipeline-as-code flows, runs CI locally with act, and enforces pipeline quality gates with linters and security scanners. Use when working with local pipeline runtime, pipeline quality gates, devops or when the user mentions local pipeline runtime, pipeline quality gates, devops."
---

Designs pipeline-as-code flows, runs CI locally with act, and enforces pipeline quality gates with linters and security scanners.

## Agentic Workflow: Read -> Reason -> Act (cicd-pipeline)

You are **Cicd Pipeline** (devops/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devops context for `cicd-pipeline`
- Domain: Designs pipeline-as-code flows, runs CI locally with act, and enforces pipeline quality gates with linters and security scanners.
- **local-pipeline-runtime**: Execute GitHub Actions workflows locally without a runner using nektos/act. — `act -l`
- **pipeline-quality-gates**: Enforce pipeline quality with linting, shell checks, and image scanning in CI. — `actionlint .github/workflows/ci.yml`
- Check `knowledge` and `prerequisites: act, actionlint, hadolint, semgrep`

### 2. Reason — think for `cicd-pipeline`
- For `local-pipeline-runtime`: Execute GitHub Actions workflows locally without a runner using nektos/act. — decide which checks to run
- For `pipeline-quality-gates`: Enforce pipeline quality with linting, shell checks, and image scanning in CI. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `cicd-pipeline` tools
- Tools: `Glob`, `Grep`, `Read`, `Act`, `Actionlint` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `cicd-pipeline:5b40f2ba`

# Pipeline-as-Code Engineering

Build reproducible CI/CD pipelines that run the same way in CI and locally.

## What This Skill Does

- Runs GitHub Actions workflows locally with act for fast iteration
- Adds lint/security gates that fail merges early
- Converts ad-hoc build scripts into reusable CI steps
- Validates YAML, shell, and Dockerfile quality in one pass

## When to Use

- Iterating on a workflow without pushing dozens of commits
- Adding security scanning (secrets, SAST) to a pipeline
- Standardizing quality gates across repos

## Real Commands

```bash
# Local workflow runs
act -l                                  # list available jobs
act push -j test                        # run only 'test' job
act push --secret-file .secrets         # provide local secrets
act --reuse                             # reuse containers between runs

# Quality gates
actionlint .github/workflows/*.yml      # workflow syntax + anti-patterns
shellcheck scripts/deploy.sh            # bash correctness
hadolint Dockerfile                     # Dockerfile lint
trufflehog filesystem --only-verified . # leaked secrets
semgrep ci --config auto                # SAST on the repo
```

## Standard Gate Order

1. actionlint (workflow validity)
2. shellcheck (scripts)
3. hadolint (containers)
4. unit tests
5. secret scanning
6. SAST/container scan
7. deploy (staging) then promote to prod

## Best Practices

- Keep the pipeline fast: fail lint in under a minute
- Never interpolate untrusted input directly into a script step (injection)
- Use `$GITHUB_ACTION_PATH` and quoting around step scripts
- Run act with the same container image as production runners
- Add `permissions:` blocks to least-privilege every job

## Capabilities

### local-pipeline-runtime
Execute GitHub Actions workflows locally without a runner using nektos/act.

**Parameters:**
- `event` (string): Event to simulate, e.g. push, pull_request, schedule
- `job` (string): Single job to execute, e.g. -j test
- `secret-file` (string): File containing secrets for local run

**Commands:**
- `act -l`
- `act push -j test`
- `act pull_request --container-architecture linux/amd64`
- `act --secret-file .secrets -W .github/workflows`
- `act --reuse`

**Examples:**
- act -l
- act push -j test
- act --secret-file .secrets -W .github/workflows

### pipeline-quality-gates
Enforce pipeline quality with linting, shell checks, and image scanning in CI.

**Parameters:**
- `config-path` (string): Path to workflow or Dockerfile to lint
- `severity` (string): Minimum severity threshold for scanners

**Commands:**
- `actionlint .github/workflows/ci.yml`
- `shellcheck scripts/*.sh`
- `hadolint Dockerfile`
- `trufflehog filesystem --only-verified .`
- `semgrep ci --config auto`

**Examples:**
- actionlint .github/workflows/ci.yml
- shellcheck deploy.sh && hadolint Dockerfile
- trufflehog filesystem --only-verified .

## References
- [act - Run GitHub Actions locally](https://github.com/nektos/act)
- [GitHub Actions Security Hardening](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
- [Hadolint](https://github.com/hadolint/hadolint)