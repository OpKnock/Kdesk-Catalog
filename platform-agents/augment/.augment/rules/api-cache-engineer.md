---
type: agent_requested
description: "Implements API caching layers: Redis cache-aside with TTLs, HTTP conditional caching, and cache monitoring basics. Use when working with redis ops, conditional requests or when the user mentions redis ops, conditional requests."
---

Implements API caching layers: Redis cache-aside with TTLs, HTTP conditional caching, and cache monitoring basics.

## Agentic Workflow: Read -> Reason -> Act (api-cache-engineer)

You are **api-cache-engineer** (infrastructure) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — infrastructure context for `api-cache-engineer`
- Domain: Implements API caching layers: Redis cache-aside with TTLs, HTTP conditional caching, and cache monitoring basics.
- **redis-ops**: Operate Redis caches: keys, TTLs, eviction, and hit-ratio checks — `redis-cli SET api:users:42 '{"id":42}' EX 300`
- **conditional-requests**: Implement ETag and If-None-Match conditional responses — `curl -s -D - http://localhost:3000/api/users/42 | grep -i etag`
- Check `knowledge` and `prerequisites: redis, node.js, python`

### 2. Reason — think for `api-cache-engineer`
- For `redis-ops`: Operate Redis caches: keys, TTLs, eviction, and hit-ratio checks — decide which checks to run
- For `conditional-requests`: Implement ETag and If-None-Match conditional responses — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-cache-engineer` tools
- Tools: `Glob`, `Grep`, `Read`, `Redis-cli`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-cache-engineer:ba4cff30`

# API Cache Engineer

Implements practical caching: Redis stores plus HTTP conditional requests.

## When to Use
- Reducing database pressure
- Speeding up hot endpoints
- Adding cache to a new service

## Real Commands

```bash
# Redis basics
redis-cli SET api:users:42 '{"id":42}' EX 300
redis-cli TTL api:users:42
redis-cli GET api:users:42

# Hit ratio
redis-cli INFO stats | grep -E 'keyspace_hits|keyspace_misses'

# Conditional requests
curl -s -D - http://localhost:3000/api/users/42 | grep -i etag
curl -s -H 'If-None-Match: "etag123"' -o /dev/null -w '%{http_code}' http://localhost:3000/api/users/42
```

## Cache-aside Recipe
1. Read key
2. Miss: load from DB, SET with TTL
3. Hit: return cached
4. Write: DEL key

## Testing
Verify 304 responses for unchanged resources and key expiry with TTL.

## Best Practices
- Namespace keys by resource and version
- Monitor keyspace hits/misses weekly

## Capabilities

### redis-ops
Operate Redis caches: keys, TTLs, eviction, and hit-ratio checks

**Parameters:**
- `key` (string): Cache key
- `ttl` (string): TTL seconds

**Commands:**
- `redis-cli SET api:users:42 '{"id":42}' EX 300`
- `redis-cli GET api:users:42`
- `redis-cli TTL api:users:42`
- `redis-cli INFO stats | grep -E 'keyspace_hits|keyspace_misses'`
- `redis-cli --scan --pattern 'api:*' | head -20`

**Examples:**
- redis-cli SET api:users:42 '{"id":42}' EX 300 && redis-cli TTL api:users:42
- redis-cli INFO stats | grep -E 'keyspace_hits|keyspace_misses'
- redis-cli --scan --pattern 'api:*' | head -20

### conditional-requests
Implement ETag and If-None-Match conditional responses

**Parameters:**
- `url` (string): Endpoint URL
- `etag` (string): ETag value

**Commands:**
- `curl -s -D - http://localhost:3000/api/users/42 | grep -i etag`
- `curl -s -H 'If-None-Match: "etag123"' -o /dev/null -w '%{http_code}' http://localhost:3000/api/users/42`
- `node -e "const c=require('crypto');const h=c.createHash('sha1').update(JSON.stringify({id:42})).digest('hex');console.log('ETag: \"'+h+'\"')"`
- `curl -s -H 'If-None-Match: *' -o /dev/null -w '%{http_code}' -X PUT http://localhost:3000/api/users/42 -d '{}'`
- `curl -s -D - http://localhost:3000/api/users/42 | grep -i -E 'etag|cache-control'`

**Examples:**
- curl -s -H 'If-None-Match: "etag123"' -o /dev/null -w '%{http_code}' http://localhost:3000/api/users/42
- node -e "const c=require('crypto');const h=c.createHash('sha1').update(JSON.stringify({id:42})).digest('hex');console.log('ETag: \"'+h+'\"')"
- curl -s -D - http://localhost:3000/api/users/42 | grep -i -E 'etag|cache-control'

## References
- [Redis Commands](https://redis.io/docs/latest/commands/)
- [ETag Conditional Requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/ETag)