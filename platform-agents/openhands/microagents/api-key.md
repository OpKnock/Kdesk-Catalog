---
name: "api-key"
description: "Designs, generates, stores, and rotates API keys: high-entropy generation with openssl, hashed storage, and Vault-backed issuance."
type: knowledge
triggers: ["api-key", "key-generation", "vault-issuance"]
---

# Api Key

Designs, generates, stores, and rotates API keys: high-entropy generation with openssl, hashed storage, and Vault-backed issuance.

## Instructions

# API Keys

## What this skill does

End-to-end API key management: generating high-entropy keys with openssl/node crypto, storing them in Vault KV, hashing keys at rest, and rotating keys with dual-write grace windows.

## When to use

- Adding key-based auth to an API
- Responding to a leaked key incident (rotation)
- Centralizing key storage instead of .env pasting

## Real commands

```bash
# Generate a 256-bit key
openssl rand -hex 32
openssl rand -base64 32

# Store in Vault
vault kv put secret/api-keys/prod key=$(openssl rand -hex 32)

# Retrieve
vault kv get -field=key secret/api-keys/prod

# List / delete
vault kv list secret/api-keys
vault kv delete secret/api-keys/expired
```

## Storage best practice

Store only a SHA-256 hash of the key in the application database:

```bash
KEY=$(openssl rand -hex 32)
echo -n "$KEY" | sha256sum
```

Show the raw key exactly once, then hash it.

## Rotation checklist

1. Generate new key and store as v2 in Vault
2. Deploy dual-read (accept old + new) for a grace window
3. Cut over writers to the new key
4. Revoke the old key with vault kv delete

## Testing

- Confirm the old key stops working after revocation
- Verify Vault ACLs: a service can only read its own path

## Best practices

- Never log keys; redact Authorization in access logs
- Rate-limit by key and monitor anomalous usage
- Use X-API-Key header or Bearer tokens consistently

## Capabilities

### key-generation
Generate strong API keys and inspect their entropy.

**Commands:**
- `openssl rand -hex 32`
- `openssl rand -base64 32`
- `node -e "console.log(require('crypto').randomBytes(32).toString('base64url'))"`
- `uuidgen`
- `openssl rand -base64 32 | sha256sum`

**Examples:**
- KEY=$(openssl rand -hex 32) && echo $KEY
- openssl rand -base64 48 | tr '+/' '-_' | tr -d '='
- node -e "console.log(require('crypto').randomBytes(24).toString('hex'))"

### vault-issuance
Store, retrieve, and rotate API keys in HashiCorp Vault KV.

**Commands:**
- `vault kv put secret/api-keys/prod key=$(openssl rand -hex 32)`
- `vault kv get secret/api-keys/prod`
- `vault kv list secret/api-keys`
- `vault kv delete secret/api-keys/expired`
- `vault kv patch secret/api-keys/prod rotated_at=$(date -u +%FT%TZ)`

**Examples:**
- vault kv put secret/api-keys/prod service=payments key=$(openssl rand -hex 32)
- vault kv get -field=key secret/api-keys/prod
- vault kv metadata get secret/api-keys/prod
