---
name: "postgresql"
description: "Operates PostgreSQL: psql queries, database lifecycle, dumps, and monitoring views. Use when working with postgres cli, database or when the user mentions postgres cli, database."
type: knowledge
triggers: ["postgresql", "postgres-cli"]
---

Operates PostgreSQL: psql queries, database lifecycle, dumps, and monitoring views.

## Agentic Workflow: Read -> Reason -> Act (postgresql)

You are **postgresql** (database/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — database context for `postgresql`
- Domain: Operates PostgreSQL: psql queries, database lifecycle, dumps, and monitoring views.
- **postgres-cli**: Query, administer, and back up PostgreSQL databases — `psql -U postgres -h localhost -d app`
- Check `knowledge` and `prerequisites: createdb, pg_dump, psql`

### 2. Reason — think for `postgresql`
- For `postgres-cli`: Query, administer, and back up PostgreSQL databases — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `postgresql` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Createdb` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `postgresql:8c54fd4c`

# PostgreSQL

Relational database operations: psql queries, database creation, schema scripts,
and backups.

## When to Use

- Running queries and admin commands
- Creating and managing databases
- Backing up/restoring with pg_dump

## Real Commands

```bash
# Connect
sudo psql -U postgres -h localhost -d app

# Database lifecycle
sudo createdb app -U postgres
sudo dropdb app -U postgres

# Meta-commands
sudo psql -U postgres -d app -c "\dt"
sudo psql -U postgres -d app -c "\d orders"

# Run a script
sudo psql -U postgres -d app -f schema.sql

# Backups
sudo pg_dump -U postgres -Fc app > app.dump
sudo pg_restore -U postgres -d app --no-owner -j4 app.dump

# Monitoring
sudo psql -U postgres -d app -c "SELECT datname, pg_size_pretty(pg_database_size(datname)) FROM pg_database;"
sudo psql -U postgres -d app -c "SELECT pid, state, query FROM pg_stat_activity;"
```

## Best Practices

- Use `-Fc` custom format for flexible restores
- Test `pg_restore` on a staging database
- Use pg_stat_activity to find blocking queries
- Set `statement_timeout` for risky ad-hoc queries
- Keep `VACUUM ANALYZE` healthy with autovacuum

## Example Response

For a lock/blocking issue: lists pg_stat_activity, identifies the blocking pid,
and cancels or terminates it after confirmation.

## Capabilities

### postgres-cli
Query, administer, and back up PostgreSQL databases

**Parameters:**
- `host` (string): Database server host (-h)
- `dbname` (string): Database to connect to (-d)
- `file` (string): Script file to execute (-f)

**Commands:**
- `psql -U postgres -h localhost -d app`
- `createdb app -U postgres`
- `psql -U postgres -d app -f schema.sql`
- `pg_dump -U postgres -Fc app > app.dump`
- `psql -U postgres -d app -c "SELECT pg_size_pretty(pg_database_size('app'));"`

**Examples:**
- psql -U postgres -d app -c "\dt+"
- psql -U postgres -d app -c "SELECT * FROM pg_stat_activity WHERE state='active';"
- pg_restore -U postgres -d app --no-owner -j4 app.dump

## References
- [PostgreSQL docs](https://www.postgresql.org/docs/current/)
- [psql reference](https://www.postgresql.org/docs/current/app-psql.html)
