---
trigger: glob
description: "Postman workflows: collections via the Postman CLI, newman runs in CI, environments, and API testing."
globs: ["**/*.json", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

# Postman

Postman workflows: collections via the Postman CLI, newman runs in CI, environments, and API testing.

## Instructions

# Postman

Postman turns request collections into repeatable API tests you can run anywhere.

## What this skill does

- Runs collections with newman in CI
- Manages environments and variables
- Generates reports for review

## When to use

- API regression testing
- Smoke tests after deploys

## Real commands

```bash
# Local run
newman run collection.json -e environment.json

# Folder + env override
newman run collection.json --folder "auth" --env-var baseUrl=http://localhost:8080

# Reports
newman run collection.json --reporters cli,json --reporter-json-export report.json
newman run collection.json --reporters junit --reporter-junit-export results.xml

# Postman CLI (cloud sync)
postman login --with-api-key $POSTMAN_API_KEY
postman collection run "My Collection" --environment "Staging"
```

## CI snippet (GitHub Actions)

```yaml
- run: npm install -g newman
- run: newman run api.postman_collection.json -e staging.postman_environment.json --bail
```

## Best practices

- Store secrets as environment variables, never inline
- Use --bail to stop on first failure in CI
- Keep collections in git for review

## Capabilities

### postman-collection-testing
Run Postman collections locally and in CI with newman, manage environments and generate reports.

**Commands:**
- `newman run collection.json -e environment.json`
- `newman run collection.json --folder "auth" --env-var baseUrl=http://localhost:8080`
- `newman run collection.json --reporters cli,json --reporter-json-export report.json`
- `postman login --with-api-key $POSTMAN_API_KEY`
- `postman collection run "My Collection" --environment "Staging"`

**Examples:**
- newman run api.postman_collection.json -e staging.postman_environment.json --bail
- newman run collection.json --reporters junit --reporter-junit-export results.xml
- postman collection run "Order API" --env-var token=abc123
