---
name: "api-mock-json"
description: "Builds zero-code REST mock servers with JSON Server: watch mode, custom routes, filtering, pagination, and CRUD persistence for rapid prototyping."
---

# Api Mock Json

Builds zero-code REST mock servers with JSON Server: watch mode, custom routes, filtering, pagination, and CRUD persistence for rapid prototyping.

## Instructions

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
