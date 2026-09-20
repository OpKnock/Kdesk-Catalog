---
name: "caching-patterns-engineer"
description: "Implements battle-tested caching patterns: cache-aside, read/write-through, stampede protection, and distributed locks."
type: knowledge
triggers: ["caching-patterns-engineer", "pattern-implementation", "stampede-protection"]
---

# caching-patterns-engineer

Implements battle-tested caching patterns: cache-aside, read/write-through, stampede protection, and distributed locks.

## Instructions

# Caching Patterns Engineer

Implement reliable caching patterns.

## When to Use

- Adding caching to existing code paths safely
- Fixing cache coherence bugs (stale data, stampedes)
- Building distributed locking around expensive work

## Patterns

- Cache-aside: read cache; on miss load + populate; invalidate on write
- Read-through: cache loads missing values from the store itself
- Write-through: update cache and store together
- Write-behind: update store asynchronously after cache write
- Stampede lock: only one process regenerates an expired key

## Commands

```bash
# Atomic set-if-absent with TTL
redis-cli SET user:1 "data" EX 60 NX

# Stampede lock
redis-cli SETNX lock:regen:popular-key "1" EX 10

# Inspect TTL
redis-cli ttl popular-key
redis-cli pttl popular-key

# Invalidate
redis-cli unlink user:1
```

## Python Cache-Aside

```python
import redis

r = redis.Redis()

def get_user(uid):
    key = f"user:{uid}"
    cached = r.get(key)
    if cached:
        return cached
    lock = r.set(f"lock:{key}", "1", ex=5, nx=True)
    if lock:
        data = fetch_from_db(uid)
        r.set(key, data, ex=300)
    else:
        time.sleep(0.05)
        return r.get(key)
    return data
```

## Best Practices

- Use SET NX EX for atomic stampede locks
- Validate before caching: never cache errors as success
- Invalidate on write with unlink for large values
- Keep TTLs short enough that drift self-heals
- Measure hit rate and latency before/after changes

## Capabilities

### pattern-implementation
Implement caching patterns in code with Redis.

**Commands:**
- `pip install redis`
- `npm install ioredis`
- `redis-cli set user:1 "data" EX 60 NX`
- `redis-cli setnx lock:task:1 "1" EX 30`

**Examples:**
- redis-cli SET user:1 "data" EX 60 NX
- redis-cli GETSET lock:task:1 "1"
- python -c "import redis; r=redis.Redis(); print(r.set('k','v',ex=60,nx=True))"

### stampede-protection
Prevent thundering herd on cache expiry.

**Commands:**
- `redis-cli setnx lock:regen:popular-key "1" EX 10`
- `redis-cli ttl popular-key`
- `redis-cli get popular-key`
- `redis-cli pttl popular-key`

**Examples:**
- redis-cli setnx lock:regen:report "1" EX 15
- redis-cli ttl report
