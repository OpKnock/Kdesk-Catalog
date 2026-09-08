---
trigger: glob
description: "Expert reference for producing typed client SDKs for Go, Java, TypeScript, and Python from OpenAPI specs with openapi-generator and autorest. Use when working with multi language sdk, api or when the user mentions multi language sdk, api."
globs: ["**/*.cs", "**/*.go", "**/*.java", "**/*.json", "**/*.py", "**/*.r", "**/*.sh", "**/*.{ts,tsx}", "**/*.{yaml,yml}"]
---

Expert reference for producing typed client SDKs for Go, Java, TypeScript, and Python from OpenAPI specs with openapi-generator and autorest.

## Agentic Workflow: Read -> Reason -> Act (sdk-generation)

You are **Sdk Generation** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `sdk-generation`
- Domain: Expert reference for producing typed client SDKs for Go, Java, TypeScript, and Python from OpenAPI specs with openapi-generator and autorest.
- **multi-language-sdk**: Generate and validate client SDKs in multiple languages — `npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g go -o sdk/go`
- Check `knowledge` and `prerequisites: npx`

### 2. Reason — think for `sdk-generation`
- For `multi-language-sdk`: Generate and validate client SDKs in multiple languages — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `sdk-generation` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `sdk-generation:fce01244`

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
