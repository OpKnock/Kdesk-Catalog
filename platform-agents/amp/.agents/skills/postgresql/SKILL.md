---
name: "postgresql"
description: "Operates PostgreSQL: psql queries, database lifecycle, dumps, and monitoring views. Use when working with postgres cli, database or when the user mentions postgres cli, database."
license: "MIT"
compatibility: "Requires createdb, pg_dump, psql."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "database"}
allowed-tools: "Glob Grep Read Bash(createdb:*) Bash(pg_dump:*) Bash(psql:*)"
---

Operates PostgreSQL: psql queries, database lifecycle, dumps, and monitoring views.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `psql -U postgres -h localhost -d app`
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
