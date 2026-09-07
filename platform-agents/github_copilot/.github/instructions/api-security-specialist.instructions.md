---
applyTo: "**/*.json **/*.r **/*.sh"
---

Manages API secrets and identity: HashiCorp Vault secret storage and rotation, AWS Secrets Manager CLI, and secrets hygiene for API keys.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `vault server -dev`, `aws secretsmanager create-secret --name prod/api-key --secre`
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

**Parameters:**
- `path` (string): Secret path in the KV store
- `format` (string): Output format: table, json, yaml
- `fields` (object): Key-value secret fields

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

**Examples:**
- -cli --help
- -api --help

## References
- [Vault KV Secrets](https://developer.hashicorp.com/vault/docs/secrets/kv/kv-v2)
- [AWS Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/)
