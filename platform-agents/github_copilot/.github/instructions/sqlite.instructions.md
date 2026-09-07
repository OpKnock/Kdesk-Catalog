---
applyTo: "**/*.r **/*.sh **/*.sql"
---

Works with SQLite databases: queries, schema management, CSV import/export, and integrity checks via sqlite3.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `sqlite3 app.db ".tables"`
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

**Parameters:**
- `mode` (string): Output mode: csv, json, column, list
- `header` (boolean): Show column headers in output
- `backup` (string): Online backup destination with .backup

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

## References
- [SQLite CLI docs](https://sqlite.org/cli.html)
- [SQLite pragmas](https://sqlite.org/pragma.html)
