---
name: "database-replication"
description: "Architects replication topologies: streaming replicas, failover with Patroni, and lag monitoring. Use when working with replication topology or when the user mentions replication topology."
---

Architects replication topologies: streaming replicas, failover with Patroni, and lag monitoring.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `patronictl -c patroni.yml list`
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

# Database Replication

Designs and operates multi-node replication: streaming standbys, leader
election/failover, and lag monitoring.

## When to Use

- Building HA topologies (primary + standby)
- Performing controlled failovers/switchovers
- Investigating lag or split-brain risks

## Real Commands

```bash
# Patroni cluster status
sudo patronictl -c patroni.yml list

# Controlled switchover
sudo patronictl -c patroni.yml switchover postgres --master node1 --candidate node2 --force

# Emergency failover
sudo patronictl -c patroni.yml failover postgres --master node1 --candidate node2

# Lag monitoring
psql -h node1 -c "SELECT client_addr, state, replay_lag FROM pg_stat_replication;"

# Replica confirmation
psql -h node2 -c "SELECT pg_is_in_recovery();"

# Redis / Mongo
redis-cli INFO replication
sudo mongosh --quiet --eval "rs.printReplicationInfo()"
sudo mongosh --quiet --eval "rs.status().members.forEach(m=>print(m.name, m.stateStr))"
```

## Failover Runbook

1. Confirm the master is truly down (quorum, not partition)
2. Promote the most current standby (`patronictl failover`)
3. Repoint applications to the new leader
4. Re-attach the old node as a follower
5. Verify lag is draining on all followers

## Best Practices

- Use quorum-based leader election (Patroni/etcd), not manual scripting
- Alert on `replay_lag` exceeding the RPO target
- Test switchovers quarterly
- Keep synchronous options only where latency allows
- Read-only traffic must not hit a lagging replica blindly

## Example Response

Reports the cluster topology, current leader, per-replica lag, and executes a
planned switchover with verification of the new leader.

## Capabilities

### replication-topology
Build and operate replicated topologies with failover

**Parameters:**
- `config` (string): Patroni config file (-c)
- `master` (string): Current master node name
- `candidate` (string): Node to promote

**Commands:**
- `patronictl -c patroni.yml list`
- `patronictl -c patroni.yml failover postgres --master node1 --candidate node2`
- `psql -h node1 -c "SELECT client_addr, state, replay_lag FROM pg_stat_replication;"`
- `redis-cli -a $PASS INFO replication`
- `mongosh --quiet --eval "rs.printReplicationInfo()"`

**Examples:**
- patronictl -c patroni.yml switchover postgres --master node1 --candidate node2 --force
- psql -h node2 -c "SELECT pg_is_in_recovery();"
- kafka-consumer-groups.sh --bootstrap-server kafka:9092 --describe --all-groups

## References
- [Patroni docs](https://patroni.readthedocs.io/)
- [PostgreSQL replication docs](https://www.postgresql.org/docs/current/high-availability.html)
- [MongoDB replica sets](https://www.mongodb.com/docs/manual/replication/)
