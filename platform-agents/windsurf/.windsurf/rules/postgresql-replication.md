---
trigger: glob
description: "PostgreSQL streaming replication: pg_basebackup, replication slots, WAL shipping, and failover. Use when working with postgres streaming replication, api or when the user mentions postgres streaming replication, api."
globs: ["**/*.r", "**/*.sh", "**/*.sql"]
---

PostgreSQL streaming replication: pg_basebackup, replication slots, WAL shipping, and failover.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `pg_basebackup -h primary -D /var/lib/postgresql/standby -U r`
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
