---
name: "api-security-specialist"
description: "Manages API secrets and identity: HashiCorp Vault secret storage and rotation, AWS Secrets Manager CLI, and secrets hygiene for API keys."
type: knowledge
triggers: ["api-security-specialist", "vault-secrets", "aws-secrets"]
---

# api-security-specialist

Manages API secrets and identity: HashiCorp Vault secret storage and rotation, AWS Secrets Manager CLI, and secrets hygiene for API keys.

## Instructions

# API Security Specialist

Secret and identity management.

## What This Skill Does
- Centralizes API secrets in Vault
- Automates rotation with cloud tools
- Enforces secrets hygiene

## When to Use
- Centralizing scattered secrets
- Rotation compliance
- Onboarding API consumers

## Real Commands

```bash
vault server -dev
vault kv put secret/api DB_PASSWORD="s3cr3t" API_KEY="key-123"
vault kv get secret/api
aws secretsmanager create-secret --name prod/api-key --secret-string "{\"key\":\"abc123\"}"
```

## Secret Hygiene
- Never commit keys; use env vars
- Rotate quarterly or on exposure
- Grant least-privilege access
- Audit reads with Vault audit logs

## Testing
- Verify secrets resolve in each environment
- Test rotation breaks old credentials
- Confirm audit trails capture access


## Best Practices
- Use short-lived tokens where possible
- Separate staging and prod namespaces
- Automate rotation schedules

## Capabilities

### vault-secrets
Store and retrieve API secrets in Vault

**Commands:**
- `vault server -dev`
- `vault kv put secret/api DB_PASSWORD="s3cr3t" API_KEY="key-123"`
- `vault kv get secret/api`
- `vault kv get -format=json secret/api | jq '.data.data.API_KEY'`
- `vault kv delete secret/api`

**Examples:**
- vault kv put stores key-value secrets
- vault kv get retrieves with -format=json
- vault kv delete removes rotated secrets

### aws-secrets
Manage secrets with AWS Secrets Manager

**Commands:**
- `aws secretsmanager create-secret --name prod/api-key --secret-string "{\"key\":\"abc123\"}"`
- `aws secretsmanager get-secret-value --secret-id prod/api-key --query SecretString --output text`
- `aws secretsmanager rotate-secret --secret-id prod/api-key`
- `aws secretsmanager list-secrets --query 'SecretList[].Name' --output text`
