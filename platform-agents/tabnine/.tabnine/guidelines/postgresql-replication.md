# Postgresql Replication

PostgreSQL streaming replication: pg_basebackup, replication slots, WAL shipping, and failover.

## Instructions

# PostgreSQL Replication

Streaming replication keeps a hot standby in near-real-time sync with the primary.

## What this skill does

- Creates replicas with pg_basebackup
- Manages replication slots
- Monitors lag and promotes on failover

## When to use

- HA and read scaling
- Fast disaster recovery

## Real commands

```bash
# Primary config (postgresql.conf)
# wal_level = replica, max_wal_senders = 10

# Create replication user
psql -c "CREATE USER replicator REPLICATION LOGIN PASSWORD 'secret';"

# Base backup + standby config (-R writes standby.signal)
pg_basebackup -h primary -D /var/lib/postgresql/standby -U replicator -R -X stream -P

# Start the standby
pg_ctl start -D /var/lib/postgresql/standby

# Monitor
psql -c "SELECT * FROM pg_stat_replication;"
psql -c "SELECT * FROM pg_replication_slots;"
psql -c "SELECT pg_current_wal_lsn();"

# Failover
pg_ctl promote -D /var/lib/postgresql/standby
```

## Lag check

```sql
SELECT client_addr, state, replay_lag
FROM pg_stat_replication;
```

## Best practices

- Enable replication slots to avoid WAL loss
- Alert on replay_lag growth
- Test failover on staging regularly

## Capabilities

### postgres-streaming-replication
Set up streaming replicas with pg_basebackup, manage replication slots, and monitor replication status.

**Commands:**
- `pg_basebackup -h primary -D /var/lib/postgresql/standby -U replicator -R -X stream`
- `psql -c "SELECT * FROM pg_replication_slots;"`
- `psql -c "SELECT * FROM pg_stat_replication;"`
- `psql -c "SELECT pg_current_wal_lsn();"`
- `pg_ctl promote -D /var/lib/postgresql/standby`

**Examples:**
- pg_basebackup -h primary -D /var/lib/postgresql/replica -U replicator -R -X stream -P
- psql -c "SELECT client_addr, state, write_lag, replay_lag FROM pg_stat_replication;"
- psql -c "SELECT pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) AS lag FROM pg_stat_replication;"