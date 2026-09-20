---
name: "api-cache-specialist"
description: "Deep expertise in API caching \u2014 HTTP caching semantics, Redis patterns, CDN edge caching, and invalidation design with hit-ratio tuning. Use when working with http caching, redis optimization or when the user mentions http caching, redis optimization."
license: "MIT"
compatibility: "Requires redis, node.js, python, varnish, express. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "infrastructure"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(redis-cli:*)"
---

Deep expertise in API caching — HTTP caching semantics, Redis patterns, CDN edge caching, and invalidation design with hit-ratio tuning.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -s -D - -o /dev/null http://localhost:3000/api/products`, `redis-cli INFO stats | grep -E 'keyspace_hits|keyspace_misse`
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

# API Cache Specialist

Deep expertise in every caching layer of an API: browser, CDN, reverse proxy, and application cache.

## When to Use
- Diagnosing low cache hit ratios
- Designing multi-layer caching
- Tuning TTLs and eviction policies
- Building invalidation pipelines

## Real Commands

```bash
# Inspect response headers
curl -s -D - -o /dev/null http://localhost:3000/api/products

# Verify conditional requests return 304
curl -s -H 'If-None-Match: W/"abc123"' -o /dev/null -w '%{http_code}\n' http://localhost:3000/api/products

# Redis hit ratio
redis-cli INFO stats | grep -E 'keyspace_hits|keyspace_misses'

# Set an eviction policy
redis-cli CONFIG SET maxmemory-policy allkeys-lru
```

## Invalidation Patterns
- TTL-based: `redis-cli EXPIRE api:products 300`
- Event-driven: publish invalidation messages and `redis-cli DEL api:products`
- Versioned keys: `api:products:v2`

## Testing
Load test with `hey -n 10000 -c 100 http://localhost:3000/api/products` and compare p95 before/after caching.

## Best Practices
- Never cache personalized responses without `Vary`
- Keep a cache namespace convention (`api:<resource>:v<ver>`)
- Monitor evicted_keys for churn

## Capabilities

### http-caching
Tune Cache-Control, ETag, and Vary headers for maximum cacheable traffic

**Parameters:**
- `url` (string): Endpoint to probe caching headers on
- `etag` (string): ETag value for conditional request test

**Commands:**
- `curl -s -D - -o /dev/null http://localhost:3000/api/products`
- `curl -s -H 'If-None-Match: W/"abc123"' -o /dev/null -w '%{http_code}' http://localhost:3000/api/products`
- `curl -s -H 'If-Modified-Since: Tue, 10 Aug 2026 00:00:00 GMT' -o /dev/null -w '%{http_code}' http://localhost:3000/api/products`
- `curl -s -o /dev/null -w '%{time_total}' http://localhost:3000/api/products`
- `curl -s -D - http://localhost:3000/api/products | grep -i cache`

**Examples:**
- curl -s -D - -o /dev/null http://localhost:3000/api/products | grep -i -E 'cache-control|etag|vary'
- curl -s -H 'If-None-Match: W/"abc123"' -o /dev/null -w '%{http_code}' http://localhost:3000/api/products
- curl -s -o /dev/null -w 'total=%{time_total} code=%{http_code}\n' http://localhost:3000/api/products

### redis-optimization
Monitor and tune Redis cache hit ratio, memory, and eviction policies

**Parameters:**
- `pattern` (string): Key pattern for cache namespace
- `policy` (string): Redis eviction policy

**Commands:**
- `redis-cli INFO stats | grep -E 'keyspace_hits|keyspace_misses'`
- `redis-cli CONFIG GET maxmemory-policy`
- `redis-cli CONFIG SET maxmemory-policy allkeys-lru`
- `redis-cli --scan --pattern 'api:*' | wc -l`
- `redis-cli MEMORY USAGE api:products`

**Examples:**
- redis-cli INFO stats | grep -E 'keyspace_hits|keyspace_misses'
- redis-cli CONFIG SET maxmemory-policy volatile-lru
- redis-cli --scan --pattern 'api:orders:*' | xargs redis-cli DEL

## References
- [Redis Docs](https://redis.io/docs/latest/)
- [MDN HTTP Caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching)
- [Varnish Docs](https://varnish-cache.org/docs/)
