---
name: "request-deduplication"
description: "Expert reference covering idempotency keys for unsafe methods, ETag/If-None-Match caching for GETs, and Redis SETNX guard patterns to prevent duplicate execution. Use when working with idempotency etag, api or when the user mentions idempotency etag, api."
license: "MIT"
compatibility: "Requires redis-cli. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(redis-cli:*)"
---

Expert reference covering idempotency keys for unsafe methods, ETag/If-None-Match caching for GETs, and Redis SETNX guard patterns to prevent duplicate execution.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -i -X POST http://localhost:8080/payments -H "Idempoten`
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

# Request Deduplication

Expert skill for making API requests idempotent and deduplicated.

## What this skill does

- Uses Idempotency-Key headers so retried POSTs return the stored response
- Caches GETs with ETag/If-None-Match to avoid duplicate work
- Guards concurrent duplicates with a Redis SETNX lock

## When to use

- Payment or order endpoints where retries must not double-charge
- Expensive report endpoints hit repeatedly by clients
- Designing APIs where the same request may arrive twice in a short window

## Real commands

```bash
# Send the same mutation twice with one key: second call short-circuits
curl -i -X POST http://localhost:8080/payments -H "Idempotency-Key: 9f8c-4a2b" -d '{"amount":100}'
curl -i -X POST http://localhost:8080/payments -H "Idempotency-Key: 9f8c-4a2b" -d '{"amount":100}'

# Conditional GET: 304 if the ETag still matches
curl -i -H 'If-None-Match: "a1b2c3"' http://localhost:8080/orders/42

# Atomic dedup guard in Redis
redis-cli SETNX idem:9f8c-4a2b processing
redis-cli EXPIRE idem:9f8c-4a2b 3600
```

## Server behavior

- On first POST with a key: execute, store response, return it
- On repeat POST with the same key: return the stored response unchanged
- GET responses carry ETag headers; clients echo them with If-None-Match

## Testing

```bash
# Twice, expect identical bodies and no double side effects
curl -s -X POST http://localhost:8080/payments -H "Idempotency-Key: k1" -d '{"amount":100}'
curl -s -X POST http://localhost:8080/payments -H "Idempotency-Key: k1" -d '{"amount":100}'

# Expect 304 on cached GET
curl -i -H 'If-None-Match: "a1b2c3"' http://localhost:8080/orders/42
```

## Best practices

- Never generate idempotency keys server-side for client mutations
- Store keys with a TTL aligned to your retry window (1-24h)
- Make the dedup record atomic with SETNX so concurrent calls cannot double-run

## Capabilities

### idempotency-etag
Deduplicate requests with idempotency keys and conditional GETs

**Parameters:**
- `idempotency_key` (string): Client-generated key identifying a logical operation
- `etag` (string): Response fingerprint used with If-None-Match
- `ttl_seconds` (integer): How long dedup records live in Redis

**Commands:**
- `curl -i -X POST http://localhost:8080/payments -H "Idempotency-Key: 9f8c-4a2b" -d '{"amount":100}'`
- `curl -i -X POST http://localhost:8080/payments -H "Idempotency-Key: 9f8c-4a2b" -d '{"amount":100}'`
- `curl -i -H 'If-None-Match: "a1b2c3"' http://localhost:8080/orders/42`
- `redis-cli SETNX idem:9f8c-4a2b processing`
- `redis-cli EXPIRE idem:9f8c-4a2b 3600`

**Examples:**
- curl -i -H 'If-None-Match: "a1b2c3"' http://localhost:8080/orders/42
- curl -s -o /dev/null -w '%{http_code}' -X POST http://localhost:8080/payments -H "Idempotency-Key: 9f8c-4a2b" -d '{"amount":100}'
- redis-cli SETNX idem:9f8c-4a2b processing

## References
- [HTTP ETag spec (RFC 7232)](https://datatracker.ietf.org/doc/html/rfc7232)
- [Stripe idempotency guide](https://docs.stripe.com/api/idempotent_requests)
