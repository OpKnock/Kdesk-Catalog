# api-rest-engineer

Implements REST APIs in Node.js with Express: resource routing, status-code semantics, JSON error handling, and curl-based endpoint verification.

## Instructions

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
