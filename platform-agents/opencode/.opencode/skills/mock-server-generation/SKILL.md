---
name: "mock-server-generation"
description: "Generate mock servers from OpenAPI specs: Prism, WireMock stubs, and OpenAPI Generator server skeletons. Use when working with mock server generate, api or when the user mentions mock server generate, api."
---

Generate mock servers from OpenAPI specs: Prism, WireMock stubs, and OpenAPI Generator server skeletons.

## Agentic Workflow: Read -> Reason -> Act (mock-server-generation)

You are **Mock Server Generation** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `mock-server-generation`
- Domain: Generate mock servers from OpenAPI specs: Prism, WireMock stubs, and OpenAPI Generator server skeletons.
- **mock-server-generate**: Generate and run mock servers from an OpenAPI/Swagger specification, and manage WireMock stubs. — `npx @stoplight/prism-cli mock openapi.yaml`
- Check `knowledge` and `prerequisites: java, npx, openapi-generator-cli`

### 2. Reason — think for `mock-server-generation`
- For `mock-server-generate`: Generate and run mock servers from an OpenAPI/Swagger specification, and manage WireMock stubs. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `mock-server-generation` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx`, `Java` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `mock-server-generation:358c60e0`

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

**Parameters:**
- `spec` (string): Path to the OpenAPI YAML/JSON spec
- `port` (integer): Port for the mock server
- `generator` (string): openapi-generator language target, e.g. nodejs-express-server

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

## References
- [Prism Documentation](https://docs.stoplight.io/docs/prism)
- [WireMock Docs](https://wiremock.org/docs/)
- [OpenAPI Generator](https://github.com/OpenAPITools/openapi-generator)
