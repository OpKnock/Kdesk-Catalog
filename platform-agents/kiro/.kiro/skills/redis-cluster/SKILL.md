---
name: "redis-cluster"
description: "Operate Redis Cluster topologies: create multi-node clusters, verify slot coverage, reshard, and manage replicas with redis-cli cluster commands."
---

# Redis Cluster

Operate Redis Cluster topologies: create multi-node clusters, verify slot coverage, reshard, and manage replicas with redis-cli cluster commands.

## Instructions

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
