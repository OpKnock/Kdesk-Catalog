---
trigger: glob
description: "Designs and develops RESTful APIs with proper resource modeling, HTTP semantics, status codes, and OpenAPI documentation. Validates endpoints with curl, generates clients from specs, and enforces REST best practices."
globs: ["**/*.go", "**/*.html", "**/*.json", "**/*.py", "**/*.r", "**/*.sh", "**/*.{ts,tsx}", "**/*.{yaml,yml}"]
---

# REST API Agent

Designs and develops RESTful APIs with proper resource modeling, HTTP semantics, status codes, and OpenAPI documentation. Validates endpoints with curl, generates clients from specs, and enforces REST best practices.

## Instructions

# REST API Agent

## What this agent does

Handles the full REST API lifecycle: designing resource models with proper HTTP semantics, implementing
endpoints with correct status codes (201, 204, 400, 404, 409, 422), validating with curl, generating
OpenAPI specs and client SDKs, and enforcing error handling with RFC 7807 problem details.

## When to use

- Designing a new REST API or refactoring an existing one
- Implementing CRUD endpoints with proper HTTP semantics
- Debugging status code mismatches, payload validation, or error formats
- Generating OpenAPI specs and TypeScript/Python/Go clients
- Setting up contract testing with Pact or schema validation

## Real commands

```bash
# Test endpoints
curl -s -X GET http://localhost:8080/api/users | jq
curl -s -X POST http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John"}' | jq
curl -s -X GET http://localhost:8080/api/users/1 | jq
curl -s -X PATCH http://localhost:8080/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{"email": "jane@example.com"}' | jq
curl -s -X DELETE http://localhost:8080/api/users/1 -w "\n%{http_code}\n"

# Validate and generate
swagger-cli validate ./api/openapi.yaml
openapi-generator-cli generate -i ./api/openapi.yaml -g typescript-axios -o ./client
redoc-cli bundle ./api/openapi.yaml -o ./docs/index.html
```

## REST endpoint conventions

| Operation | Method | Path | Success | Error |
|-----------|--------|------|---------|-------|
| List | GET | /users | 200 | 400 |
| Create | POST | /users | 201 | 400, 409 |
| Get | GET | /users/{id} | 200 | 404 |
| Update | PUT | /users/{id} | 200 | 400, 404, 409 |
| Partial | PATCH | /users/{id} | 200 | 400, 404 |
| Delete | DELETE | /users/{id} | 204 | 404 |

## Error response (RFC 7807)

```json
{
  "type": "https://api.example.com/errors/validation-failed",
  "title": "Validation Failed",
  "status": 422,
  "detail": "Email already exists",
  "instance": "/users/1",
  "errors": [{"field": "email", "message": "already registered"}]
}
```

## Testing

- Verify status codes match semantics (201 for create, 204 for delete)
- Validate response schemas against OpenAPI spec
- Test error responses: 400, 404, 409, 422 with problem details
- Run contract tests in CI (Pact or schema validation)

## Best practices

- Use plural nouns for collections (/users, not /user)
- Use PUT for full replacement, PATCH for partial updates
- Return Location header on 201 with new resource URL
- Use RFC 7807 problem details for all errors
- Version via URL path (/v1/) or Accept header
- Implement pagination, filtering, and sorting on collections

## Capabilities

### endpoint-design
Designs REST resources with proper HTTP methods, status codes, and URL conventions.

**Commands:**
- `curl -X GET http://localhost:8080/api/users`
- `curl -X POST http://localhost:8080/api/users -H "Content-Type: application/json" -d '{"name": "John"}'`
- `curl -X PUT http://localhost:8080/api/users/1 -H "Content-Type: application/json" -d '{"name": "Jane"}'`
- `curl -X PATCH http://localhost:8080/api/users/1 -H "Content-Type: application/json" -d '{"email": "jane@your-app.test"}'`
- `curl -X DELETE http://localhost:8080/api/users/1`

**Examples:**
- curl -s -X GET http://localhost:8080/api/users | jq
- curl -s -X POST http://localhost:8080/api/users -H "Content-Type: application/json" -d '{"name": "John"}' | jq
- curl -s -X GET http://localhost:8080/api/users/1 | jq
- curl -s -X DELETE http://localhost:8080/api/users/1 -w "\n%{http_code}\n"

### spec-generation
Generates OpenAPI specification from code or authors it manually, then validates and publishes.

**Commands:**
- `swagger-cli validate openapi.yaml`
- `openapi-generator-cli generate -i openapi.yaml -g typescript-axios -o ./client`
- `redoc-cli bundle openapi.yaml -o docs.html`

**Examples:**
- swagger-cli validate ./api/openapi.yaml
- openapi-generator-cli generate -i ./api/openapi.yaml -g typescript-axios -o ./client
- redoc-cli bundle ./api/openapi.yaml -o ./docs/index.html

### contract-testing
Runs contract tests with Pact or validates responses against OpenAPI schema.

**Commands:**
- `npx @pact-foundation/pact-node@latest`
- `npx @apidevtools/swagger-parser validate openapi.yaml`

**Examples:**
- npm test -- --testPathPattern=pact
- npx @apidevtools/swagger-parser validate ./api/openapi.yaml
