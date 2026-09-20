---
applyTo: "**/*.go **/*.r **/*.sh"
---

# Caching

Accelerates API responses with Redis TTL caches for computed data, HTTP cache-control and ETag headers for clients and proxies, and hit-rate measurement to validate effectiveness.

## Instructions

# Caching

## What this skill does

Implements API caching: Redis TTL caches for computed data, HTTP cache-control/ETag headers for clients and proxies, and hit-rate measurement.

## When to use

- An endpoint returns the same data repeatedly
- Reducing latency for static assets
- Caching expensive queries or third-party calls

## Real commands

```bash
# Redis TTL cache
redis-cli SET cache:users:page:1 '[...]' EX 300
redis-cli GET cache:users:page:1
redis-cli TTL cache:users:page:1
redis-cli DEL cache:users:page:1

# HTTP caching headers
curl -sI https://api.your-app.test/static/app.js | grep -iE 'cache-control|etag'

# Validation request (304 expected)
curl -s -H "If-None-Match: \"abc123\"" -o /dev/null -w "%{http_code}\n" https://api.your-app.test/static/app.js

# Hit rate
redis-cli INFO stats | grep -E 'keyspace_hits|keyspace_misses'
```

## Invalidation patterns

- Cache-aside: write-through on read, DEL on write
- Versioned keys: key = data:users:v2 (avoids invalidation)
- Time-based: short TTL for hot data, long TTL for cold

## Testing

- Run the same request twice; second should be faster
- Verify 304 responses for conditional requests

## Best practices

- Always set TTL; unbounded caches grow forever
- Cache by canonical key (normalized URL/query)
- Measure hit ratio; < 70% may mean poor key design
- Never cache user-specific responses without private/no-store

## Capabilities

### redis-cache
Cache values in Redis with TTLs.

**Commands:**
- `redis-cli SET mykey "hello" EX 60`
- `redis-cli GET mykey`
- `redis-cli TTL mykey`
- `redis-cli DEL mykey`
- `redis-cli MSET user:1 '{"id":1}' user:2 '{"id":2}'`

**Examples:**
- redis-cli SET cache:users:page:1 '[...]' EX 300
- redis-cli GET cache:users:page:1
- redis-cli -3 SETNX cache:lock:order:42 1 EX 30

### http-caching
Control browser/proxy caching with headers.

**Commands:**
- `curl -sI https://api.your-app.test/static/app.js | grep -i cache-control`
- `curl -s -H "Cache-Control: max-age=0" -o /dev/null -w "%{http_code} %{time_total}\n" https://api.your-app.test/static/app.js`
- `curl -s -H "If-Modified-Since: $(date -R -d '1 day ago')" -o /dev/null -w "%{http_code}\n" https://api.your-app.test/static/app.js`
- `curl -s -I -H "Cache-Control: no-cache" https://api.your-app.test/api/users`

**Examples:**
- curl -sI https://api.your-app.test/static/app.js | grep -iE 'cache-control|etag|age'
- curl -s -H "If-None-Match: \"abc123\"" -o /dev/null -w "%{http_code}\n" https://api.your-app.test/static/app.js
- curl -s -o /dev/null -w "%{http_code} %{time_total}\n" https://api.your-app.test/static/app.js

### cache-stats
Measure hit rates and invalidate selectively.

**Commands:**
- `redis-cli INFO stats | grep -E 'keyspace_hits|keyspace_misses'`
- `redis-cli --scan --pattern 'cache:users:*' | wc -l`
- `varnishstat | grep -E 'MAIN.cache_hit|MAIN.cache_miss'`
- `curl -s https://api.your-app.test/static/app.js -o /dev/null -w "%{http_code}\n" -H "Cache-Control: max-age=0"`

**Examples:**
- redis-cli INFO stats | grep -E 'keyspace_hits|keyspace_misses'
- redis-cli --scan --pattern 'cache:users:*' | head -20
- varnishstat | grep -E 'hit_ratio|MAIN.cache_hit'
