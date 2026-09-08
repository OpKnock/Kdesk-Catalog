---
name: "mongodb-sharding"
description: "Deploy and manage MongoDB sharded clusters: config servers, mongos routers, shard collections and balanced data. Use when working with sharded cluster operations, api or when the user mentions sharded cluster operations, api."
type: knowledge
triggers: ["mongodb-sharding", "sharded-cluster-operations"]
---

Deploy and manage MongoDB sharded clusters: config servers, mongos routers, shard collections and balanced data.

## Agentic Workflow: Read -> Reason -> Act (mongodb-sharding)

You are **Mongodb Sharding** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `mongodb-sharding`
- Domain: Deploy and manage MongoDB sharded clusters: config servers, mongos routers, shard collections and balanced data.
- **sharded-cluster-operations**: Configure shardsvr mongods, start mongos, enable sharding and manage chunk distribution. — `mongod --shardsvr --replSet shard1 --dbpath /data/shard1 --port 27018`
- Check `knowledge` and `prerequisites: mongod, mongos, mongosh`

### 2. Reason — think for `mongodb-sharding`
- For `sharded-cluster-operations`: Configure shardsvr mongods, start mongos, enable sharding and manage chunk distribution. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `mongodb-sharding` tools
- Tools: `Glob`, `Grep`, `Read`, `Mongod`, `Mongos` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `mongodb-sharding:4a6d02ee`

# MongoDB Sharding

Sharding distributes data across multiple machines so write-heavy collections scale horizontally.

## What this skill does

- Starts shardsvr mongods behind a replica set name
- Runs mongos routers against the config server replica set
- Enables sharding and chooses shard keys

## When to use

- A collection outgrows a single server
- Write throughput needs horizontal scaling
- Building out a new sharded cluster

## Real commands

```bash
# Shard member (needs --shardsvr and a replSet)
mongod --shardsvr --replSet shard1 --dbpath /data/shard1 --port 27018

# Config server (--configsvr, replica set cfgReplSet)
mongod --configsvr --replSet cfgReplSet --dbpath /data/cfg --port 27019

# mongos router
mongos --configdb cfgReplSet/cfg1:27019,cfg2:27019,cfg3:27019 --port 27017

# Through mongos:
sh.addShard('shard1/mongo1:27018,mongo2:27018')
sh.enableSharding('appdb')
sh.shardCollection('appdb.orders', {customer_id: 'hashed'})
sh.status()
```

## Shard key guidance

- Hashed keys give even distribution; ranged keys allow locality
- Never choose a low-cardinality or monotonically increasing key

## Best practices

- Always run shards as replica sets
- Monitor `sh.status()` for chunk imbalance
- Use `balancerStart/Stop` during maintenance windows

## Capabilities

### sharded-cluster-operations
Configure shardsvr mongods, start mongos, enable sharding and manage chunk distribution.

**Parameters:**
- `shardKey` (string): Field(s) used as the shard key, e.g. _id or customer_id
- `shard` (string): Shard name or connection string for addShard
- `namespace` (string): database.collection to enable sharding on

**Commands:**
- `mongod --shardsvr --replSet shard1 --dbpath /data/shard1 --port 27018`
- `mongos --configdb cfgReplSet/cfg1:27019,cfg2:27019,cfg3:27019 --bind_ip 0.0.0.0 --port 27017`
- `mongosh --eval "sh.enableSharding('appdb')"`
- `mongosh --eval "sh.shardCollection('appdb.orders', {customer_id: 'hashed'})"`
- `mongosh --eval "sh.status()"`

**Examples:**
- mongosh --eval "sh.shardCollection('appdb.orders', {_id: 'hashed'})"
- mongosh --eval "sh.moveChunk('appdb.orders', {customer_id: MinKey}, 'shard1')"
- mongosh --eval "sh.addShard('shard1/mongo1:27018,mongo2:27018')"

## References
- [MongoDB Sharding Docs](https://www.mongodb.com/docs/manual/sharding/)
- [sh helper methods](https://www.mongodb.com/docs/manual/reference/method/js-sharding-administration/)
