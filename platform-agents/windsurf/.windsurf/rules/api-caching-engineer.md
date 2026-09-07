---
trigger: glob
description: "Implements API caching with invalidation strategies: HTTP headers, Redis cache-aside with TTL, and event-driven invalidation. Use when working with http header caching, event invalidation or when the user mentions http header caching, event invalidation."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
---

Implements API caching with invalidation strategies: HTTP headers, Redis cache-aside with TTL, and event-driven invalidation.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -s -D - http://localhost:3000/api/products | grep -i -E`, `redis-cli PUBLISH product.updated '{"id":42}'`
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

# API Caching Engineer

Implements caching with disciplined invalidation so data stays fresh.

## When to Use
- Repeated reads hammer the database
- Stale data incidents from bad TTLs
- Adding caching to specific endpoints

## Real Commands

```bash
# Verify headers
curl -s -D - http://localhost:3000/api/products | grep -i -E 'cache-control|etag|vary'

# Conditional requests
curl -s -H 'If-None-Match: W/"etag1"' -o /dev/null -w '%{http_code}' http://localhost:3000/api/products

# Event-driven invalidation
redis-cli PUBLISH product.updated '{"id":42}'
redis-cli DEL api:products:42

# Namespace flush
redis-cli --scan --pattern 'api:products:*' | xargs -r redis-cli DEL
```

## Invalidation Rules
- Writes delete the affected keys
- Domain events drive scoped deletion
- Never wait for TTL for correctness

## Testing
Write a test that updates a resource and asserts the next read misses.

## Best Practices
- Invalidate by namespace patterns, not single keys
- Keep TTLs generous but never load-bearing

## Capabilities

### http-header-caching
Apply Cache-Control, ETag, and Vary for safe HTTP caching

**Parameters:**
- `url` (string): Endpoint URL
- `ttl` (string): Cache-Control max-age

**Commands:**
- `curl -s -D - http://localhost:3000/api/products | grep -i -E 'cache-control|etag|vary'`
- `curl -s -H 'If-None-Match: W/"etag1"' -o /dev/null -w '%{http_code}' http://localhost:3000/api/products`
- `curl -s -H 'If-Modified-Since: Mon, 10 Aug 2026 00:00:00 GMT' -o /dev/null -w '%{http_code}' http://localhost:3000/api/products`
- `curl -s -X POST http://localhost:3000/api/products -H 'Content-Type: application/json' -d '{}' -D - | grep -i cache-control`
- `curl -s -o /dev/null -w '%{http_code}' -H 'Cache-Control: no-cache' http://localhost:3000/api/products`

**Examples:**
- curl -s -D - http://localhost:3000/api/products | grep -i -E 'cache-control|etag|vary'
- curl -s -H 'If-None-Match: W/"etag1"' -o /dev/null -w '%{http_code}' http://localhost:3000/api/products
- curl -s -X POST http://localhost:3000/api/products -H 'Content-Type: application/json' -d '{}' -D - | grep -i cache-control

### event-invalidation
Invalidate cache entries on domain events with pub/sub

**Parameters:**
- `channel` (string): Redis pub/sub channel
- `keyPattern` (string): Keys to invalidate

**Commands:**
- `redis-cli PUBLISH product.updated '{"id":42}'`
- `redis-cli SUBSCRIBE product.updated`
- `redis-cli DEL api:products:42`
- `redis-cli --scan --pattern 'api:products:*' | xargs -r redis-cli DEL`
- `redis-cli SET api:products:42 '{}' EX 60 NX`

**Examples:**
- redis-cli PUBLISH product.updated '{"id":42}' && redis-cli DEL api:products:42
- redis-cli --scan --pattern 'api:products:*' | xargs -r redis-cli DEL
- redis-cli SUBSCRIBE product.updated

## References
- [Redis Pub/Sub](https://redis.io/docs/latest/develop/use/pubsub/)
- [HTTP Caching Semantics](https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching)
