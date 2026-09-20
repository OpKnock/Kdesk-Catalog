---
trigger: glob
description: "Builds and deploys infrastructure with Pulumi (TypeScript/Python/Go): stacks, previews, outputs, imports, and state management."
globs: ["**/*.go", "**/*.json", "**/*.py", "**/*.r", "**/*.sh", "**/*.{ts,tsx}"]
---

# pulumi

Builds and deploys infrastructure with Pulumi (TypeScript/Python/Go): stacks, previews, outputs, imports, and state management.

## Instructions

# Pulumi Infrastructure as Code

Provision cloud resources with real programming languages: stacks, previews, and secrets.

## What This Skill Does

- Scaffolds projects in TypeScript, Python, Go, or .NET
- Creates and selects stacks per environment
- Previews diffs before applying changes
- Manages config and encrypted secrets
- Imports existing resources and refreshes state

## When to Use

- Preferring real code (loops, conditionals) over HCL
- Multi-environment infrastructure with shared packages
- Teams that want typed resource APIs

## Real Commands

```bash
# Project setup
pulumi new aws-typescript --name infra --stack dev
pulumi stack init dev
pulumi stack select prod

# Deploy loop
pulumi preview
pulumi up -y
pulumi destroy -y

# Config and secrets
pulumi config set aws:region us-east-1
pulumi config set --secret db_password 's3cr3t'
pulumi config get aws:region

# Outputs and state
pulumi stack output endpoint
pulumi stack output --json
pulumi import aws:s3/bucket:Bucket my-bucket aws-123456
pulumi state refresh
pulumi state unprotect 'urn:...'
```

## Minimal Program

```typescript
import * as aws from "@pulumi/aws";
const bucket = new aws.s3.Bucket("my-bucket", {
  acl: "private",
});
export const bucketName = bucket.id;
```

## Best Practices

- One stack per environment (dev/staging/prod) with config separation
- Always use `--secret` for credentials; never plaintext config
- Run `pulumi preview` in CI and require human approval for prod up
- Use automation API or policy-as-code (OPA) for guardrails
- Lock provider versions via package manifests

## Capabilities

### stack-lifecycle
Create, preview, deploy, and destroy infrastructure stacks.

**Commands:**
- `pulumi new aws-typescript`
- `pulumi stack init dev`
- `pulumi preview`
- `pulumi up -y`
- `pulumi destroy -y`
- `pulumi stack select prod`

**Examples:**
- pulumi new aws-typescript
- pulumi preview
- pulumi up -y

### config-and-state
Manage configuration, secrets, outputs, and import existing resources.

**Commands:**
- `pulumi config set aws:region us-east-1`
- `pulumi config set --secret db_password 's3cr3t'`
- `pulumi config get aws:region`
- `pulumi stack output`
- `pulumi import aws:s3/bucket:Bucket my-bucket aws-123456`
- `pulumi state refresh`

**Examples:**
- pulumi config set --secret db_password 's3cr3t'
- pulumi stack output endpoint
- pulumi import aws:s3/bucket:Bucket my-bucket aws-123456
