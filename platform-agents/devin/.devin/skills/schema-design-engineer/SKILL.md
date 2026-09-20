---
name: "schema-design-engineer"
description: "Designs and validates relational, NoSQL, and event-driven data schemas, producing migration-ready DDL, normalized models, and schema diagrams."
---

# schema-design-engineer

Designs and validates relational, NoSQL, and event-driven data schemas, producing migration-ready DDL, normalized models, and schema diagrams.

## Instructions

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

**Commands:**
- `mongosh appdb --eval "db.createCollection('users', { validator: { $jsonSchema: { bsonType: 'object', required: ['email'] } } })"`
- `mongosh appdb --eval "db.users.getIndexes()"`
- `jq '.[0] | keys' sample.json`
- `mongosh appdb --eval "db.users.aggregate([{ $sample: { size: 1 } }])"`

**Examples:**
- mongosh appdb --eval "db.users.getIndexes()"
- jq -r '.items[] | .sku' catalog.json | sort -u
- mongosh appdb --eval "db.orders.createIndex({ customerId: 1, createdAt: -1 })"
