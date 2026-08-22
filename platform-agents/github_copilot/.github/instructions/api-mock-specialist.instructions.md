---
applyTo: "**/*.r **/*.sh **/*.{yaml,yml}"
---

# api-mock-specialist

Generates mock API servers directly from OpenAPI documents using Stoplight Prism, with dynamic examples, validation, and path/query behavior configuration.

## Instructions

# API Mock Specialist

Mocks APIs from OpenAPI documents with Prism.

## What This Skill Does
- Serves any OpenAPI file as a running mock server
- Returns example or generated responses per operation
- Validates incoming requests against schemas

## When to Use
- Contract-first development where the spec exists before code
- Providing frontends a spec-accurate backend instantly
- Demo environments for API products

## Real Commands

```bash
npx @stoplight/prism-cli mock openapi.yaml
npx @stoplight/prism-cli mock -d -p 4010 openapi.yaml
curl -s http://localhost:4010/users | jq .
```

## Behavior Config

```yaml
x-mock-response:
  headers:
    X-RateLimit-Remaining: 40
x-example: null   # forces generation
```

Inline annotations in the spec control mock output per operation.

## Testing
- Hit endpoints and confirm responses conform to schemas
- Send invalid bodies to observe validation error responses
- Test 404 behavior with unlisted resource ids

## Best Practices
- Keep the mock spec in sync with the real implementation spec
- Use -d mode when exact examples matter to consumers
- Point CI contract tests at Prism before the real API exists

## Capabilities

### prism-mocking
Serve an OpenAPI-defined mock API with Prism

**Commands:**
- `npx @stoplight/prism-cli mock openapi.yaml`
- `npx @stoplight/prism-cli mock -d -p 4010 openapi.yaml`
- `npx @stoplight/prism-cli mock openapi.yaml --errors`
- `curl -s http://localhost:4010/users | jq .`
- `curl -s -o /dev/null -w '%{http_code}\n' http://localhost:4010/users/999999`

**Examples:**
- prism mock -d openapi.yaml uses example values instead of generated ones
- prism mock -p 4010 openapi.yaml serves the spec on port 4010
- prism mock --errors returns 500-style dynamic responses for malformed requests

### spec-validation
Validate the OpenAPI document before mocking it

**Commands:**
- `npx swagger-cli validate openapi.yaml`
- `npx @stoplight/prism-cli mock --help`
- `curl -s http://localhost:4010/__prism/health`

**Examples:**
- -cli --help
- -api --help
