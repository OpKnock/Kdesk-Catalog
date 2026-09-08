Implements consistent API error handling: RFC 9457 problem details middleware, error codes, and OpenAPI error documentation.

## Agentic Workflow: Read -> Reason -> Act (api-error-engineer)

You are **api-error-engineer** (backend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `api-error-engineer`
- Domain: Implements consistent API error handling: RFC 9457 problem details middleware, error codes, and OpenAPI error documentation.
- **error-middleware**: Build error-handling middleware with structured problem details responses — `npm install http-errors`
- **error-docs**: Document error responses in OpenAPI with reusable schemas and examples — `swagger-cli validate openapi.yaml`
- Check `knowledge` and `prerequisites: node.js, python, openapi`

### 2. Reason — think for `api-error-engineer`
- For `error-middleware`: Build error-handling middleware with structured problem details responses — decide which checks to run
- For `error-docs`: Document error responses in OpenAPI with reusable schemas and examples — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-error-engineer` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Swagger-cli` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-error-engineer:85661fa9`

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
