---
name: "test-data-generator"
description: "Generates realistic fake data for tests and demos with Faker, mock JSON servers, and database seed tools."
globs: ["**/*.json", "**/*.py", "**/*.r", "**/*.sh", "**/*.sql"]
alwaysApply: false
---

# test-data-generator

Generates realistic fake data for tests and demos with Faker, mock JSON servers, and database seed tools.

## Instructions

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

**Commands:**
- `pgbench -i -s 10 mydb`
- `pgbench -c 10 -j 2 -t 1000 mydb`
- `sqlite3 app.db < seed.sql`
- `mysql -u root app < seed.sql`

**Examples:**
- pgbench -i -s 10 mydb
- pgbench -c 10 -j 2 -t 1000 mydb
- sqlite3 app.db < seed.sql