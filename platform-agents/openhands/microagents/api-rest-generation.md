---
name: "api-rest-generation"
description: "Generates REST clients and documentation from OpenAPI with openapi-generator-cli and Redocly: multi-language client generation, config files, and docs deployment."
type: knowledge
triggers: ["api-rest-generation", "client-generation", "docs-deployment"]
---

# Api Rest Generation

Generates REST clients and documentation from OpenAPI with openapi-generator-cli and Redocly: multi-language client generation, config files, and docs deployment.

## Instructions

# API REST v5 - Clients & Docs

Code and doc generation from OpenAPI.

## What This Skill Does
- Generates clients for TS, Python, Go, Java
- Builds static docs from the spec
- Keeps generated artifacts in sync

## When to Use
- Releasing official SDKs
- Sharing docs with consumers
- Multi-language client support

## Real Commands

```bash
npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g typescript-fetch -o ./client-ts
npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g python -o ./client-py
npx @redocly/cli build-docs openapi.yaml -o dist/api.html
```

## Generation Config

```yaml
inputSpec: openapi.yaml
generators:
  typescript-fetch:
    output: client-ts
    additionalProperties:
      useSingleRequestParameter: true
```

## Testing
- Compile each generated client
- Run a smoke call against the live API
- Diff generated output on spec changes

## Best Practices
- Commit generated clients in SDK repos
- Regenerate on tagged releases only
- Validate specs before generation

## Capabilities

### client-generation
Generate typed API clients in multiple languages

**Commands:**
- `npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g typescript-fetch -o ./client-ts`
- `npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g python -o ./client-py`
- `npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g go -o ./client-go`
- `npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g java -o ./client-java`
- `npx @openapitools/openapi-generator-cli config-help -g typescript-fetch`

**Examples:**
- -g typescript-fetch produces a fetch-based TS client
- -g python generates a requests-based client
- config-help documents generator options

### docs-deployment
Build and preview reference documentation

**Commands:**
- `npx @redocly/cli build-docs openapi.yaml -o dist/api.html`
- `npx @redocly/cli preview-docs openapi.yaml`
- `npx @redocly/cli bundle openapi.yaml -o dist/openapi.bundle.yaml`
- `npx @redocly/cli lint openapi.yaml`
