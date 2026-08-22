# Redis Streams Management

Administer Redis Streams in production: inspect with XINFO, manage consumer group lifecycle, enforce retention with XTRIM, and remove stale entries.

## Instructions

# Redis Streams Management

Hand-crafted skill for administering Redis Streams in production.

## What this skill does

- Inspects stream internals: length, radix-tree nodes, consumer groups
- Creates, destroys, and deletes consumer groups
- Enforces retention with XTRIM MAXLEN or MINID policies

## When to use

- Capacity planning and debugging memory growth from streams
- Renaming or retiring consumer groups after deployments
- Cleaning up test data or stray entries

## Real commands

```bash
# Full stream metadata
redis-cli XINFO STREAM orders

# Per-group stats: pending, consumers, last-delivered-id
redis-cli XINFO GROUPS orders

# Create a group; MKSTREAM creates the key if missing
redis-cli XGROUP CREATE orders workers $ MKSTREAM

# Per-consumer pending counts
redis-cli XINFO CONSUMERS orders workers

# Trim to roughly 1000 newest entries
redis-cli XTRIM orders MAXLEN ~ 1000

# Trim by ID: drop everything older than a timestamp
redis-cli XTRIM orders MINID 1699999999999-0

# Delete specific entries
redis-cli XDEL orders 1699999999999-0

# Remove a group
redis-cli XGROUP DESTROY orders oldgroup
```

## Retention policy

```bash
# Cron-safe: keep only the last 100k entries
redis-cli XTRIM orders MAXLEN ~ 100000
```

## Testing

```bash
redis-cli XADD orders * sku A1
redis-cli XINFO GROUPS orders
redis-cli XTRIM orders MAXLEN ~ 5
redis-cli XLEN orders
```

## Best practices

- Use the ~ flag so trimming is O(1) instead of exact
- Prefer MINID over MAXLEN when entries carry business timestamps
- Check XINFO STREAM length before trimming to avoid deleting live data

## Capabilities

### stream-administration
Administer streams: info, groups, trim, delete entries, set IDs

**Commands:**
- `redis-cli XINFO STREAM orders`
- `redis-cli XINFO GROUPS orders`
- `redis-cli XGROUP CREATE orders workers $ MKSTREAM`
- `redis-cli XTRIM orders MAXLEN ~ 1000`
- `redis-cli XDEL orders 1699999999999-0`
- `redis-cli XGROUP DESTROY orders oldgroup`

**Examples:**
- redis-cli XINFO STREAM orders
- redis-cli XTRIM orders MINID 1699999999999-0
- redis-cli XGROUP DESTROY orders workers