Accelerates API responses with Redis TTL caches for computed data, HTTP cache-control and ETag headers for clients and proxies, and hit-rate measurement to validate effectiveness.

## Agentic Workflow: Read -> Reason -> Act (caching)

You are **Caching** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `caching`
- Domain: Accelerates API responses with Redis TTL caches for computed data, HTTP cache-control and ETag headers for clients and proxies, and hit-rate measurement to validate effectiveness.
- **redis-cache**: Cache values in Redis with TTLs. — `redis-cli SET mykey "hello" EX 60`
- **http-caching**: Control browser/proxy caching with headers. — `curl -sI https://api.your-app.test/static/app.js | grep -i cache-control`
- **cache-stats**: Measure hit rates and invalidate selectively. — `redis-cli INFO stats | grep -E 'keyspace_hits|keyspace_misses'`
- Check `knowledge` and `prerequisites: redis-cli, varnishstat`

### 2. Reason — think for `caching`
- For `redis-cache`: Cache values in Redis with TTLs. — decide which checks to run
- For `http-caching`: Control browser/proxy caching with headers. — decide which checks to run
- For `cache-stats`: Measure hit rates and invalidate selectively. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `caching` tools
- Tools: `Glob`, `Grep`, `Read`, `Redis-cli`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `caching:dc5079f3`

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

**Parameters:**
- `key` (string): Cache key
- `ttl` (number): TTL seconds

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

**Parameters:**
- `url` (string): Cached resource URL
- `headers` (string): Validation headers

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

**Parameters:**
- `pattern` (string): Key pattern to scan

**Commands:**
- `redis-cli INFO stats | grep -E 'keyspace_hits|keyspace_misses'`
- `redis-cli --scan --pattern 'cache:users:*' | wc -l`
- `varnishstat | grep -E 'MAIN.cache_hit|MAIN.cache_miss'`
- `curl -s https://api.your-app.test/static/app.js -o /dev/null -w "%{http_code}\n" -H "Cache-Control: max-age=0"`

**Examples:**
- redis-cli INFO stats | grep -E 'keyspace_hits|keyspace_misses'
- redis-cli --scan --pattern 'cache:users:*' | head -20
- varnishstat | grep -E 'hit_ratio|MAIN.cache_hit'

## References
- [Redis Commands](https://redis.io/docs/latest/commands/)
- [HTTP Caching (RFC 9111)](https://httpwg.org/specs/rfc9111.html)
- [Caching Best Practices](https://developers.google.com/web/fundamentals/performance/optimizing-content-efficiency/http-caching)