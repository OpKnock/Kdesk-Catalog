---
name: "redis-insight"
description: "Visualizes and manages Redis with RedisInsight, plus core redis-cli operations for verification. Use when working with redis insight, database or when the user mentions redis insight, database."
license: "MIT"
compatibility: "Requires redis-cli, redisinsight."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "database"}
allowed-tools: "Glob Grep Read Bash(redis-cli:*) Bash(redisinsight:*)"
---

Visualizes and manages Redis with RedisInsight, plus core redis-cli operations for verification.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `redisinsight`
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
