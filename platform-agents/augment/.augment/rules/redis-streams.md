---
type: agent_requested
description: "Expert Redis Streams reference covering XADD/XREAD/XRANGE/XREVRANGE basics, ID structure, blocking reads, and range queries suited to event logs and time series data. Use when working with redis streams core, api or when the user mentions redis streams core, api."
---

Expert Redis Streams reference covering XADD/XREAD/XRANGE/XREVRANGE basics, ID structure, blocking reads, and range queries suited to event logs and time series data.

## Agentic Workflow: Read -> Reason -> Act (redis-streams)

You are **Redis Streams** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `redis-streams`
- Domain: Expert Redis Streams reference covering XADD/XREAD/XRANGE/XREVRANGE basics, ID structure, blocking reads, and range queries suited to event logs and time series data.
- **redis-streams-core**: Core Redis Streams operations: append, range read, block, length — `redis-cli XADD temperature:2026-08 * sensor office value 22.5`
- Check `knowledge` and `prerequisites: redis-cli`

### 2. Reason — think for `redis-streams`
- For `redis-streams-core`: Core Redis Streams operations: append, range read, block, length — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `redis-streams` tools
- Tools: `Glob`, `Grep`, `Read`, `Redis-cli` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `redis-streams:7de10cb4`

# Redis Streams

Expert skill for the core Redis Streams data type.

## What this skill does

- Appends field-value entries with XADD and auto-generated IDs
- Reads ranges forward and backward with XRANGE/XREVRANGE
- Blocks for new entries with XREAD and checks stream length

## When to use

- Append-only event logs with per-message timestamps
- Sensor or metrics time series
- Learning streams before moving to consumer groups

## Real commands

```bash
# Append an entry; * lets Redis generate <ms>-<seq> ID
redis-cli XADD temperature:2026-08 * sensor office value 22.5

# All entries, oldest to newest
redis-cli XRANGE temperature:2026-08 - +

# Newest 3 entries
redis-cli XREVRANGE temperature:2026-08 + - COUNT 3

# Entry count
redis-cli XLEN temperature:2026-08

# Block up to 5s for new entries (offset $ = end of stream)
redis-cli XREAD BLOCK 5000 COUNT 2 STREAMS temperature:2026-08 $

# Range by time window: IDs are <ms>-<seq>
redis-cli XRANGE temperature:2026-08 1723000000000-0 1723999999999-0
```

## ID anatomy

- IDs are <milliseconds-time>-<sequence> in UTC
- Same-ms entries get incrementing sequence numbers
- XADD MAXLEN ~ 1000 keeps the stream bounded while appending

## Testing

```bash
redis-cli XADD temperature:2026-08 * sensor lab value 21.0
redis-cli XRANGE temperature:2026-08 - + COUNT 5
redis-cli XLEN temperature:2026-08
```

## Best practices

- Use * to let Redis generate monotonic IDs
- Give streams descriptive keys since IDs encode time already
- Prefer MAXLEN trimming at insert time for hot streams

## Capabilities

### redis-streams-core
Core Redis Streams operations: append, range read, block, length

**Parameters:**
- `stream` (string): Stream key name
- `count` (integer): Number of entries to return
- `block` (integer): Blocking read timeout in milliseconds

**Commands:**
- `redis-cli XADD temperature:2026-08 * sensor office value 22.5`
- `redis-cli XRANGE temperature:2026-08 - +`
- `redis-cli XREVRANGE temperature:2026-08 + - COUNT 3`
- `redis-cli XLEN temperature:2026-08`
- `redis-cli XREAD BLOCK 5000 COUNT 2 STREAMS temperature:2026-08 $`

**Examples:**
- redis-cli XRANGE temperature:2026-08 - + COUNT 5
- redis-cli XRANGE temperature:2026-08 1723000000000-0 1723999999999-0
- redis-cli XREAD BLOCK 5000 COUNT 2 STREAMS temperature:2026-08 $

## References
- [Redis Streams data type](https://redis.io/docs/latest/develop/data-types/streams/)
- [XADD command](https://redis.io/docs/latest/commands/xadd/)