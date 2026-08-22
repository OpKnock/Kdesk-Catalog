---
trigger: glob
description: "Deploy and manage MongoDB replica sets: init, membership, failover, elections, and oplog inspection."
globs: ["**/*.go", "**/*.r", "**/*.sh"]
---

# Mongodb Replica Set

Deploy and manage MongoDB replica sets: init, membership, failover, elections, and oplog inspection.

## Instructions

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
