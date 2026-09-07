---
applyTo: "**/*.r **/*.sh"
---

Designs, generates, stores, and rotates API keys: high-entropy generation with openssl, hashed storage, and Vault-backed issuance.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `openssl rand -hex 32`, `vault kv put secret/api-keys/prod key=$(openssl rand -hex 32`
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

**Parameters:**
- `bytes` (number): Number of random bytes (32 = 256 bits)
- `encoding` (string): hex, base64, or base64url

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

**Parameters:**
- `path` (string): Vault KV path, e.g. secret/api-keys/prod
- `field` (string): Single field to read from the secret

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

## References
- [Vault KV v2](https://developer.hashicorp.com/vault/docs/secrets/kv/kv-v2)
- [OWASP API Key Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/API_Key_Security_Cheat_Sheet.html)
- [RFC 9110 Authorization](https://www.rfc-editor.org/rfc/rfc9110#name-authorization)
