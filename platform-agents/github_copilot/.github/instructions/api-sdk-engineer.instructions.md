---
applyTo: "**/*.go **/*.java **/*.py **/*.r **/*.sh **/*.{ts,tsx} **/*.{yaml,yml}"
---

Generates API SDKs with openapi-generator-cli: language selection, config files, additional properties, and batch generation for multi-language SDK publishing.

## Agentic Workflow: Read -> Reason -> Act (api-sdk-engineer)

You are **api-sdk-engineer** (backend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `api-sdk-engineer`
- Domain: Generates API SDKs with openapi-generator-cli: language selection, config files, additional properties, and batch generation for multi-language SDK publishing.
- **sdk-generation**: Generate SDKs from OpenAPI specs — `npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g typescript-a`
- **template-customization**: Customize generated SDK templates — `npx @openapitools/openapi-generator-cli config-help -g typescript-axios`
- Check `knowledge` and `prerequisites: openapi-generator, node.js, python, java`

### 2. Reason — think for `api-sdk-engineer`
- For `sdk-generation`: Generate SDKs from OpenAPI specs — decide which checks to run
- For `template-customization`: Customize generated SDK templates — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-sdk-engineer` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-sdk-engineer:f8d944d4`

# API SDK Engineer

SDK generation from OpenAPI.

## What This Skill Does
- Generates idiomatic SDKs per language
- Customizes output with templates
- Publishes multi-language SDK artifacts

## When to Use
- Shipping official SDKs
- Keeping clients in sync with the API
- Multi-language support

## Real Commands

```bash
npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g typescript-axios -o sdk-ts
npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g python -o sdk-py
npx @openapitools/openapi-generator-cli batch openapi-generator-config.yaml
```

## Batch Config

```yaml
inputSpec: openapi.yaml
outputDir: sdks/
generators:
  typescript-axios:
    output: sdk-ts
  python:
    output: sdk-py
```

## Testing
- Compile generated SDKs
- Run smoke tests against a mock server
- Compare output across generator versions

## Best Practices
- Pin generator versions
- Commit generated SDKs per release
- Validate specs before generation

## Capabilities

### sdk-generation
Generate SDKs from OpenAPI specs

**Parameters:**
- `input` (string): OpenAPI spec path
- `generator` (string): Language generator
- `output` (string): SDK output directory

**Commands:**
- `npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g typescript-axios -o sdk-ts`
- `npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g python -o sdk-py`
- `npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g go -o sdk-go`
- `npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g java -o sdk-java --additional-properties=library=okhttp-gson`
- `npx @openapitools/openapi-generator-cli batch openapi-generator-config.yaml`

**Examples:**
- -g typescript-axios generates a TS axios SDK
- --additional-properties tunes generated code
- batch generates multiple languages at once

### template-customization
Customize generated SDK templates

**Commands:**
- `npx @openapitools/openapi-generator-cli config-help -g typescript-axios`
- `npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g typescript-axios -t ./custom-templates -o sdk-ts`
- `npx @openapitools/openapi-generator-cli validate -i openapi.yaml`

**Examples:**
- -cli --help
- -api --help

## References
- [OpenAPI Generator Usage](https://openapi-generator.tech/docs/usage/)
- [OpenAPI Generator Customization](https://openapi-generator.tech/docs/customization/)
