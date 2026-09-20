---
applyTo: "**/*.java **/*.json **/*.r **/*.sh **/*.{yaml,yml}"
---

# Mock Server Generation

Generate mock servers from OpenAPI specs: Prism, WireMock stubs, and OpenAPI Generator server skeletons.

## Instructions

# Mock Server Generation

Turn an OpenAPI spec into a running mock server in seconds so frontend and tests never block on backend availability.

## What this skill does

- Runs Prism mock servers straight from the spec
- Creates and manages WireMock stub mappings over the admin API
- Generates full server skeletons with openapi-generator

## When to use

- Frontend development before the backend exists
- Contract-based integration tests
- Demonstrations and demo environments

## Real commands

```bash
# Dynamic mock from spec (synthetic example data)
npx @stoplight/prism-cli mock openapi.yaml
npx @stoplight/prism-cli mock -p 4010 openapi.yaml

# WireMock standalone
java -jar wiremock-standalone.jar --port 8080 --verbose

# Register a stub mapping
curl -X POST http://localhost:8080/__admin/mappings -d @stub.json

# List registered mappings
curl http://localhost:8080/__admin/mappings

# Generate a Node express skeleton server
openapi-generator-cli generate -g nodejs-express-server -i openapi.yaml -o mock-server/
```

## stub.json example

```json
{
  "request": { "method": "GET", "url": "/api/users/1" },
  "response": { "status": 200, "jsonBody": { "id": 1, "name": "Alice" } }
}
```

## Best practices

- Validate the spec first (`openapi-generator-cli validate -i openapi.yaml`)
- Use Prism for dynamic mocks, WireMock for deterministic stubs
- Keep generated skeletons out of version control or regenerate on spec change

## Capabilities

### mock-server-generate
Generate and run mock servers from an OpenAPI/Swagger specification, and manage WireMock stubs.

**Commands:**
- `npx @stoplight/prism-cli mock openapi.yaml`
- `npx @stoplight/prism-cli mock -p 4010 openapi.yaml`
- `java -jar wiremock-standalone.jar --port 8080 --verbose`
- `curl -X POST http://localhost:8080/__admin/mappings -d @stub.json`
- `openapi-generator-cli generate -g nodejs-express-server -i openapi.yaml -o mock-server/`

**Examples:**
- npx @stoplight/prism-cli mock -p 4010 petstore.yaml
- curl -X POST http://localhost:8080/__admin/mappings -d '{"request":{"method":"GET","url":"/api/users"},"response":{"status":200,"jsonBody":[{"id":1}]}}'
- openapi-generator-cli generate -g go-server -i openapi.yaml -o out/
