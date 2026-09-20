---
name: "api-mock-json"
description: "Builds zero-code REST mock servers with JSON Server: watch mode, custom routes, filtering, pagination, and CRUD persistence for rapid prototyping. Use when working with json server, route customization or when the user mentions json server, route customization."
type: knowledge
triggers: ["api-mock-json", "json-server", "route-customization"]
---

Builds zero-code REST mock servers with JSON Server: watch mode, custom routes, filtering, pagination, and CRUD persistence for rapid prototyping.

## Agentic Workflow: Read -> Reason -> Act (api-mock-json)

You are **Api Mock Json** (testing) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — testing context for `api-mock-json`
- Domain: Builds zero-code REST mock servers with JSON Server: watch mode, custom routes, filtering, pagination, and CRUD persistence for rapid prototyping.
- **json-server**: Serve a mock REST API from a JSON database file — `npm install -g json-server`
- **route-customization**: Map custom URLs and add middleware to the mock server — `curl -s http://localhost:3001/users/1 | jq .`
- Check `knowledge` and `prerequisites: prism, wiremock, msw`

### 2. Reason — think for `api-mock-json`
- For `json-server`: Serve a mock REST API from a JSON database file — decide which checks to run
- For `route-customization`: Map custom URLs and add middleware to the mock server — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-mock-json` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Json-server` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-mock-json:1facaef5`

# API Mock v2 - JSON Server

Instant REST mocks from a JSON file.

## What This Skill Does
- Serves CRUD endpoints for each collection in db.json
- Provides filtering, pagination, and sorting via query params
- Persists mutations back to the db file in watch mode

## When to Use
- Rapid UI prototyping against REST shapes
- Quick contract demos before the real backend exists
- Local frontend development with fake data

## Real Commands

```bash
npm install -g json-server
json-server --watch db.json --port 3001
curl -s http://localhost:3001/users | jq 'length'
curl -s -X POST http://localhost:3001/users -H 'Content-Type: application/json' -d '{"name":"alice"}'
```

## db.json Example

```json
{
  "users": [{ "id": 1, "name": "alice", "role": "admin" }],
  "orders": []
}
```

Endpoints: GET/POST /users, GET/PUT/PATCH/DELETE /users/:id.

## Testing
- Query filters: /users?role=admin
- Pagination: /users?_page=2&_limit=5
- Sorting: /users?_sort=name&_order=asc
- Full-text: /users?q=ali

## Best Practices
- Commit db.json with seed data for reproducibility
- Use routes.json to simulate nested or custom paths
- Do not use JSON Server in production traffic

## Capabilities

### json-server
Serve a mock REST API from a JSON database file

**Parameters:**
- `port` (integer): Port for the mock server, default 3000
- `db-file` (string): JSON file containing collections to serve
- `routes-file` (string): Custom route mapping file (routes.json)

**Commands:**
- `npm install -g json-server`
- `json-server --watch db.json --port 3001`
- `json-server db.json --routes routes.json --port 3001`
- `curl -s http://localhost:3001/users | jq 'length'`
- `curl -s -X POST http://localhost:3001/users -H 'Content-Type: application/json' -d '{"name":"alice"}'`

**Examples:**
- json-server --watch db.json --port 3001 serves full REST endpoints
- curl -s 'http://localhost:3001/users?_page=2&_limit=5' exercises built-in pagination
- curl -s 'http://localhost:3001/users?role=admin' uses query filtering

### route-customization
Map custom URLs and add middleware to the mock server

**Commands:**
- `curl -s http://localhost:3001/users/1 | jq .`
- `curl -s -X PUT http://localhost:3001/users/1 -H 'Content-Type: application/json' -d '{"name":"bob"}'`
- `curl -s -X DELETE http://localhost:3001/users/1 -o /dev/null -w '%{http_code}\n'`

**Examples:**
- -cli --help
- -api --help

## References
- [json-server GitHub](https://github.com/typicode/json-server)
- [jq Manual](https://jqlang.github.io/jq/manual/)
