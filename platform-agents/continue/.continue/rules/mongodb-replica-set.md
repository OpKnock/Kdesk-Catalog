---
name: "Mongodb Replica Set"
description: "Deploy and manage MongoDB replica sets: init, membership, failover, elections, and oplog inspection. Use when working with replica set operations, api or when the user mentions replica set operations, api."
globs: ["**/*.go", "**/*.r", "**/*.sh"]
alwaysApply: false
---

Deploy and manage MongoDB replica sets: init, membership, failover, elections, and oplog inspection.

## Agentic Workflow: Read -> Reason -> Act (mongodb-replica-set)

You are **Mongodb Replica Set** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `mongodb-replica-set`
- Domain: Deploy and manage MongoDB replica sets: init, membership, failover, elections, and oplog inspection.
- **replica-set-operations**: Initialize and manage a MongoDB replica set through mongod flags and mongosh replica set commands. — `mongod --replSet rs0 --dbpath /data/db --bind_ip 0.0.0.0 --port 27017`
- Check `knowledge` and `prerequisites: mongod, mongosh`

### 2. Reason — think for `mongodb-replica-set`
- For `replica-set-operations`: Initialize and manage a MongoDB replica set through mongod flags and mongosh replica set commands. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `mongodb-replica-set` tools
- Tools: `Glob`, `Grep`, `Read`, `Mongod`, `Mongosh` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `mongodb-replica-set:311c67bd`

# MongoDB Replica Set

A replica set is a group of mongod instances that maintain the same data set, providing redundancy and automatic failover.

## What this skill does

- Starts mongod nodes with a replica set name
- Initializes the set and manages membership
- Diagnoses elections, failover and oplog issues

## When to use

- Setting up HA MongoDB for the first time
- Adding or removing members
- Investigating primary/secondary state or stale members

## Real commands

```bash
# Start each node with the same replSet name
mongod --replSet rs0 --dbpath /data/db --bind_ip 0.0.0.0 --port 27017

# Initiate with explicit member list
mongosh --eval "rs.initiate({_id:'rs0',members:[{_id:0,host:'mongo1:27017'},{_id:1,host:'mongo2:27017'},{_id:2,host:'mongo3:27017'}]})"

# Add/remove members
mongosh --eval "rs.add('mongo2:27017')"
mongosh --eval "rs.remove('mongo3:27017')"

# Force a step-down (maintenance)
mongosh --eval "rs.stepDown(60)"

# Inspect state
mongosh --eval "rs.status()"
mongosh --eval "rs.conf()"
```

## Oplog inspection

```js
use local
db.oplog.rs.find().sort({$natural:-1}).limit(1)
```

## Best practices

- Always use odd member counts or an arbiter
- Monitor `replSetSecondary` state and oplog lag
- Reconfigure with `rs.reconfig()` only with majority reachable

## Capabilities

### replica-set-operations
Initialize and manage a MongoDB replica set through mongod flags and mongosh replica set commands.

**Parameters:**
- `replSet` (string): Replica set name, must match across members
- `host` (string): Hostname:port of the member to add or remove
- `force` (boolean): Force reconfiguration when out of quorum

**Commands:**
- `mongod --replSet rs0 --dbpath /data/db --bind_ip 0.0.0.0 --port 27017`
- `mongosh --eval "rs.initiate()"`
- `mongosh --eval "rs.add('mongo2:27017')"`
- `mongosh --eval "rs.status()"`
- `mongosh --eval "rs.conf()"`

**Examples:**
- mongosh --eval "rs.initiate({_id:'rs0',members:[{_id:0,host:'mongo1:27017'},{_id:1,host:'mongo2:27017'},{_id:2,host:'mongo3:27017'}]})"
- mongosh --eval "rs.stepDown(60)"
- mongosh --eval "rs.status()" | grep -E 'stateStr|name'

## References
- [MongoDB Replication Docs](https://www.mongodb.com/docs/manual/replication/)
- [rs helper methods](https://www.mongodb.com/docs/manual/reference/method/js-replica-set-administration/)