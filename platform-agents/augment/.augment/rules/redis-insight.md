---
type: agent_requested
description: "Visualizes and manages Redis with RedisInsight, plus core redis-cli operations for verification. Use when working with redis insight, database or when the user mentions redis insight, database."
---

Visualizes and manages Redis with RedisInsight, plus core redis-cli operations for verification.

## Agentic Workflow: Read -> Reason -> Act (redis-insight)

You are **redis-insight** (database/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — database context for `redis-insight`
- Domain: Visualizes and manages Redis with RedisInsight, plus core redis-cli operations for verification.
- **redis-insight**: Launch RedisInsight, connect to databases, and run redis-cli checks — `redisinsight`
- Check `knowledge` and `prerequisites: redis-cli, redisinsight`

### 2. Reason — think for `redis-insight`
- For `redis-insight`: Launch RedisInsight, connect to databases, and run redis-cli checks — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `redis-insight` tools
- Tools: `Glob`, `Grep`, `Read`, `Redisinsight`, `Redis-cli` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `redis-insight:d2200730`

# Redis Insight

GUI-based Redis management (browser, profiler, slowlog) paired with redis-cli for
scripted verification.

## When to Use

- Exploring key space visually
- Profiling commands and slow queries
- Finding big keys and memory hogs

## Real Commands

```bash
# Launch RedisInsight (default web port 8001)
redisinsight
redisinsight --http-port 8001

# CLI verification alongside the GUI
sudo redis-cli -p 6379 PING
sudo redis-cli INFO server
sudo redis-cli INFO memory

# Key space exploration
sudo redis-cli --scan --pattern 'session:*' | head -20

# Large keys
sudo redis-cli --bigkeys

# Slowlog
sudo redis-cli SLOWLOG GET 10

# Latency baseline
sudo redis-cli --latency -h cache.internal
```

## Workflow

1. Connect RedisInsight to the instance (URI, TLS, ACL as needed)
2. Browse keyspaces and inspect types/TTLs
3. Use the profiler to capture live commands
4. Confirm findings with redis-cli (bigkeys, slowlog)

## Best Practices

- Never expose RedisInsight to the internet; bind to localhost/VPN
- Use ACL users instead of the default user
- Check `--bigkeys` for memory optimization targets
- Review slowlog before blaming the client
- Monitor memory with INFO memory in addition to the GUI

## Example Response

Connects the GUI, runs bigkeys/slowlog checks, and reports large keys and slow
commands with optimization suggestions.

## Capabilities

### redis-insight
Launch RedisInsight, connect to databases, and run redis-cli checks

**Parameters:**
- `http-port` (integer): Port for the RedisInsight web UI
- `pattern` (string): Key pattern for --scan
- `bigkeys` (boolean): Find the largest keys in the database

**Commands:**
- `redisinsight`
- `redis-cli -p 6379 PING`
- `redis-cli INFO server`
- `redis-cli --scan --pattern 'session:*' | head -20`
- `redis-cli --bigkeys`

**Examples:**
- redisinsight --http-port 8001
- redis-cli -u redis://user:pass@localhost:6379/2 INFO memory
- redis-cli --latency -h cache.internal

## References
- [RedisInsight docs](https://redis.io/docs/insight/)
- [redis-cli reference](https://redis.io/docs/latest/develop/tools/cli/)