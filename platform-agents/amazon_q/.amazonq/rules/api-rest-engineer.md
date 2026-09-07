Implements REST APIs in Node.js with Express: resource routing, status-code semantics, JSON error handling, and curl-based endpoint verification.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npm init -y && npm install express`, `curl -s -o /dev/null -w '%{http_code}\n' http://localhost:30`
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

# API REST Engineer

REST implementation with Express.

## What This Skill Does
- Implements CRUD endpoints with Express routing
- Uses REST-correct status codes
- Handles errors with consistent JSON

## When to Use
- Building Node.js REST services
- Implementing new resource endpoints
- Fixing status code semantics

## Real Commands

```bash
npm init -y && npm install express
node app.js
curl -s -X POST http://localhost:3000/api/users -H 'Content-Type: application/json' -d '{"name":"alice"}' -w '\n%{http_code}\n'
```

## Status Code Rules
- 200 for GET/PUT/PATCH success
- 201 + Location for POST
- 204 for DELETE success
- 400 invalid body, 404 missing resource, 409 conflict

## Testing
- Exercise each status code with curl
- Verify Location header on creates
- Validate 404 bodies include the resource id

## Best Practices
- Keep route handlers thin; extract services
- Use middleware for validation before handlers
- Document codes in the OpenAPI contract

## Capabilities

### express-routing
Build REST resource routes with Express

**Parameters:**
- `resource` (string): Resource name in the route path
- `id` (integer): Resource identifier
- `body` (object): JSON payload for mutations

**Commands:**
- `npm init -y && npm install express`
- `node app.js`
- `curl -s -X POST http://localhost:3000/api/users -H 'Content-Type: application/json' -d '{"name":"alice"}' -w '\n%{http_code}\n'`
- `curl -s http://localhost:3000/api/users | jq 'length'`
- `curl -s http://localhost:3000/api/users/1 | jq .name`

**Examples:**
- POST /api/users returns 201 Created
- GET /api/users/1 returns the resource or 404
- curl -w '%{http_code}' asserts status codes

### status-semantics
Apply correct HTTP status codes per operation

**Commands:**
- `curl -s -o /dev/null -w '%{http_code}\n' http://localhost:3000/api/users/999`
- `curl -s -o /dev/null -w '%{http_code}\n' -X DELETE http://localhost:3000/api/users/1`
- `curl -s -o /dev/null -w '%{http_code}\n' -X PATCH http://localhost:3000/api/users/1 -H 'Content-Type: application/json' -d '{"name":"bob"}'`
- `curl -s -o /dev/null -w '%{http_code}\n' http://localhost:3000/api/health`

**Examples:**
- -cli --help
- -api --help

## References
- [Express Routing Guide](https://expressjs.com/en/guide/routing.html)
- [MDN HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)