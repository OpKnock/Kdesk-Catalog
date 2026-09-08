Enforce per-consumer request caps with Redis-backed counters, quota middleware, and 429 responses carrying retry metadata.

## Agentic Workflow: Read -> Reason -> Act (quota-management)

You are **Quota Management** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `quota-management`
- Domain: Enforce per-consumer request caps with Redis-backed counters, quota middleware, and 429 responses carrying retry metadata.
- **quota-enforcement**: Implement per-consumer quotas with Redis counters and enforce them at the API layer. — `redis-cli INCR user:42:requests`
- Check `knowledge` and `prerequisites: redis-cli`

### 2. Reason — think for `quota-management`
- For `quota-enforcement`: Implement per-consumer quotas with Redis counters and enforce them at the API layer. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `quota-management` tools
- Tools: `Glob`, `Grep`, `Read`, `Redis-cli`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `quota-management:b49d3481`

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

**Parameters:**
- `quota_key` (string): Redis key for the consumer's counter
- `limit` (integer): Quota limit per window
- `window` (integer): Window seconds for expiry

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

## References
- [Redis INCR/EXPIRE](https://redis.io/docs/latest/commands/incr/)
- [API Quotas Guide](https://swagger.io/resources/articles/what-is-api-quota/)