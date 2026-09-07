Deploy and manage MongoDB replica sets: init, membership, failover, elections, and oplog inspection.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `mongod --replSet rs0 --dbpath /data/db --bind_ip 0.0.0.0 --p`
- Check `knowledge` references and prerequisites before proceeding

### 2. Reason
Analyze and plan:
- Compare current state vs desired state (drift, checksums, policy)
- Evaluate trust, compatibility, and risk: use `kdesk trust` and `kdesk doctor` patterns
- Decide: which capabilities/tools are needed, which can be skipped

### 3. Act
Execute with guards:
- Run only `allowed-tools` (see frontmatter); use `safe_path` for writes
- Prefer `Bash` with explicit binaries (`curl`, `kubectl`, `kdesk`) over generic shell
- Record evidence: file paths, checksums, and tool outputs for verification

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