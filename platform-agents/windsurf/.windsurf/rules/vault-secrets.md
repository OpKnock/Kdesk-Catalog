---
trigger: glob
description: "Manages secrets in HashiCorp Vault KV v2. Reads and writes versioned secrets, creates scoped tokens with policies, inspects token identity and metadata, and applies least-privilege access through HCL policies. Use when working with vault secrets, api or when the user mentions vault secrets, api."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
---

Manages secrets in HashiCorp Vault KV v2. Reads and writes versioned secrets, creates scoped tokens with policies, inspects token identity and metadata, and applies least-privilege access through HCL policies.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `vault kv put secret/app/api_key=abc123`
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

# Vault v2

Hand-crafted skill for HashiCorp Vault secret management.

## What this skill does

- Reads and writes versioned secrets with KV v2
- Creates scoped tokens for apps
- Inspects token identity and secret metadata

## When to use

- Storing API keys, DB credentials, certificates
- Issuing short-lived tokens for services
- Auditing what a token can actually access

## Real commands

```bash
# Write and read a secret
vault kv put secret/app/api_key=abc123
vault kv get secret/app
vault kv get -format=json secret/app | jq -r ".data.data.api_key"

# Version metadata
vault kv metadata get secret/app

# Delete a version
vault kv delete secret/app/api_key

# Tokens
vault token create -policy=app -ttl=1h
vault read auth/token/lookup-self
```

## Policy example

```hcl
path "secret/data/app/*" {
  capabilities = ["read"]
}
```

## Testing

```bash
vault kv put secret/test/hello=world
vault kv get secret/test/hello
vault token create -policy=app -ttl=30m
```

## Best practices

- Prefer short-lived tokens over long-lived ones
- Write policies per service, then hand the policy not the root token
- Never echo secrets in shells you share; use -field=

## Capabilities

### vault-secrets
Read/write secrets and manage auth in Vault

**Parameters:**
- `path` (string): Secret path, e.g. secret/app
- `policy` (string): Policy name for tokens
- `ttl` (string): Token lifetime, e.g. 1h

**Commands:**
- `vault kv put secret/app/api_key=abc123`
- `vault kv get secret/app`
- `vault kv delete secret/app/api_key`
- `vault token create -policy=app -ttl=1h`
- `vault read auth/token/lookup-self`
- `vault kv metadata get secret/app`

**Examples:**
- vault kv put secret/app/api_key=abc123
- vault kv get -format=json secret/app | jq -r ".data.data.api_key"
- vault token create -policy=app -ttl=1h

## References
- [Vault KV v2 docs](https://developer.hashicorp.com/vault/docs/secrets/kv/kv-v2)
- [Vault token auth](https://developer.hashicorp.com/vault/docs/auth/token)
- [Vault policies](https://developer.hashicorp.com/vault/docs/concepts/policies)
