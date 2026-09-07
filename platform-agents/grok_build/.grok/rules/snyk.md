Scans dependencies, code, IaC, and containers with Snyk, monitoring projects and enforcing policies from the CLI.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `snyk auth`, `snyk code test`
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

**Parameters:**
- `severityThreshold` (string): Minimum severity: low, medium, high, critical
- `allProjects` (boolean): Scan all projects in the directory
- `org` (string): Snyk organization slug

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

**Parameters:**
- `severityThreshold` (string): Minimum severity to report
- `report` (boolean): Upload IaC results to Snyk

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

**Parameters:**
- `projectName` (string): Custom project name in the Snyk dashboard
- `org` (string): Snyk org slug or ID to associate monitored projects with.

**Commands:**
- `snyk monitor`
- `snyk monitor --all-projects`
- `snyk monitor --project-name=api`
- `snyk test --all-projects --prune-repeated-subdependencies`

**Examples:**
- snyk monitor
- snyk monitor --all-projects
- snyk monitor --project-name=my-api

## References
- [Snyk Documentation](https://docs.snyk.io/)
- [Snyk CLI GitHub](https://github.com/snyk/cli)