# Api Test Data Sqlite Seeding

Seeds database test data with SQL scripts and Node scripts: sqlite3 import, PostgreSQL COPY/INSERT, fixtures, and repeatable seed flows.

## Instructions

# API Test Data v2 - Database Seeding

Database seeding for API tests.

## What This Skill Does
- Seeds SQLite and PostgreSQL fixtures
- Resets state between tests
- Exports reusable seed scripts

## When to Use
- Integration test databases
- CI ephemeral environments
- Reproducible local dev data

## Real Commands

```bash
sqlite3 test.db "INSERT INTO users (name, email) VALUES ('alice', 'a@example.com')"
psql -d app -c "COPY users (name, email) FROM '/tmp/users.csv' WITH (FORMAT csv, HEADER true)"
psql -d app -c "TRUNCATE users RESTART IDENTITY"
```

## Seeding Strategy
1. Truncate with restart identity
2. Insert fixtures in dependency order
3. Re-verify with count queries

## Testing
- Reset then seed in test setup hooks
- Verify foreign keys after truncation
- Time large seeds with COPY vs INSERT


## Best Practices
- Keep seed scripts idempotent
- Version seeds with migrations
- Use CSV COPY for bulk rows

## Capabilities

### sqlite-seeding
Seed SQLite databases for API tests

**Commands:**
- `sqlite3 test.db "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)"`
- `sqlite3 test.db "INSERT INTO users (name, email) VALUES ('alice', 'a@localhost'), ('bob', 'b@localhost')"`
- `sqlite3 test.db "SELECT COUNT(*) FROM users"`
- `node -e "const db=require('better-sqlite3')('test.db'); db.prepare('INSERT INTO users (name,email) VALUES (?,?)').run('carol','c@example.com'); console.log(db.prepare('SELECT COUNT(*) c FROM users').get())"`
- `sqlite3 test.db ".dump" > seed.sql`

**Examples:**
- sqlite3 multi-row INSERT seeds fixtures
- better-sqlite3 runs prepared statements
- .dump exports the full seed

### postgres-seeding
Seed PostgreSQL for integration tests

**Commands:**
- `psql -d app -f seed.sql`
- `psql -d app -c "COPY users (name, email) FROM '/tmp/users.csv' WITH (FORMAT csv, HEADER true)"`
- `psql -d app -c "TRUNCATE users RESTART IDENTITY"`
- `pg_dump --data-only -t users app > seed.sql`

**Examples:**
- -cli --help
- -api --help