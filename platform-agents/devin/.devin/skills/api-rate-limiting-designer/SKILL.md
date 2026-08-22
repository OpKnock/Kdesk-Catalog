---
name: "api-rate-limiting-designer"
description: "Designs rate limiting algorithms and data models: token bucket, sliding window, fixed window, and Redis-backed counters with Lua atomicity."
---

# api-rate-limiting-designer

Designs rate limiting algorithms and data models: token bucket, sliding window, fixed window, and Redis-backed counters with Lua atomicity.

## Instructions

# API Rate Limiting Designer

Designs rate limiting algorithms.

## What This Skill Does
- Chooses window and bucket algorithms for the workload
- Models counters with Redis primitives
- Ensures atomicity with Lua

## When to Use
- Specifying rate limit behavior before implementation
- Comparing fixed vs sliding window tradeoffs
- Choosing data stores for distributed limits

## Real Commands

```bash
redis-cli INCR rate:user:42
redis-cli EXPIRE rate:user:42 60
redis-cli ZADD rate:user:42 $(date +%s%3N) req-1
redis-cli ZREMRANGEBYSCORE rate:user:42 -inf $(($(date +%s%3N)-60000))
redis-cli ZCARD rate:user:42
```

## Algorithm Guide
- Fixed window: simple, allows boundary bursts (2x limit)
- Sliding window: smooth, keeps per-request timestamps
- Token bucket: permits bursts up to capacity
- Leaky bucket: constant output rate

## Lua Atomic Script

```lua
local c = redis.call('INCR', KEYS[1])
if c == 1 then redis.call('EXPIRE', KEYS[1], ARGV[1]) end
return c
```

## Testing
- Verify boundary bursts with clock-skew tests
- Compare memory use of ZSET vs counter designs
- Test multi-node consistency for distributed APIs

## Best Practices
- Never trust client-supplied identifiers alone
- Add jitter to key TTLs to avoid thundering herds
- Design the 429 response before implementation

## Capabilities

### redis-windows
Model rate limit windows with Redis primitives

**Commands:**
- `redis-cli INCR rate:user:42`
- `redis-cli EXPIRE rate:user:42 60`
- `redis-cli ZADD rate:user:42 $(date +%s%3N) req-1`
- `redis-cli ZREMRANGEBYSCORE rate:user:42 -inf $(($(date +%s%3N)-60000))`
- `redis-cli ZCARD rate:user:42`

**Examples:**
- INCR + EXPIRE implements a fixed window counter
- ZADD with millisecond timestamps tracks sliding windows
- ZREMRANGEBYSCORE prunes expired sliding window entries

### lua-atomicity
Use Lua scripts for atomic check-and-increment

**Commands:**
- `redis-cli --eval ratelimit.lua 1 rate:user:42 , 10 60`
- `redis-cli EVAL 'local c=redis.call("INCR",KEYS[1]); if c==1 then redis.call("EXPIRE",KEYS[1],ARGV[1]) end; return c' 1 rate:user:42 60`
- `redis-cli GET rate:user:42`
- `redis-cli DEL rate:user:42`

**Examples:**
- -cli --help
- -api --help
