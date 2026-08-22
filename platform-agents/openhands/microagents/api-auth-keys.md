---
name: "api-auth-keys"
description: "API auth with API key management - generate secure keys, hash at rest, scope and rate-limit them, and rotate keys without downtime."
type: knowledge
triggers: ["api-auth-keys", "api-key-mgmt"]
---

# Api Auth Keys

API auth with API key management - generate secure keys, hash at rest, scope and rate-limit them, and rotate keys without downtime.

## Instructions

# API Auth (API Keys)

## What this skill does
Manage API keys for third-party access: generate cryptographically secure keys, store only hashes, attach scopes and expiry, support rotation and revocation.

## When to use
- Issuing keys to external partners
- Replacing shared static secrets
- Enforcing per-key limits and scopes

## Real commands
```bash
# Generate a strong key
openssl rand -hex 32
node -e "const c=require('crypto');console.log(c.randomBytes(32).toString('hex'))"

# Hash for storage (never store the raw key)
node -e "const c=require('crypto');console.log(c.createHash('sha256').update(process.argv[1]).digest('hex'))" $KEY

# Create a scoped key
curl -s -X POST http://localhost:8080/api/keys \
  -H 'X-Admin-Key: $ADMIN' -H 'Content-Type: application/json' \
  -d '{"name":"billing","scopes":["read:invoices"],"expires_at":"2025-01-01T00:00:00Z"}' | jq '{key, id}'

# List keys
curl -s http://localhost:8080/api/keys | jq '.keys[] | {id, name, last_used_at}'

# Rotate
curl -s -X POST http://localhost:8080/api/keys/$ID/rotate -H 'X-Admin-Key: $ADMIN' | jq '{new_key, old_expires}'

# Revoke
curl -s -X DELETE http://localhost:8080/api/keys/$ID -H 'X-Admin-Key: $ADMIN' | jq '.revoked'

# Use it
curl -s http://localhost:8080/api/orders -H 'X-API-Key: $KEY' -o /dev/null -w '%{http_code}'
```

## Key formats
- `sk_live_` prefix + 32+ random bytes (industry standard)
- Show the raw key exactly once at creation

## Best practices
- Hash with SHA-256 before storing (plus optional HMAC pepper)
- Require scopes; default to least privilege
- Set expiry on all keys; auto-rotate yearly
- On rotation, accept the old key for a grace window

## Testing
```bash
curl -s http://localhost:8080/api/orders -H 'X-API-Key: bad-key' -o /dev/null -w '%{http_code}\n'
curl -s http://localhost:8080/api/keys/$ID/rotate -X POST -H 'X-Admin-Key: $ADMIN' | jq
```

## Capabilities

### api-key-mgmt
Generate, hash, scope, and rotate API keys

**Commands:**
- `openssl rand -hex 32`
- `node -e "const c=require('crypto');console.log(c.randomBytes(32).toString('hex'))"`
- `node -e "const c=require('crypto');console.log(c.createHash('sha256').update(process.argv[1]).digest('hex'))" $KEY`
- `curl -s -X POST http://localhost:8080/api/keys -H 'X-Admin-Key: $ADMIN' -H 'Content-Type: application/json' -d '{"name":"billing","scopes":["read:invoices"],"expires_at":"2025-01-01T00:00:00Z"}' | jq '{key, id}'`
- `curl -s http://localhost:8080/api/keys | jq '.keys[] | {id, name, last_used_at}'`

**Examples:**
- curl -s -X DELETE http://localhost:8080/api/keys/$ID -H 'X-Admin-Key: $ADMIN' | jq '.revoked'
- curl -s http://localhost:8080/api/keys/$ID/rotate -X POST -H 'X-Admin-Key: $ADMIN' | jq '{new_key, old_expires}'
- curl -s http://localhost:8080/api/orders -H 'X-API-Key: $KEY' -o /dev/null -w '%{http_code}'
