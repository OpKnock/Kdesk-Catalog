# api-error-engineer

Implements consistent API error handling: RFC 9457 problem details middleware, error codes, and OpenAPI error documentation.

## Instructions

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