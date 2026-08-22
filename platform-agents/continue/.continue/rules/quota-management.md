---
name: "Quota Management"
description: "Enforce per-consumer request caps with Redis-backed counters, quota middleware, and 429 responses carrying retry metadata."
globs: ["**/*.py", "**/*.r", "**/*.sh"]
alwaysApply: false
---

# Quota Management

Enforce per-consumer request caps with Redis-backed counters, quota middleware, and 429 responses carrying retry metadata.

## Instructions

# Quota Management

Quotas cap how many requests each consumer may make, enforced at the API layer.

## What this skill does

- Counts requests per key with Redis
- Checks quota before serving
- Returns 429 with retry info

## When to use

- Per-plan limits for API consumers
- Fairness across tenants

## Real commands

```bash
# Count per user per window
redis-cli INCR user:42:requests
redis-cli EXPIRE user:42:requests 60
redis-cli GET user:42:requests

# Store quota config
redis-cli -n 3 SET quota:user:42 1000

# Verify enforcement
curl -s -o /dev/null -w "%{http_code}\n" -H "X-Api-Key: key-42" http://localhost:8080/api
```

## Check logic (pseudo)

```python
used = redis.incr(f"user:{key}:requests")
if used == 1:
    redis.expire(f"user:{key}:requests", window)
if used > quota(key):
    return 429, {"retry_after": window}
```

## Response headers

- `Retry-After: 60`
- `X-RateLimit-Limit`, `X-RateLimit-Remaining`

## Best practices

- Make INCR+EXPIRE atomic or use the INCR+EXPIRE pattern with care
- Read quotas from a config store, not code
- Expose remaining quota in headers

## Capabilities

### quota-enforcement
Implement per-consumer quotas with Redis counters and enforce them at the API layer.

**Commands:**
- `redis-cli INCR user:42:requests`
- `redis-cli EXPIRE user:42:requests 60`
- `redis-cli GET user:42:requests`
- `redis-cli -n 3 SET quota:user:42 1000`
- `curl -s -o /dev/null -w "%{http_code}\n" -H "X-Api-Key: key-42" http://localhost:8080/api`

**Examples:**
- redis-cli INCR user:42:requests; redis-cli EXPIRE user:42:requests 60
- redis-cli GET user:42:requests
- curl -s -o /dev/null -w "%{http_code}\n" -H "X-Api-Key: key-42" http://localhost:8080/api