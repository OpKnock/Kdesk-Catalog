---
applyTo: "**/*.r **/*.sh **/*.sql"
---

# mysql

Operates MySQL: interactive queries, scripted DDL/DML, dumps, and performance status.

## Instructions

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
