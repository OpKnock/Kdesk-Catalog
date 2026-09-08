Expert core reference covering resource modeling, curl CRUD flows, status code semantics, and JSON handling with jq suited to daily API work.

## Agentic Workflow: Read -> Reason -> Act (rest)

You are **Rest** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `rest`
- Domain: Expert core reference covering resource modeling, curl CRUD flows, status code semantics, and JSON handling with jq suited to daily API work.
- **rest-crud**: Execute and debug REST CRUD flows with curl and jq — `curl -s -X POST https://api.your-app.test/v1/orders -H 'Content-Type: applicatio`
- Check `knowledge` references before acting

### 2. Reason — think for `rest`
- For `rest-crud`: Execute and debug REST CRUD flows with curl and jq — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `rest` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `rest:6bfccbc6`

# REST APIs

Expert skill for building and debugging REST APIs.

## What this skill does

- Models resources and picks the right verb per operation
- Exercises CRUD flows end-to-end with curl
- Reads and asserts on JSON responses with jq

## When to use

- Designing a new resource endpoint
- Reproducing a bug report against a running API
- Verifying behavior before writing tests

## Real commands

```bash
# Create (expect 201)
curl -s -X POST https://api.your-app.test/v1/orders -H 'Content-Type: application/json' -d '{"customer":7,"total":199}'

# Read one (expect 200)
curl -s https://api.your-app.test/v1/orders/7 | jq '.total'

# List with query params
curl -i https://api.your-app.test/v1/orders?page=2

# Full update vs partial update
curl -s -X PUT https://api.your-app.test/v1/orders/7 -H 'Content-Type: application/json' -d '{"customer":7,"total":199,"status":"shipped"}'
curl -s -X PATCH https://api.your-app.test/v1/orders/7 -d '{"status":"canceled"}'

# Delete (expect 204)
curl -s -o /dev/null -w '%{http_code}\n' -X DELETE https://api.your-app.test/v1/orders/7

# Not found check
curl -s -o /dev/null -w '%{http_code}\n' https://api.your-app.test/v1/orders/999
```

## Status code semantics

- 200 success, 201 created, 204 no content
- 400 client error, 401 unauthenticated, 403 forbidden, 404 not found
- 409 conflict, 422 validation, 429 rate limited, 500 server error

## Testing

```bash
curl -s https://api.your-app.test/v1/orders | jq '.items | length'
```

## Best practices

- Use nouns for resources, not verbs: /orders not /getOrders
- Return 201 + Location header on create, 204 on delete
- Keep GET endpoints side-effect free

## Capabilities

### rest-crud
Execute and debug REST CRUD flows with curl and jq

**Parameters:**
- `url` (string): Endpoint URL including path and query
- `method` (string): HTTP verb: GET, POST, PUT, PATCH, DELETE
- `body` (string): JSON request body for mutating requests

**Commands:**
- `curl -s -X POST https://api.your-app.test/v1/orders -H 'Content-Type: application/json' -d '{"customer":7,"total":199}'`
- `curl -s -X PUT https://api.your-app.test/v1/orders/7 -H 'Content-Type: application/json' -d '{"status":"shipped"}'`
- `curl -s https://api.your-app.test/v1/orders/7 | jq '.total'`
- `curl -s -o /dev/null -w '%{http_code}\n' -X DELETE https://api.your-app.test/v1/orders/7`
- `curl -i https://api.your-app.test/v1/orders?page=2`

**Examples:**
- curl -s https://api.your-app.test/v1/orders | jq '.items[] | {id, total}'
- curl -s -X PATCH https://api.your-app.test/v1/orders/7 -d '{"status":"canceled"}'
- curl -s -o /dev/null -w '%{http_code}\n' https://api.your-app.test/v1/orders/999

## References
- [MDN HTTP methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)
- [curl man page](https://curl.se/docs/manpage.html)