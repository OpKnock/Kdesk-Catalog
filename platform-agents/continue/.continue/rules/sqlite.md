---
name: "Sqlite"
description: "Works with SQLite databases: queries, schema management, CSV import/export, and integrity checks via sqlite3."
globs: ["**/*.r", "**/*.sh", "**/*.sql"]
alwaysApply: false
---

# Sqlite

Works with SQLite databases: queries, schema management, CSV import/export, and integrity checks via sqlite3.

## Instructions

# SQLite

Embedded SQL database operations: queries, schema, CSV roundtrips, and integrity
verification via sqlite3.

## When to Use

- Inspecting an app's local database file
- Converting data between CSV and tables
- Quick analytics on single-file data

## Real Commands

```bash
# Explore
sudo sqlite3 app.db ".tables"
sudo sqlite3 app.db ".schema users"

# Queries
sudo sqlite3 app.db "SELECT count(*), max(created_at) FROM orders;"
sudo sqlite3 app.db "SELECT * FROM users WHERE email LIKE '%example.com' LIMIT 5;"

# CSV export/import
sudo sqlite3 -header -csv app.db "SELECT * FROM orders;" > orders.csv
sudo sqlite3 app.db ".mode csv" ".import orders.csv orders"

# Integrity
sudo sqlite3 app.db "PRAGMA integrity_check;"
sudo sqlite3 app.db "PRAGMA quick_check;"

# WAL for concurrency
sudo sqlite3 app.db "PRAGMA journal_mode=WAL;"

# Backup
sudo sqlite3 app.db ".backup app-backup.db"
```

## Best Practices

- Enable WAL for production-ish usage; better concurrency
- Run `PRAGMA integrity_check` before and after risky ops
- Use `.backup` for live backups; don't copy the file blindly
- Create indexes for query columns
- `ANALYZE` after bulk imports

## Example Response

Reports schema, row counts, and integrity status; performs the requested import/
export and verifies row counts both ways.

## Capabilities

### sqlite3-cli
Query, manage, and convert SQLite databases

**Commands:**
- `sqlite3 app.db ".tables"`
- `sqlite3 app.db "SELECT * FROM users LIMIT 10;"`
- `sqlite3 app.db ".schema users"`
- `sqlite3 app.db ".mode csv" "SELECT * FROM users" > users.csv`
- `sqlite3 app.db "PRAGMA integrity_check;"`

**Examples:**
- sqlite3 app.db "CREATE INDEX idx_users_email ON users(email);"
- sqlite3 app.db ".mode csv" ".import users.csv users"
- sqlite3 app.db "PRAGMA journal_mode=WAL;"