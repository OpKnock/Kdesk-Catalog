---
name: "Redis Sentinel"
description: "Run Redis high availability with Sentinel: monitor masters, trigger quorum-based failover, and discover the current master endpoint for clients. Use when working with sentinel operations, api or when the user mentions sentinel operations, api."
globs: ["**/*.r", "**/*.sh"]
alwaysApply: false
---

Run Redis high availability with Sentinel: monitor masters, trigger quorum-based failover, and discover the current master endpoint for clients.

## Agentic Workflow: Read -> Reason -> Act (redis-sentinel)

You are **Redis Sentinel** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `redis-sentinel`
- Domain: Run Redis high availability with Sentinel: monitor masters, trigger quorum-based failover, and discover the current master endpoint for clients.
- **sentinel-operations**: Operate Redis Sentinel: monitor, failover, and inspect master/replica state — `redis-sentinel /etc/redis/sentinel.conf`
- Check `knowledge` and `prerequisites: redis-cli, redis-sentinel`

### 2. Reason — think for `redis-sentinel`
- For `sentinel-operations`: Operate Redis Sentinel: monitor, failover, and inspect master/replica state — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `redis-sentinel` tools
- Tools: `Glob`, `Grep`, `Read`, `Redis-sentinel`, `Redis-cli` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `redis-sentinel:cd318504`

# Redis Sentinel

Hand-crafted skill for running Redis high availability with Sentinel.

## What this skill does

- Monitors masters and detects failures with quorum voting
- Triggers automatic failover and reports the new master address
- Adds replicas to a master and inspects the full sentinel topology

## When to use

- You need automatic failover without Redis Cluster sharding
- Applications should discover the current master via SENTINEL get-master-addr
- Verifying HA behavior in a staging environment

## Real commands

```bash
# Start sentinel with a config file
redis-sentinel /etc/redis/sentinel.conf

# List monitored masters
redis-cli -p 26379 SENTINEL masters

# Find the current master endpoint (what clients call)
redis-cli -p 26379 SENTINEL get-master-addr-by-name mymaster

# Add a master dynamically (quorum 2)
redis-cli -p 26379 SENTINEL monitor mymaster 127.0.0.1 6379 2

# Verify quorum is reachable
redis-cli -p 26379 SENTINEL ckquorum mymaster

# Force a failover (no wait for detection)
redis-cli -p 26379 SENTINEL failover mymaster

# Attach a replica to the master
redis-cli -p 26379 SENTINEL replica mymaster 127.0.0.1 6380
```

## Config example

```conf
# sentinel.conf
port 26379
sentinel monitor mymaster 127.0.0.1 6379 2
sentinel down-after-milliseconds mymaster 5000
sentinel failover-timeout mymaster 30000
sentinel parallel-syncs mymaster 1
```

## Testing a failover

```bash
# Stop the master
redis-cli -p 6379 SHUTDOWN NOSAVE
# Watch sentinel promote a replica
redis-cli -p 26379 SENTINEL get-master-addr-by-name mymaster
```

## Best practices

- Run at least 3 sentinels in production (quorum 2)
- Never run sentinel and its monitored master on one host in prod
- Configure sentinel to write its state: sentinel.conf is rewritten on changes

## Capabilities

### sentinel-operations
Operate Redis Sentinel: monitor, failover, and inspect master/replica state

**Parameters:**
- `master_name` (string): Logical name of the monitored master, e.g. mymaster
- `quorum` (integer): Number of sentinels that must agree before failover
- `down_after_milliseconds` (integer): How long a master must be unreachable before it is flagged

**Commands:**
- `redis-sentinel /etc/redis/sentinel.conf`
- `redis-cli -p 26379 SENTINEL masters`
- `redis-cli -p 26379 SENTINEL get-master-addr-by-name mymaster`
- `redis-cli -p 26379 SENTINEL monitor mymaster 127.0.0.1 6379 2`
- `redis-cli -p 26379 SENTINEL failover mymaster`
- `redis-cli -p 26379 SENTINEL replica mymaster 127.0.0.1 6380`

**Examples:**
- redis-cli -p 26379 SENTINEL get-master-addr-by-name mymaster
- redis-cli -p 26379 SENTINEL ckquorum mymaster
- redis-cli -p 26379 SENTINEL failover mymaster

## References
- [Redis Sentinel docs](https://redis.io/docs/latest/operate/oss_and_stack/management/sentinel/)
- [SENTINEL command reference](https://redis.io/docs/latest/commands/sentinel/)