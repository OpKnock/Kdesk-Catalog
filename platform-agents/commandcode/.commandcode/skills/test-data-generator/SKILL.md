---
name: "test-data-generator"
description: "Generates realistic fake data for tests and demos with Faker, mock JSON servers, and database seed tools. Use when working with faker generation, mock json servers, database seeding or when the user mentions faker generation, mock json servers, database seeding."
license: "MIT"
compatibility: "Requires faker, node.js, python, factory-boy, lorem-ipsum, json-schema-faker. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "testing"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(faker:*) Bash(mysql:*) Bash(npx:*) Bash(pgbench:*) Bash(python:*) Bash(sqlite3:*)"
---

Generates realistic fake data for tests and demos with Faker, mock JSON servers, and database seed tools.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `faker name`, `npx json-server --watch db.json --port 3000`
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

# Test Data Generation

Create realistic data for testing, demos, and development.

## What This Skill Does

- Generates fake names, profiles, and domain records with Faker
- Serves and resets mock REST APIs with json-server
- Seeds databases with realistic volumes via pgbench and SQL
- Produces locale-aware and schema-shaped data

## When to Use

- Building test fixtures for API tests
- Populating dev/demo environments
- Load-testing with realistic payloads

## Real Commands

```bash
# Faker CLI
faker name
faker profile --locale=fr_FR
faker -i 500 user_profile > users.jsonl
python -m faker credit_card_number --repeat 5

# Mock API
npx json-server --watch db.json --port 3000
curl -s http://localhost:3000/users | jq '.[0]'

# Database seeding
pgbench -i -s 10 mydb
pgbench -c 10 -j 2 -t 1000 mydb
sqlite3 app.db < seed.sql
```

## Seed Script Pattern

```bash
# Generate 1000 users into JSON
echo '[' > db.json
for i in $(seq 1 1000); do
  faker profile --locale=en_US
  [ $i -lt 1000 ] && echo ','
done >> db.json
echo ']' >> db.json
```

## Best Practices

- Generate data matching production schema constraints
- Use locales matching real users for i18n tests
- Keep seed scripts idempotent (delete before insert)
- Mask or synthesize data never copied from prod
- Size seed volumes to match load-test targets

## Capabilities

### faker-generation
Generate fake records from the command line.

**Parameters:**
- `provider` (string): Faker provider: name, address, profile, pystr
- `locale` (string): Locale, e.g. en_US, fr_FR, ja_JP
- `repeat` (number): Number of records (-i)

**Commands:**
- `faker name`
- `faker profile --locale=fr_FR`
- `faker pystr --min_chars=10 --max_chars=20`
- `faker -i 500 user_profile > users.jsonl`
- `python -m faker address --repeat 10`

**Examples:**
- faker name
- faker profile --locale=fr_FR
- python -m faker credit_card_number --repeat 5

### mock-json-servers
Serve and reset fake API data for development.

**Parameters:**
- `dbFile` (string): JSON database file
- `port` (number): Server port

**Commands:**
- `npx json-server --watch db.json --port 3000`
- `npx json-server db.json --routes routes.json`
- `curl -s http://localhost:3000/users`
- `npx json-server db.json --static ./public`

**Examples:**
- npx json-server --watch db.json --port 3000
- curl -s http://localhost:3000/users | jq '.[0]'
- npx json-server db.json --routes routes.json

### database-seeding
Seed databases with realistic volumes.

**Parameters:**
- `scale` (number): pgbench scale factor (-s)
- `clients` (number): Concurrent clients (-c)

**Commands:**
- `pgbench -i -s 10 mydb`
- `pgbench -c 10 -j 2 -t 1000 mydb`
- `sqlite3 app.db < seed.sql`
- `mysql -u root app < seed.sql`

**Examples:**
- pgbench -i -s 10 mydb
- pgbench -c 10 -j 2 -t 1000 mydb
- sqlite3 app.db < seed.sql

## References
- [Faker Python Documentation](https://faker.readthedocs.io/)
- [json-server GitHub](https://github.com/typicode/json-server)
- [pgbench Documentation](https://www.postgresql.org/docs/current/pgbench.html)
