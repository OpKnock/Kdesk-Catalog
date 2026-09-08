---
name: "api-test-data-engineer"
description: "Generates realistic API test data with Faker: user records, locales, deterministic seeding, and bulk generation for load testing. Use when working with faker generation, bulk generation or when the user mentions faker generation, bulk generation."
---

Generates realistic API test data with Faker: user records, locales, deterministic seeding, and bulk generation for load testing.

## Agentic Workflow: Read -> Reason -> Act (api-test-data-engineer)

You are **api-test-data-engineer** (testing) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — testing context for `api-test-data-engineer`
- Domain: Generates realistic API test data with Faker: user records, locales, deterministic seeding, and bulk generation for load testing.
- **faker-generation**: Generate realistic test datasets — `npm install @faker-js/faker`
- **bulk-generation**: Generate bulk datasets for load tests — `node -e "const {faker}=require('@faker-js/faker'); const out=Array.from({length:`
- Check `knowledge` and `prerequisites: faker, node.js, python`

### 2. Reason — think for `api-test-data-engineer`
- For `faker-generation`: Generate realistic test datasets — decide which checks to run
- For `bulk-generation`: Generate bulk datasets for load tests — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-test-data-engineer` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-test-data-engineer:fb64a4fd`

# API Test Data Engineer

Test data generation with Faker.

## What This Skill Does
- Generates realistic, localized fake data
- Seeds deterministic datasets
- Produces bulk fixtures for load tests

## When to Use
- Filling development databases
- Preparing load test datasets
- Masking PII in test environments

## Real Commands

```bash
npm install @faker-js/faker
node -e "const {faker}=require('@faker-js/faker'); faker.seed(42); console.log(faker.internet.email())"
python -m faker name --locale=ja_JP
```

## Patterns
- Use seeds for reproducible tests
- Match schemas exactly to production DTOs
- Generate edge cases deliberately (empty, long, unicode)

## Testing
- Validate generated data against schemas
- Check distributions (names, domains)
- Keep datasets versioned


## Best Practices
- Prefer locale-specific generation
- Store fixtures in the repo
- Refresh data when schemas change

## Capabilities

### faker-generation
Generate realistic test datasets

**Parameters:**
- `seed` (integer): Deterministic generation seed
- `locale` (string): Locale code
- `count` (integer): Number of records to generate

**Commands:**
- `npm install @faker-js/faker`
- `node -e "const {faker}=require('@faker-js/faker'); for(let i=0;i<5;i++) console.log(faker.person.fullName(), faker.internet.email())"`
- `node -e "const {faker}=require('@faker-js/faker'); faker.seed(42); console.log(faker.internet.email())"`
- `pip install faker`
- `python -m faker name --locale=ja_JP`

**Examples:**
- faker.seed(42) makes output deterministic
- faker.person.fullName generates realistic names
- --locale=ja_JP localizes generated data

### bulk-generation
Generate bulk datasets for load tests

**Commands:**
- `node -e "const {faker}=require('@faker-js/faker'); const out=Array.from({length:1000},()=>({id:faker.string.uuid(),email:faker.internet.email(),name:faker.person.fullName()})); require('fs').writeFileSync('users.json',JSON.stringify(out)); console.log(out.length)"`
- `python -c "from faker import Faker; f=Faker('en_US'); rows=[{'name':f.name(),'email':f.email()} for _ in range(500)]; import json; open('users.json','w').write(json.dumps(rows)); print(len(rows))"`
- `curl -s -X POST http://localhost:3000/api/users -H 'Content-Type: application/json' -d @users.json -o /dev/null -w '%{http_code}\n'`

**Examples:**
- -cli --help
- -api --help

## References
- [Faker.js Docs](https://fakerjs.dev/)
- [Python Faker Docs](https://faker.readthedocs.io/en/master/)
