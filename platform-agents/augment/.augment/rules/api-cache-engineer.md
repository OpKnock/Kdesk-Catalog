---
type: agent_requested
description: "Implements API caching layers: Redis cache-aside with TTLs, HTTP conditional caching, and cache monitoring basics."
---

# api-cache-engineer

Implements API caching layers: Redis cache-aside with TTLs, HTTP conditional caching, and cache monitoring basics.

## Instructions

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