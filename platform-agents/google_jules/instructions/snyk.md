# Snyk

Scans dependencies, code, IaC, and containers with Snyk, monitoring projects and enforcing policies from the CLI.

## Instructions

# Snyk

Developer-first security scanning for dependencies, code, IaC, and containers.

## What This Skill Does

- Tests lockfiles for known vulnerabilities and fix paths
- Scans source code with Snyk Code SAST
- Scans Terraform/CloudFormation/K8s with Snyk IaC
- Monitors projects so new vulns surface without rescanning

## When to Use

- Pre-merge dependency checks in CI
- Continuous monitoring of long-lived projects
- Full-stack scan (code + deps + IaC + images)

## Real Commands

```bash
# Authenticate (once)
snyk auth

# Dependencies
snyk test
snyk test --all-projects --severity-threshold=high
snyk test --json -o snyk-results.json

# Code and IaC
snyk code test
snyk iac test --report
snyk container test nginx:1.25 --severity-threshold=high

# Monitor
snyk monitor --all-projects
snyk monitor --project-name=my-api
```

## CI Gate

```yaml
- name: Snyk test
  run: snyk test --all-projects --severity-threshold=high --fail-on=upgradable
```

## Best Practices

- Set --severity-threshold=high in CI to start; tighten later
- Use --fail-on=upgradable to only fail when a fix exists
- Monitor every release so regressions alert automatically
- Keep SNYK_TOKEN in CI secrets, never in the repo
- Triage with the dashboard's priority score, not raw counts

## Capabilities

### dependency-testing
Test projects for vulnerable dependencies.

**Commands:**
- `snyk auth`
- `snyk test`
- `snyk test --all-projects`
- `snyk test --severity-threshold=high`
- `snyk test --json -o snyk-results.json`

**Examples:**
- snyk test
- snyk test --all-projects --severity-threshold=high
- snyk test --org=my-org --json

### code-iac-container
Scan source code, IaC files, and container images.

**Commands:**
- `snyk code test`
- `snyk iac test`
- `snyk iac test --report`
- `snyk container test ubuntu:latest`
- `snyk iac test --sarif`

**Examples:**
- snyk code test
- snyk iac test --report
- snyk container test nginx:1.25 --severity-threshold=high

### monitoring
Monitor projects and get alerts for new vulns.

**Commands:**
- `snyk monitor`
- `snyk monitor --all-projects`
- `snyk monitor --project-name=api`
- `snyk test --all-projects --prune-repeated-subdependencies`

**Examples:**
- snyk monitor
- snyk monitor --all-projects
- snyk monitor --project-name=my-api
