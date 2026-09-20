---
name: "redis-streams"
description: "Expert Redis Streams reference covering XADD/XREAD/XRANGE/XREVRANGE basics, ID structure, blocking reads, and range queries suited to event logs and time series data."
type: knowledge
triggers: ["redis-streams", "redis-streams-core"]
---

# Redis Streams

Expert Redis Streams reference covering XADD/XREAD/XRANGE/XREVRANGE basics, ID structure, blocking reads, and range queries suited to event logs and time series data.

## Instructions

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
