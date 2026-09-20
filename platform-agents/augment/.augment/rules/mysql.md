---
type: agent_requested
description: "Operates MySQL: interactive queries, scripted DDL/DML, dumps, and performance status. Use when working with mysql cli, database or when the user mentions mysql cli, database."
---

Operates MySQL: interactive queries, scripted DDL/DML, dumps, and performance status.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `mysql -u root -p`
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

# MySQL

Relational database operations: queries, schema scripts, dumps, and server status
via the mysql client.

## When to Use

- Running queries and admin statements
- Applying schema changes
- Backing up and restoring databases

## Real Commands

```bash
# Interactive
sudo mysql -u root -p

# One-shot queries
sudo mysql -u root -p appdb -e "SHOW TABLES;"
sudo mysql -u root -p -e "SELECT VERSION(), CURRENT_TIMESTAMP;"

# Run a script
sudo mysql -u root -p appdb < schema.sql

# Backup with consistent snapshot
sudo mysqldump -u root -p --single-transaction --routines appdb > backup.sql

# Restore
sudo mysql -u root -p appdb < backup.sql

# Server status
sudo mysqladmin -u root status
sudo mysql -u root -p -e "SHOW GLOBAL STATUS LIKE 'Threads_connected';"

# Remote host
sudo mysql -h db.example.com -P 3306 -u app -p appdb
```

## Best Practices

- Use `--single-transaction` for InnoDB backups without locking
- Never put passwords in command history (`-p` prompts)
- Test restores in staging
- Check slow query log for performance issues
- Use `EXPLAIN` before optimizing queries

## Example Response

For a slow query: runs EXPLAIN, reports the access type and index usage, and
recommends an index or query rewrite.

## Capabilities

### mysql-cli
Query, import/export, and inspect MySQL servers

**Parameters:**
- `execute` (string): SQL to execute in one-shot mode (-e)
- `single-transaction` (boolean): Consistent snapshot for InnoDB dumps
- `host` (string): Server hostname (-h)

**Commands:**
- `mysql -u root -p`
- `mysql -u root -p appdb -e "SHOW TABLES;"`
- `mysql -u root -p appdb < schema.sql`
- `mysqldump -u root -p --single-transaction appdb > backup.sql`
- `mysqladmin -u root status`

**Examples:**
- mysql -h db.example.com -P 3306 -u app -p appdb -e "SELECT count(*) FROM orders;"
- mysql -u root -p -e "SHOW GLOBAL STATUS LIKE 'Threads_connected';"
- mysqldump -u root -p --no-data --routines appdb > schema-only.sql

## References
- [MySQL reference manual](https://dev.mysql.com/doc/refman/8.0/en/)
- [mysqldump reference](https://dev.mysql.com/doc/refman/8.0/en/mysqldump.html)