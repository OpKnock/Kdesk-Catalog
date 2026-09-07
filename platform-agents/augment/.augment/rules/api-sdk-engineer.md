---
type: agent_requested
description: "Generates API SDKs with openapi-generator-cli: language selection, config files, additional properties, and batch generation for multi-language SDK publishing. Use when working with sdk generation, template customization or when the user mentions sdk generation, template customization."
---

Generates API SDKs with openapi-generator-cli: language selection, config files, additional properties, and batch generation for multi-language SDK publishing.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npx @openapitools/openapi-generator-cli generate -i openapi.`, `npx @openapitools/openapi-generator-cli config-help -g types`
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