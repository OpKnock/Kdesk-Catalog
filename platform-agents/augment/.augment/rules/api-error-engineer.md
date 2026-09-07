---
type: agent_requested
description: "Implements consistent API error handling: RFC 9457 problem details middleware, error codes, and OpenAPI error documentation. Use when working with error middleware, error docs or when the user mentions error middleware, error docs."
---

Implements consistent API error handling: RFC 9457 problem details middleware, error codes, and OpenAPI error documentation.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npm install http-errors`, `swagger-cli validate openapi.yaml`
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

# API Error Engineer

Implements standardized, documented, and observable error handling for APIs.

## When to Use
- Inconsistent error bodies across endpoints
- Stack traces leaking to clients
- Building error catalogs

## Real Commands

```bash
# Install middleware deps
npm install http-errors express-async-errors

# Reproduce error responses
curl -s http://localhost:3000/api/users/999 | python -m json.tool
curl -s -X POST http://localhost:3000/api/users -H 'Content-Type: application/json' -d '{}' -w '\n%{http_code}'

# Validate docs include errors
swagger-cli validate openapi.yaml
redocly lint openapi.yaml
```

## Problem Details Shape

```json
{"type":"https://api.example.com/errors/user-not-found","title":"User not found","status":404,"code":"USER_NOT_FOUND","instance":"/api/users/999"}
```

## Testing
Assert on status, code, and title for every documented error in automated tests.

## Best Practices
- Never leak stack traces to clients
- One `code` per failure mode
- Document each code in OpenAPI

## Capabilities

### error-middleware
Build error-handling middleware with structured problem details responses

**Parameters:**
- `status` (string): HTTP status code
- `code` (string): Domain error code

**Commands:**
- `npm install http-errors`
- `npm install express-async-errors`
- `curl -s http://localhost:3000/api/users/999 | python -m json.tool`
- `curl -s -X POST http://localhost:3000/api/users -H 'Content-Type: application/json' -d '{}' -w '\n%{http_code}'`
- `node -e "console.log(require('http-errors').createError(404, 'User not found'))"`

**Examples:**
- curl -s http://localhost:3000/api/users/999 | python -m json.tool
- curl -s -X POST http://localhost:3000/api/users -H 'Content-Type: application/json' -d '{}' -w 'status=%{http_code}\n'
- node -e "console.log(JSON.stringify(require('http-errors').createError(422, 'Validation failed')))"

### error-docs
Document error responses in OpenAPI with reusable schemas and examples

**Parameters:**
- `spec` (string): OpenAPI spec path

**Commands:**
- `swagger-cli validate openapi.yaml`
- `redocly lint openapi.yaml`
- `curl -s http://localhost:3000/api/docs -o /dev/null -w '%{http_code}'`
- `openapi-generator validate -i openapi.yaml`
- `npx @stoplight/spectral-cli lint openapi.yaml`

**Examples:**
- swagger-cli validate openapi.yaml && redocly lint openapi.yaml
- npx @stoplight/spectral-cli lint --ruleset error-docs.yaml openapi.yaml
- openapi-generator validate -i openapi.yaml

## References
- [RFC 9457 Problem Details](https://www.rfc-editor.org/rfc/rfc9457)
- [http-errors](https://github.com/jshttp/http-errors)
- [FastAPI Exception Handling](https://fastapi.tiangolo.com/tutorial/handling-errors/)