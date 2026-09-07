---
name: "redis"
description: "Operates Redis: key management, expiry, transactions, Lua scripting, and benchmarking. Use when working with redis cli, database or when the user mentions redis cli, database."
---

Operates Redis: key management, expiry, transactions, Lua scripting, and benchmarking.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `redis-cli SET user:42 '{"name": "jane"}' EX 3600`
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

# Redis

In-memory data store operations: strings, hashes, lists, sets, TTLs, transactions,
and Lua scripting via redis-cli.

## When to Use

- Caching with TTLs
- Rate limiting and counters
- Queues and leaderboards with list/set commands

## Real Commands

```bash
# Strings with TTL
sudo redis-cli SET user:42 '{"name": "jane"}' EX 3600
sudo redis-cli GET user:42
sudo redis-cli TTL user:42

# Counters
sudo redis-cli INCR page_views
sudo redis-cli INCRBY page_views 5

# Lists / sets
sudo redis-cli LPUSH recent:items item-1
sudo redis-cli LRANGE recent:items 0 4
sudo redis-cli SADD online u1 u2
sudo redis-cli SCARD online

# Hashes
sudo redis-cli HSET user:42 name jane age 34
sudo redis-cli HGETALL user:42

# Scripts
sudo redis-cli EVAL "return redis.call('incr', KEYS[1])" 1 mycounter

# Bulk delete by pattern
sudo redis-cli --scan --pattern 'cache:*' | xargs -r redis-cli DEL

# Benchmark
sudo redis-benchmark -t set,get -n 100000 -c 50 -q
```

## Best Practices

- Always set TTLs for cache keys
- Use SCAN, never KEYS, in production
- Keep scripts pure (no time/random) for replication safety
- Use pipeline/MULTI for batch operations
- Set maxmemory-policy for eviction behavior

## Example Response

Implements the cache/queue pattern, verifies values and TTLs, and benchmarks to
confirm performance targets.

## Capabilities

### redis-cli
Manage keys, data structures, TTLs, and run scripts with redis-cli

**Parameters:**
- `ex` (integer): Expire the key after N seconds (EX)
- `ttl` (string): Key TTL: seconds, millis, or timestamp options
- `benchmark` (boolean): Run redis-benchmark load testing

**Commands:**
- `redis-cli SET user:42 '{"name": "jane"}' EX 3600`
- `redis-cli GET user:42`
- `redis-cli INCR page_views`
- `redis-cli LPUSH recent:items item-1`
- `redis-cli --scan --pattern 'cache:*' | xargs -r redis-cli DEL`

**Examples:**
- redis-cli SADD online_users u1 u2 u3
- redis-cli EVAL "return redis.call('incr', KEYS[1])" 1 counter
- redis-cli --benchmark -n 100000 -c 50 -q

## References
- [Redis commands reference](https://redis.io/docs/latest/commands/)
- [redis-cli docs](https://redis.io/docs/latest/develop/tools/cli/)
