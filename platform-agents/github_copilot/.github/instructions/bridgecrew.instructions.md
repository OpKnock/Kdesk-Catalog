---
applyTo: "**/*.json **/*.r **/*.sh **/*.tf **/*.{yaml,yml}"
---

Run it scans locally over directories and files with framework selection. Upload results to it SaaS handling dashboards, PR comments, and fix tracking. results for centralized fix tracking.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `bridgecrew --directory .`, `bridgecrew --bc-api-key $BRIDGECREW_API_KEY --repo-id myorg/`
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

# Bridgecrew IaC Security

Scan infrastructure-as-code against Bridgecrew/Prisma Cloud policies for misconfigurations.

## What This Skill Does

- Scans Terraform, CloudFormation, Serverless, ARM, and Kubernetes manifests
- Reports policy violations with fix guidance in multiple formats
- Integrates with the Bridgecrew SaaS platform for dashboards and PR gatekeeping
- Excludes false positives per policy or per check

## When to Use

- Pre-deploy IaC review for misconfigurations
- CI gate that fails on high-severity policy violations
- Centralized compliance reporting for cloud infrastructure

## Real Commands

```bash
# Basic directory scan
bridgecrew --directory .

# Framework-scoped scan with JSON output
bridgecrew -d terraform/ --framework terraform -o json

# Single-file scan
bridgecrew -f main.tf -o cli

# Skip a noisy policy and output SARIF for GitHub code scanning
bridgecrew -d . --skip-check CKV_AWS_79 --output sarif

# Upload to the platform
bridgecrew --bc-api-key $BRIDGECREW_API_KEY --repo-id myorg/infra

# Modern engine: checkov with platform key
checkov -d . --bc-api-key $BRIDGECREW_API_KEY --repo-id myorg/infra
```

## Best Practices

- Run in CI on every PR; fail only on HIGH/CRITICAL to start
- Keep baseline results reviewed and suppress known-false positives explicitly
- Scan Kubernetes YAML with the k8s framework as part of the same pipeline
- Prefer checkov for newer policy features; bridgecrew CLI is legacy
- Store the API key in CI secrets, never in the repo

## Capabilities

### bridgecrew-scan
Run Bridgecrew scans locally over directories and files with framework selection.

**Parameters:**
- `directory` (string): Directory to scan recursively
- `framework` (string): IaC framework: terraform, cloudformation, serverless, arm
- `output` (string): Report format: cli, json, junitxml, sarif

**Commands:**
- `bridgecrew --directory .`
- `bridgecrew -d terraform/ --framework terraform`
- `bridgecrew -f main.tf -o json`
- `bridgecrew -d . --skip-check CKV_AWS_79`
- `bridgecrew -d . --output junitxml`

**Examples:**
- bridgecrew --directory ./infra --framework terraform --output cli
- bridgecrew -f serverless.yml --framework serverless
- bridgecrew -d . --compact

### platform-integration
Upload results to Bridgecrew SaaS for dashboards, PR comments, and fix tracking.

**Parameters:**
- `apiKey` (string): Bridgecrew API key (env: BRIDGECREW_API_KEY)
- `repoId` (string): Repository identifier for result upload, e.g. org/repo

**Commands:**
- `bridgecrew --bc-api-key $BRIDGECREW_API_KEY --repo-id myorg/infra`
- `checkov -d . --bc-api-key $BRIDGECREW_API_KEY --repo-id myorg/infra --repo-branch main`
- `bridgecrew --bc-api-key $BRIDGECREW_API_KEY --directory . --skip-fixes`

**Examples:**
- bridgecrew --bc-api-key $BRIDGECREW_API_KEY --repo-id acme/infra
- checkov -d . --bc-api-key $BRIDGECREW_API_KEY --repo-id acme/infra --download-external-modules

## References
- [Bridgecrew Documentation](https://docs.bridgecrew.io/)
- [Prisma Cloud IaC Docs](https://docs.prismacloud.io/en/enterprise-edition/content/iac)
