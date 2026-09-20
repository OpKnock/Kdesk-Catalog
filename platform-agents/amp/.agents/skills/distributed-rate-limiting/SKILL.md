---
name: "distributed-rate-limiting"
description: "Designs and operates distributed rate limits across API gateways and services using Redis sliding-window counters, with load-test verification."
---

# Distributed Rate Limiting

Designs and operates distributed rate limits across API gateways and services using Redis sliding-window counters, with load-test verification.

## Instructions

# Distributed Rate Limiting

## What this skill does

Distributed rate limiting enforces a consistent request budget across every instance of a service by storing counters in a shared store (Redis). This skill covers counter inspection, headers, and load-test verification.

## When to use

- Enforcing per-client quotas across multiple API gateway replicas
- Debugging unexpected 429 responses on a specific key
- Tuning limits before a public launch

## Real commands

```bash
# Find all live limit counters
redis-cli --scan --pattern 'rl:*' | head -20

# Inspect one bucket
redis-cli GET rl:{client}:{route}:count
redis-cli TTL rl:{client}:{route}:window

# Verify the response headers the client sees
curl -i https://httpbin.org/headers -H 'Authorization: Bearer $TOKEN' | grep -i 'x-ratelimit'

# Load-test the endpoint and count 429s
ab -n 2000 -c 50 https://httpbin.org/get | grep -E 'Requests per second|Failed requests'
```

## Redis sliding window (Lua) example

```lua
-- EVAL script: per-user sliding window
local key = KEYS[1]
local now = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local limit = tonumber(ARGV[3])
redis.call('ZREMRANGEBYSCORE', key, 0, now - window * 1000)
local count = redis.call('ZCARD', key)
if count < limit then
  redis.call('ZADD', key, now, now .. '-' .. math.random(100000))
  redis.call('EXPIRE', key, window * 2)
  return 1
end
return 0
```

## Testing

```bash
# Confirm 429s start after the limit is exhausted
for i in $(seq 1 250); do curl -s -o /dev/null -w '%{http_code}\n' https://httpbin.org/get; done | sort | uniq -c
```

## Best practices

- Return standard headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`.
- Keep Lua scripts atomic and idempotent; test them with `redis-cli --eval`.
- Exclude health checks and internal calls from counting.
- Monitor the Redis instance; a limit-store outage must fail open or closed deliberately.

## Capabilities

### redis-window-limits
Inspect Redis-based rate limit counters, exercise limited endpoints, and measure effective limiting under load.

**Commands:**
- `redis-cli --scan --pattern 'rl:*' | head -20`
- `redis-cli GET rl:{client}:{route}:count`
- `curl -i https://httpbin.org/headers -H 'Authorization: Bearer $TOKEN' | grep -i 'x-ratelimit'`
- `redis-cli TTL rl:{client}:{route}:window`
- `ab -n 2000 -c 50 https://httpbin.org/get | grep -E 'Requests per second|Failed requests'`

**Examples:**
- redis-cli --scan --pattern 'rl:*' | head -20
- curl -i https://httpbin.org/headers | grep -i 'x-ratelimit'
- ab -n 2000 -c 50 https://httpbin.org/get | grep -E 'Requests per second|Failed requests'
