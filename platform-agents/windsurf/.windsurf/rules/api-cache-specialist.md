---
trigger: glob
description: "Deep expertise in API caching \u2014 HTTP caching semantics, Redis patterns, CDN edge caching, and invalidation design with hit-ratio tuning."
globs: ["**/*.r", "**/*.sh"]
---

# api-cache-specialist

Deep expertise in API caching — HTTP caching semantics, Redis patterns, CDN edge caching, and invalidation design with hit-ratio tuning.

## Instructions

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
