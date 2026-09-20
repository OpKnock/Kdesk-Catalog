---
name: "vault"
description: "Manages secrets, policies, tokens, and dynamic credentials with HashiCorp Vault CLI and KV/transit secret engines. Use when working with kv secrets, policies and tokens, dynamic secrets, audit and ops or when the user mentions kv secrets, policies and tokens, dynamic secrets, audit and ops."
license: "MIT"
compatibility: "Requires vault."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "security"}
allowed-tools: "Glob Grep Read Bash(vault:*)"
---

Manages secrets, policies, tokens, and dynamic credentials with HashiCorp Vault CLI and KV/transit secret engines.

## Agentic Workflow: Read -> Reason -> Act (vault)

You are **vault** (security/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — security context for `vault`
- Domain: Manages secrets, policies, tokens, and dynamic credentials with HashiCorp Vault CLI and KV/transit secret engines.
- **kv-secrets**: Store, read, and delete secrets in KV engines. — `vault kv put secret/myapp db_password="hunter2" db_user="app"`
- **policies-and-tokens**: Author policies and create scoped tokens. — `vault policy write app-readonly - <<'EOF'`
- **dynamic-secrets**: Generate dynamic credentials for databases. — `vault secrets enable database`
- Check `knowledge` and `prerequisites: vault`

### 2. Reason — think for `vault`
- For `kv-secrets`: Store, read, and delete secrets in KV engines. — decide which checks to run
- For `policies-and-tokens`: Author policies and create scoped tokens. — decide which checks to run
- For `dynamic-secrets`: Generate dynamic credentials for databases. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `vault` tools
- Tools: `Glob`, `Grep`, `Read`, `Vault` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `vault:5a64aa0b`

# Vault

Centralized secrets management with dynamic, revocable credentials.

## What This Skill Does

- Stores and reads KV secrets with versioning
- Writes and tests policies, creates scoped tokens
- Generates dynamic database credentials with leases
- Enables audit logging and manages unsealing

## When to Use

- Centralizing application secrets
- Issuing short-lived credentials instead of static keys
- Auditing secret access

## Real Commands

```bash
# KV v2
vault secrets enable -path=secret kv-v2
vault kv put secret/myapp db_password="hunter2"
vault kv get -field=db_password secret/myapp
vault kv list secret/

# Policies and tokens
vault policy write app-readonly - <<'EOF'
path "secret/data/myapp" { capabilities = ["read"] }
EOF
vault token create -policy=app-readonly -ttl=1h
vault login -method=token

# Dynamic DB credentials
vault secrets enable database
vault write database/roles/readonly db_name=postgres \
  creation_statements="SELECT username FROM pg_user" \
  default_ttl=1h max_ttl=24h
vault read database/creds/readonly

# Audit
vault audit enable file file_path=/var/log/vault-audit.log
vault status
```

## Best Practices

- Use dynamic credentials with short TTLs over static secrets
- Scope tokens with least-privilege policies
- Enable audit logging in production
- Rotate the root token after init and store unseal keys offline
- Never commit Vault tokens; inject via agent or sidecar

## Capabilities

### kv-secrets
Store, read, and delete secrets in KV engines.

**Parameters:**
- `path` (string): Secret path, e.g. secret/myapp
- `field` (string): Single field to read

**Commands:**
- `vault kv put secret/myapp db_password="hunter2" db_user="app"`
- `vault kv get secret/myapp`
- `vault kv get -field=db_password secret/myapp`
- `vault kv delete secret/myapp`
- `vault kv list secret/`
- `vault secrets enable -path=secret kv-v2`

**Examples:**
- vault kv put secret/myapp api_key=xyz
- vault kv get -field=db_password secret/myapp
- vault kv list secret/

### policies-and-tokens
Author policies and create scoped tokens.

**Parameters:**
- `policy` (string): Policy name
- `ttl` (string): Token TTL, e.g. 1h

**Commands:**
- `vault policy write app-readonly - <<'EOF'`
- `vault policy read app-readonly`
- `vault token create -policy=app-readonly -ttl=1h`
- `vault login -method=token`
- `vault token lookup`

**Examples:**
- vault token create -policy=app-readonly -ttl=1h
- vault login -method=token
- vault policy read app-readonly

### dynamic-secrets
Generate dynamic credentials for databases.

**Parameters:**
- `role` (string): Database role name
- `lease` (string): Lease ID to renew or revoke

**Commands:**
- `vault secrets enable database`
- `vault write database/config/postgres connection_url="postgresql://root:pass@localhost:5432/postgres"`
- `vault read database/creds/readonly`
- `vault list database/roles`
- `vault lease renew database/creds/readonly/x`

**Examples:**
- vault read database/creds/readonly
- vault list database/roles
- vault write database/roles/readonly db_name=postgres

### audit-and-ops
Check server status and enable audit logs.

**Parameters:**
- `auditType` (string): Audit backend: file, syslog, socket
- `filePath` (string): Log path for the file audit backend.

**Commands:**
- `vault status`
- `vault audit enable file file_path=/var/log/vault-audit.log`
- `vault audit list`
- `vault unseal`
- `vault operator init`

**Examples:**
- vault status
- vault audit enable file file_path=/var/log/vault-audit.log
- vault audit list

## References
- [Vault Documentation](https://developer.hashicorp.com/vault/docs)
- [Vault KV Engine](https://developer.hashicorp.com/vault/docs/secrets/kv/kv-v2)

## Progressive Disclosure
This skill has many capabilities. For detailed reference:
- `references/REFERENCE.md` — full capability docs and edge cases
- `scripts/` — executable helpers (see `allowed-tools`)
- `assets/` — templates and data files
Load references on demand via relative paths, not at startup.
