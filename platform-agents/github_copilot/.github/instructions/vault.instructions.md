---
applyTo: "**/*.r **/*.sh **/*.sql"
---

# vault

Manages secrets, policies, tokens, and dynamic credentials with HashiCorp Vault CLI and KV/transit secret engines.

## Instructions

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
