---
name: "schema-design-engineer"
description: "Designs and validates relational, NoSQL, and event-driven data schemas, producing migration-ready DDL, normalized models, and schema diagrams. Use when working with sql schema modeling, document schema design or when the user mentions sql schema modeling, document schema design."
license: "MIT"
compatibility: "Requires postgresql, mongodb, node.js, python, dbdiagram, dbeaver."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "data"}
allowed-tools: "Glob Grep Read Bash(atlas:*) Bash(jq:*) Bash(mongosh:*) Bash(pg_dump:*) Bash(psql:*) Bash(sqlite3:*)"
---

Designs and validates relational, NoSQL, and event-driven data schemas, producing migration-ready DDL, normalized models, and schema diagrams.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `psql -d appdb -c "\dt"`, `mongosh appdb --eval "db.createCollection('users', { validat`
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

# Schema Design Engineering

Design, inspect, and document data schemas for SQL, NoSQL, and event-driven systems.

## What This Skill Does

- Inspects existing schemas with database-native CLIs and Atlas
- Produces normalized relational models with primary/foreign keys and indexes
- Defines JSON Schema validators for document stores
- Generates ER diagrams and migration-ready DDL
- Reviews schemas for naming, type, and denormalization tradeoffs

## When to Use

- Designing a new database schema from requirements
- Reviewing an existing schema for normalization or index issues
- Producing DDL or a schema diagram for a new feature

## Real Commands

```bash
# Inspect an existing PostgreSQL schema
psql -d appdb -c "\dt"
psql -d appdb -c "\d orders"
pg_dump -s appdb > schema.sql

# Inspect with Atlas (works for Postgres, MySQL, SQLite, and more)
atlas schema inspect --url "postgres://user:pass@localhost:5432/appdb"

# Inspect a SQLite schema
sqlite3 app.db ".schema"
sqlite3 app.db "PRAGMA foreign_key_list(orders);"

# Validate a JSON document against its shape
jq '.[0] | keys' sample.json
```

## Sample Normalized Model

```sql
CREATE TABLE customers (
  id          BIGSERIAL PRIMARY KEY,
  email       TEXT NOT NULL UNIQUE,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE orders (
  id           BIGSERIAL PRIMARY KEY,
  customer_id  BIGINT NOT NULL REFERENCES customers(id),
  status       TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'paid', 'shipped')),
  created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX orders_customer_idx ON orders (customer_id, created_at DESC);
```

## Best Practices

- Prefer normalized forms (3NF) unless profiling shows a real denormalization win
- Always add FKs with matching indexes on the referencing side
- Use TEXT/DECIMAL for money and TIMESTAMPTZ for timestamps
- Add CHECK constraints over application-level validation
- Keep the schema diffable: version it in code, never mutate production DDL by hand

## Capabilities

### sql-schema-modeling
Inspect, model, and normalize SQL schemas using psql, sqlite3, and Atlas.

**Parameters:**
- `url` (string): Database connection URL for schema inspection, e.g. postgres://user@localhost:5432/db
- `table` (string): Table name to describe or inspect
- `format` (string): Output format: SQL, HCL, or diagram

**Commands:**
- `psql -d appdb -c "\dt"`
- `psql -d appdb -c "\d users"`
- `sqlite3 app.db ".schema users"`
- `atlas schema inspect --url "postgres://user:pass@localhost:5432/appdb"`
- `pg_dump -s appdb > schema.sql`

**Examples:**
- atlas schema inspect --url "sqlite://app.db" > schema.hcl
- psql -d appdb -c "\d orders"
- sqlite3 app.db "PRAGMA foreign_key_list(orders);"

### document-schema-design
Define MongoDB and JSON document models with mongosh validation and jq checks.

**Parameters:**
- `collection` (string): MongoDB collection to define or inspect
- `index` (object): Index fields and direction, e.g. {customerId: 1}

**Commands:**
- `mongosh appdb --eval "db.createCollection('users', { validator: { $jsonSchema: { bsonType: 'object', required: ['email'] } } })"`
- `mongosh appdb --eval "db.users.getIndexes()"`
- `jq '.[0] | keys' sample.json`
- `mongosh appdb --eval "db.users.aggregate([{ $sample: { size: 1 } }])"`

**Examples:**
- mongosh appdb --eval "db.users.getIndexes()"
- jq -r '.items[] | .sku' catalog.json | sort -u
- mongosh appdb --eval "db.orders.createIndex({ customerId: 1, createdAt: -1 })"

## References
- [PostgreSQL Documentation](https://www.postgresql.org/docs/current/ddl.html)
- [Atlas Schema Docs](https://atlasgo.io/docs)
- [MongoDB Schema Validation](https://www.mongodb.com/docs/manual/core/schema-validation/)
