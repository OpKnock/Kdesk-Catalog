---
name: "api-test-data-engineer"
description: "Generates realistic API test data with Faker: user records, locales, deterministic seeding, and bulk generation for load testing."
type: knowledge
triggers: ["api-test-data-engineer", "faker-generation", "bulk-generation"]
---

# api-test-data-engineer

Generates realistic API test data with Faker: user records, locales, deterministic seeding, and bulk generation for load testing.

## Instructions

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
