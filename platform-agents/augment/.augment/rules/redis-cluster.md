---
type: agent_requested
description: "Operate Redis Cluster topologies: create multi-node clusters, verify slot coverage, reshard, and manage replicas with redis-cli cluster commands. Use when working with redis cluster admin, api or when the user mentions redis cluster admin, api."
---

Operate Redis Cluster topologies: create multi-node clusters, verify slot coverage, reshard, and manage replicas with redis-cli cluster commands.

## Agentic Workflow: Read -> Reason -> Act (redis-cluster)

You are **Redis Cluster** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `redis-cluster`
- Domain: Operate Redis Cluster topologies: create multi-node clusters, verify slot coverage, reshard, and manage replicas with redis-cli cluster commands.
- **redis-cluster-admin**: Create, inspect, and rebalance Redis Cluster topologies with redis-cli cluster commands — `redis-cli -c -p 7000 cluster info`
- Check `knowledge` and `prerequisites: redis-cli`

### 2. Reason — think for `redis-cluster`
- For `redis-cluster-admin`: Create, inspect, and rebalance Redis Cluster topologies with redis-cli cluster commands — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `redis-cluster` tools
- Tools: `Glob`, `Grep`, `Read`, `Redis-cli` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `redis-cluster:e8913ad1`

# Redis Cluster

Hand-crafted skill for operating Redis Cluster topologies from the command line.

## What this skill does

- Boots a 6-node cluster (3 masters, 3 replicas) with redis-cli --cluster create
- Verifies that all 16384 hash slots are covered and master-replica links are healthy
- Adds nodes and reshards slots between masters without manual slot math

## When to use

- Setting up a production Redis Cluster from scratch
- Debugging CLUSTERDOWN or "Slot X already busy" errors
- Planning slot migrations before a maintenance window

## Real commands

```bash
# Create a cluster from six nodes on ports 7000-7005
redis-cli --cluster create 127.0.0.1:7000 127.0.0.1:7001 127.0.0.1:7002 127.0.0.1:7003 127.0.0.1:7004 127.0.0.1:7005 --cluster-replicas 1

# Health check: reports slot coverage and link status
redis-cli --cluster check 127.0.0.1:7000

# Cluster-wide stats
redis-cli -c -p 7000 cluster info

# Node table: id, ip:port, flags, slots
redis-cli -c -p 7000 cluster nodes

# Add a fresh node, then move 1000 slots onto it
redis-cli --cluster add-node 127.0.0.1:7006 127.0.0.1:7000
redis-cli --cluster reshard 127.0.0.1:7000 --cluster-from 8a4f9c --cluster-to 7b2cd1 --cluster-slots 1000 --cluster-yes
```

## Config example

Start six isolated instances:

```bash
for port in 7000 7001 7002 7003 7004 7005; do
  mkdir -p /data/redis/$port
  redis-server --port $port --cluster-enabled yes     --cluster-config-file nodes-$port.conf     --appendonly yes --dir /data/redis/$port --daemonize yes
done
```

## Testing

```bash
redis-cli -c -p 7000 set foo bar
redis-cli -c -p 7000 get foo
redis-cli --cluster check 127.0.0.1:7000
```

## Best practices

- Always run `--cluster check` before and after resharding
- Keep a replication factor of at least 1 in production
- Use hash tags like {user:42} to pin related keys to the same slot
- If partial availability is acceptable, set cluster-require-full-coverage no

## Capabilities

### redis-cluster-admin
Create, inspect, and rebalance Redis Cluster topologies with redis-cli cluster commands

**Parameters:**
- `cluster-replicas` (integer): Number of replicas per master when creating a cluster
- `cluster-slots` (integer): Number of hash slots to move during resharding
- `cluster-yes` (boolean): Auto-answer the resharding confirmation prompts

**Commands:**
- `redis-cli -c -p 7000 cluster info`
- `redis-cli --cluster create 127.0.0.1:7000 127.0.0.1:7001 127.0.0.1:7002 127.0.0.1:7003 127.0.0.1:7004 127.0.0.1:7005 --cluster-replicas 1`
- `redis-cli --cluster add-node 127.0.0.1:7006 127.0.0.1:7000`
- `redis-cli --cluster reshard 127.0.0.1:7000 --cluster-from 8a4f9c --cluster-to 7b2cd1 --cluster-slots 1000 --cluster-yes`
- `redis-cli --cluster check 127.0.0.1:7000`
- `redis-cli -p 7000 cluster nodes`

**Examples:**
- redis-cli --cluster check 127.0.0.1:7000
- redis-cli -c -p 7000 cluster info
- redis-cli --cluster reshard 127.0.0.1:7000 --cluster-from 8a4f9c --cluster-to 7b2cd1 --cluster-slots 1000 --cluster-yes

## References
- [Redis Cluster Tutorial](https://redis.io/docs/latest/operate/oss_and_stack/management/scaling/)
- [CLUSTER command reference](https://redis.io/docs/latest/commands/cluster-info/)