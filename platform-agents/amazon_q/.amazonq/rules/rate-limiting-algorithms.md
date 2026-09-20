# Rate Limiting Algorithms

Rate limiting algorithms: token bucket, leaky bucket, fixed window, sliding window — implementation and tuning.

## Instructions

# Rate Limiting Algorithms

Choose and implement the right algorithm: token bucket, leaky bucket, or sliding window.

## What this skill does

- Implements token bucket in Lua/Redis
- Configures nginx leaky-bucket limiting
- Tunes burst and refill

## When to use

- Designing a rate limiter from scratch
- Explaining bursts and smoothness trade-offs

## Real commands

```bash
# Token bucket via Redis Lua
redis-cli --eval token_bucket.lua mykey , 10 1 5

# nginx leaky bucket
nginx -t && nginx -s reload

# Verify status codes
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/api
ab -n 200 -c 20 http://localhost:8080/api
```

## nginx config

```nginx
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
location /api {
    limit_req zone=api burst=20 nodelay;
}
```

## Token bucket Lua sketch

```lua
local key, rate, burst, cost = KEYS[1], tonumber(ARGV[1]), tonumber(ARGV[2]), tonumber(ARGV[3])
local t = redis.call('GET', key..':t') or 0
local tokens = tonumber(redis.call('GET', key..':n') or burst)
-- refill per elapsed time, then spend
```

## Algorithm cheat sheet

- Token bucket: allows bursts up to capacity
- Leaky bucket: smooths rate, no bursts
- Fixed window: simple, bursty at boundaries
- Sliding window: smooth, memory-heavy

## Best practices

- Use Lua in Redis for atomicity
- Prefer burst + nodelay for APIs with spikes
- Test boundaries with ab/curl status codes

## Capabilities

### rate-limit-algorithms
Implement token bucket and sliding window algorithms, and configure nginx burst handling.

**Commands:**
- `redis-cli --eval token_bucket.lua mykey, , 10 1 5`
- `redis-cli EVALSHA $(redis-cli SCRIPT LOAD "$(cat token_bucket.lua)") 1 mykey 10 1 5`
- `nginx -t`
- `nginx -s reload`
- `curl -s -o /dev/null -w "%{http_code}\n" -X POST http://localhost:8080/api`

**Examples:**
- redis-cli --eval token_bucket.lua user:7 , 10 1 5
- ab -n 200 -c 20 http://localhost:8080/api
- curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/api