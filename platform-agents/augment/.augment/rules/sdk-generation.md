---
type: agent_requested
description: "Expert reference for producing typed client SDKs for Go, Java, TypeScript, and Python from OpenAPI specs with openapi-generator and autorest. Use when working with multi language sdk, api or when the user mentions multi language sdk, api."
---

Expert reference for producing typed client SDKs for Go, Java, TypeScript, and Python from OpenAPI specs with openapi-generator and autorest.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx @openapitools/openapi-generator-cli generate -i openapi.`
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

# SDK Generation

Expert skill for generating client SDKs from API specs.

## What this skill does

- Generates typed clients for Go, Java, TypeScript, and Python
- Configures libraries and code style per generator
- Compiles the output to verify the SDK is usable

## When to use

- Publishing a public API and shipping official clients
- Internal services that share one contract with many teams
- Avoiding hand-maintained HTTP wrappers

## Real commands

```bash
# Go SDK
npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g go -o sdk/go

# Java with OkHttp/Gson
npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g java -o sdk/java --library=okhttp-gson

# TypeScript with fetch
npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g typescript-fetch -o sdk/ts --additional-properties=supportsES6=true

# Python
npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g python -o sdk/python

# Inspect generator options before generating
npx @openapitools/openapi-generator-cli config-help -g python

# C# with AutoRest
npx autorest --input-file=swagger.json --csharp --output-folder=./sdk/csharp
```

## Verify the output

```bash
cd sdk/python && pip install -e . && python -c 'from openapi_client.api.orders_api import OrdersApi; print(OrdersApi)'
cd sdk/go && go build ./...
cd sdk/ts && npm i && npx tsc --noEmit
```

## Versioning the SDK

- Tag releases with the API version: sdk-v1.2.0
- Regenerate only from tagged specs

## Best practices

- Pin the generator version for reproducible output
- Commit generated code to give consumers stable imports
- Add a smoke test that calls the live API with the generated client

## Capabilities

### multi-language-sdk
Generate and validate client SDKs in multiple languages

**Parameters:**
- `language` (string): Target language and library, e.g. java + okhttp-gson
- `input` (string): OpenAPI or Swagger input file
- `output` (string): Output directory for the generated SDK

**Commands:**
- `npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g go -o sdk/go`
- `npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g java -o sdk/java --library=okhttp-gson`
- `npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g typescript-fetch -o sdk/ts --additional-properties=supportsES6=true`
- `npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g python -o sdk/python`
- `npx @openapitools/openapi-generator-cli config-help -g python`

**Examples:**
- npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g java -o sdk/java --library=okhttp-gson
- npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g typescript-fetch -o sdk/ts
- npx autorest --input-file=swagger.json --csharp --output-folder=./sdk/csharp

## References
- [OpenAPI Generator generators list](https://openapi-generator.tech/docs/generators)
- [AutoRest docs](https://github.com/Azure/autorest)