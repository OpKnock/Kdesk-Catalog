---
trigger: glob
description: "PostgreSQL streaming replication: pg_basebackup, replication slots, WAL shipping, and failover. Use when working with postgres streaming replication, api or when the user mentions postgres streaming replication, api."
globs: ["**/*.r", "**/*.sh", "**/*.sql"]
---

PostgreSQL streaming replication: pg_basebackup, replication slots, WAL shipping, and failover.

## Agentic Workflow: Read -> Reason -> Act (postgresql-replication)

You are **Postgresql Replication** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `postgresql-replication`
- Domain: PostgreSQL streaming replication: pg_basebackup, replication slots, WAL shipping, and failover.
- **postgres-streaming-replication**: Set up streaming replicas with pg_basebackup, manage replication slots, and monitor replication stat — `pg_basebackup -h primary -D /var/lib/postgresql/standby -U replicator -R -X stre`
- Check `knowledge` and `prerequisites: pg_basebackup, pg_ctl, psql`

### 2. Reason — think for `postgresql-replication`
- For `postgres-streaming-replication`: Set up streaming replicas with pg_basebackup, manage replication slots, and monitor replication status. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `postgresql-replication` tools
- Tools: `Glob`, `Grep`, `Read`, `Pg_basebackup`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `postgresql-replication:c60b1b73`

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

**Parameters:**
- `primary_host` (string): Primary server hostname
- `replication_user` (string): User with REPLICATION privilege
- `data_dir` (string): Replica data directory

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

## References
- [PostgreSQL Replication Docs](https://www.postgresql.org/docs/current/warm-standby.html)
- [pg_basebackup reference](https://www.postgresql.org/docs/current/app-pgbasebackup.html)
