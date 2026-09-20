---
name: "mock-server-generation"
description: "Generate mock servers from OpenAPI specs: Prism, WireMock stubs, and OpenAPI Generator server skeletons. Use when working with mock server generate, api or when the user mentions mock server generate, api."
---

Generate mock servers from OpenAPI specs: Prism, WireMock stubs, and OpenAPI Generator server skeletons.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx @stoplight/prism-cli mock openapi.yaml`
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
