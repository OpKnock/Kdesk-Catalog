---
name: "postgresql"
description: "Operates PostgreSQL: psql queries, database lifecycle, dumps, and monitoring views."
globs: ["**/*.r", "**/*.sh", "**/*.sql"]
alwaysApply: false
---

# postgresql

Operates PostgreSQL: psql queries, database lifecycle, dumps, and monitoring views.

## Instructions

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