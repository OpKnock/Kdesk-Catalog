---
name: "redis-streams-consumer"
description: "Consume Redis Streams with consumer groups: read via XREADGROUP, acknowledge with XACK, inspect pending entries, and recover stalled work with XCLAIM. Use when working with stream consumer groups, api or when the user mentions stream consumer groups, api."
license: "MIT"
compatibility: "Requires redis-cli."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(redis-cli:*)"
---

Consume Redis Streams with consumer groups: read via XREADGROUP, acknowledge with XACK, inspect pending entries, and recover stalled work with XCLAIM.

## Agentic Workflow: Read -> Reason -> Act (redis-streams-consumer)

You are **Redis Streams Consumer** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `redis-streams-consumer`
- Domain: Consume Redis Streams with consumer groups: read via XREADGROUP, acknowledge with XACK, inspect pending entries, and recover stalled work with XCLAIM.
- **stream-consumer-groups**: Consume streams with consumer groups: read, ack, inspect pending, claim — `redis-cli XREADGROUP GROUP pay-group c1 COUNT 5 STREAMS orders:pay >`
- Check `knowledge` and `prerequisites: redis-cli`

### 2. Reason — think for `redis-streams-consumer`
- For `stream-consumer-groups`: Consume streams with consumer groups: read, ack, inspect pending, claim — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `redis-streams-consumer` tools
- Tools: `Glob`, `Grep`, `Read`, `Redis-cli` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `redis-streams-consumer:8f12f434`

# Redis Streams - Consumer Groups

Hand-crafted skill for reliable stream consumption with Redis consumer groups.

## What this skill does

- Reads new entries with XREADGROUP and the > special ID
- Acknowledges processed entries so they leave the PEL (pending list)
- Inspects pending entries and reclaims stale work with XCLAIM/ XAUTOCLAIM

## When to use

- Building at-least-once processing on top of Redis Streams
- Debugging unacked messages after a consumer crash
- Rebalancing work between consumers

## Real commands

```bash
# Read up to 5 new entries for consumer c1
redis-cli XREADGROUP GROUP pay-group c1 COUNT 5 STREAMS orders:pay >

# Acknowledge processed IDs
redis-cli XACK orders:pay pay-group 1699999999999-0

# Show pending entries per consumer
redis-cli XPENDING orders:pay pay-group
redis-cli XPENDING orders:pay pay-group - + 10 c2

# Claim entries idle > 60s for consumer c2
redis-cli XCLAIM orders:pay pay-group c2 60000 1699999999999-0

# Auto-claim loop (idle > 60s, start from 0-0)
redis-cli XAUTOCLAIM orders:pay pay-group c2 60000 0-0

# Read a consumer's own history
redis-cli XREADGROUP GROUP pay-group c1 COUNT 10 STREAMS orders:pay 0
```

## Delivery semantics

- Entries are handed to one group member only; unacked IDs stay pending
- A crashed consumer leaves pending entries that XCLAIM reassigns
- Always XACK after processing, otherwise the PEL grows forever

## Testing

```bash
redis-cli XADD orders:pay * amount 10
redis-cli XREADGROUP GROUP pay-group c1 COUNT 1 STREAMS orders:pay >
redis-cli XPENDING orders:pay pay-group
```

## Best practices

- Read with the > ID for new work, with 0 for replaying your own history
- Set an idle threshold based on your processing SLA before claiming
- Make the claim operation idempotent: process only if you still own the entry

## Capabilities

### stream-consumer-groups
Consume streams with consumer groups: read, ack, inspect pending, claim

**Parameters:**
- `group` (string): Consumer group name to read from
- `consumer` (string): Consumer name within the group
- `count` (integer): Maximum number of entries to read

**Commands:**
- `redis-cli XREADGROUP GROUP pay-group c1 COUNT 5 STREAMS orders:pay >`
- `redis-cli XACK orders:pay pay-group 1699999999999-0`
- `redis-cli XPENDING orders:pay pay-group`
- `redis-cli XCLAIM orders:pay pay-group c2 60000 1699999999999-0`
- `redis-cli XREADGROUP GROUP pay-group c1 COUNT 10 STREAMS orders:pay 0`

**Examples:**
- redis-cli XREADGROUP GROUP pay-group c1 COUNT 5 STREAMS orders:pay >
- redis-cli XPENDING orders:pay pay-group - + 10 c2
- redis-cli XAUTOCLAIM orders:pay pay-group c2 60000 0-0

## References
- [Redis Streams intro](https://redis.io/docs/latest/develop/data-types/streams/)
- [XREADGROUP command](https://redis.io/docs/latest/commands/xreadgroup/)
