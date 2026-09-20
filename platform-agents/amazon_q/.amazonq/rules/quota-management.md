Enforce per-consumer request caps with Redis-backed counters, quota middleware, and 429 responses carrying retry metadata.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `redis-cli INCR user:42:requests`
- Check `knowledge` references and prerequisites before proceeding

### 2. Reason
Analyze and plan:
- Compare current state vs desired state (drift, checksums, policy)
- Evaluate trust, compatibility, and risk: use `kdesk trust` and `kdesk doctor` patterns
- Decide: which capabilities/tools are needed, which can be skipped

### 3. Act
Execute with guards:
- Run only `allowed-tools` (see frontmatter); use `safe_path` for writes
- Prefer `Bash` with explicit binaries (`curl`, `kubectl`, `kdesk`) over generic shell
- Record evidence: file paths, checksums, and tool outputs for verification

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