---
name: "replication"
description: "Sets up and monitors database replication: PostgreSQL streaming, MySQL binlog, Redis replicas, and failover checks."
type: knowledge
triggers: ["replication", "replication-setup"]
---

# Replication

Sets up and monitors database replication: PostgreSQL streaming, MySQL binlog, Redis replicas, and failover checks.

## Instructions

# Replication

Configures and verifies database replication so standby systems stay current for
HA and read scaling.

## When to Use

- Adding a read replica for scale-out
- Setting up warm standbys for failover
- Verifying replication health after changes

## Real Commands

```bash
# PostgreSQL: create replica from base backup
sudo pg_basebackup -h primary -D /var/lib/postgresql/16/replica -R -U replicator

# Verify replica is catching up
psql -h replica -U app -c "SELECT pg_is_in_recovery();"
psql -h primary -U postgres -c "SELECT client_addr, state, replay_lag FROM pg_stat_replication;"

# Promote on failover
sudo pg_ctlcluster 16 replica promote

# MySQL: check replication
mysql -e "SHOW SLAVE STATUS\G" | grep -E 'Slave_IO_Running|Slave_SQL_Running|Seconds_Behind_Master'

# Redis: info and promote
redis-cli INFO replication
redis-cli -p 6380 SLAVEOF NO ONE

# MongoDB replica set status
sudo mongosh --quiet --eval "rs.status().members.forEach(m => print(m.name, m.stateStr))"
```

## Health Checklist

- PostgreSQL: `state = streaming`, `replay_lag` small, `pg_is_in_recovery()` true
- MySQL: `Slave_IO_Running: Yes`, `Slave_SQL_Running: Yes`, low lag
- Redis: `role:slave`, `master_link_status:up`
- MongoDB: `SECONDARY` with no stale votes

## Best Practices

- Test promotion in staging; never first-learn it in an outage
- Alert on lag, not just connectivity
- Use synchronous replication for zero-loss workloads
- Monitor replication slots / binlog retention
- Document the failover runbook

## Example Response

Reports replication state per engine, lag values, and any stopped/catching-up
states, then executes the promotion or re-sync steps needed.

## Capabilities

### replication-setup
Configure, monitor, and promote replication across database engines

**Commands:**
- `psql -h primary -U replicator -c "SELECT * FROM pg_stat_replication;"`
- `pg_basebackup -h primary -D /var/lib/postgresql/replica -R -U replicator`
- `mysql -e "SHOW SLAVE STATUS\G" | grep -E 'Slave_IO_Running|Slave_SQL_Running'`
- `redis-cli INFO replication`
- `mongosh --quiet --eval "rs.status().members.forEach(m => print(m.name, m.stateStr))"`

**Examples:**
- psql -h replica -U app -c "SELECT pg_is_in_recovery();"
- mysql -e "START SLAVE;"
- redis-cli -p 6380 SLAVEOF 10.0.0.5 6379
