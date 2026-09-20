---
name: "client-generation"
description: "Generate API clients from OpenAPI specs with openapi-generator, swagger-codegen, and oapi-codegen across many languages. Use when working with openapi generator, oapi codegen or when the user mentions openapi generator, oapi codegen."
license: "MIT"
compatibility: "Requires npx, oapi-codegen."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(go:*) Bash(npx:*) Bash(oapi-codegen:*)"
---

Generate API clients from OpenAPI specs with openapi-generator, swagger-codegen, and oapi-codegen across many languages.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx @openapitools/openapi-generator-cli generate -i openapi.`, `go install github.com/oapi-codegen/oapi-codegen/v2/cmd/oapi-`
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

# Client Generation

Generate typed API clients directly from OpenAPI specifications.

## When to Use

- Producing SDKs for consumers of your API
- Keeping client and server types in sync from one spec
- Generating clients in multiple languages from one source

## openapi-generator-cli

```bash
npx @openapitools/openapi-generator-cli generate \
  -i openapi.yaml -g typescript-fetch -o src/client

# Go client
npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g go -o gen/go

# Python client with package name
npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g python -o gen/python --package-name myapi
```

List generators:

```bash
npx @openapitools/openapi-generator-cli list | grep -i "typescript\|go\|python"
```

## oapi-codegen (Go)

```bash
go install github.com/oapi-codegen/oapi-codegen/v2/cmd/oapi-codegen@latest

oapi-codegen -package api -generate types,client openapi.yaml > gen/client.gen.go
oapi-codegen -package api -generate types,chi-server,spec openapi.yaml > gen/server.gen.go
```

## Config via openapitools.json

```json
{
  "generator-cli": {
    "version": "7.8.0",
    "generators": {
      "typescript": {
        "generatorName": "typescript-fetch",
        "inputSpec": "openapi.yaml",
        "output": "src/client"
      }
    }
  }
}
```

## Testing

```bash
npx @openapitools/openapi-generator-cli validate -i openapi.yaml
npm run build
npx tsc --noEmit
```

## Best Practices

- Validate the spec before generating: `openapi-generator-cli validate -i openapi.yaml`
- Commit generated clients separately from the spec
- Regenerate on every spec change, ideally in CI
- Use config files to lock generator versions
- Review generated code with linting in CI

## Capabilities

### openapi-generator
Generate typed API clients from OpenAPI/Swagger specs with OpenAPI Generator

**Parameters:**
- `spec` (string): Path or URL to the OpenAPI spec
- `generator` (string): Generator name such as typescript-fetch, go, python, java
- `output` (string): Output directory for generated code

**Commands:**
- `npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g typescript-fetch -o src/client`
- `npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g go -o gen/go`
- `npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g python -o gen/python --package-name myapi`
- `npx @openapitools/openapi-generator-cli version`

**Examples:**
- npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g typescript-fetch -o src/client
- npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g java -o gen/java --library resttemplate
- npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g go -o gen/go --additional-properties=withGoMod=false

### oapi-codegen
Generate Go clients and servers with oapi-codegen

**Parameters:**
- `package_name` (string): Go package name for generated code
- `generate` (string): Comma-separated generators: types, client, chi-server, spec

**Commands:**
- `go install github.com/oapi-codegen/oapi-codegen/v2/cmd/oapi-codegen@latest`
- `oapi-codegen -package api -generate types,client openapi.yaml > gen/client.gen.go`
- `oapi-codegen -package api -generate types,chi-server openapi.yaml > gen/server.gen.go`
- `go build ./...`

**Examples:**
- oapi-codegen -package api -generate types,client openapi.yaml > gen/client.gen.go
- oapi-codegen -package api -generate types,chi-server,spec openapi.yaml > gen/server.gen.go
- go test ./...

## References
- [OpenAPI Generator Docs](https://openapi-generator.tech/docs/usage)
- [oapi-codegen Docs](https://github.com/oapi-codegen/oapi-codegen)
