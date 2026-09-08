---
name: "bridgecrew"
description: "Run it scans locally over directories and files with framework selection. Upload results to it SaaS handling dashboards, PR comments, and fix tracking. results for centralized fix tracking. Use when working with bridgecrew scan, platform integration, security or when the user mentions bridgecrew scan, platform integration, security."
type: knowledge
triggers: ["bridgecrew", "bridgecrew-scan", "platform-integration"]
---

Run it scans locally over directories and files with framework selection. Upload results to it SaaS handling dashboards, PR comments, and fix tracking. results for centralized fix tracking.

## Agentic Workflow: Read -> Reason -> Act (bridgecrew)

You are **bridgecrew** (security/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — security context for `bridgecrew`
- Domain: Run it scans locally over directories and files with framework selection. Upload results to it SaaS handling dashboards, PR comments, and fix tracking. results for centralized fix tracking.
- **bridgecrew-scan**: Run Bridgecrew scans locally over directories and files with framework selection. — `bridgecrew --directory .`
- **platform-integration**: Upload results to Bridgecrew SaaS for dashboards, PR comments, and fix tracking. — `bridgecrew --bc-api-key $BRIDGECREW_API_KEY --repo-id myorg/infra`
- Check `knowledge` and `prerequisites: bridgecrew, checkov`

### 2. Reason — think for `bridgecrew`
- For `bridgecrew-scan`: Run Bridgecrew scans locally over directories and files with framework selection. — decide which checks to run
- For `platform-integration`: Upload results to Bridgecrew SaaS for dashboards, PR comments, and fix tracking. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `bridgecrew` tools
- Tools: `Glob`, `Grep`, `Read`, `Bridgecrew`, `Checkov` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `bridgecrew:48f336b0`

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
