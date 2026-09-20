---
name: "openapi"
description: "Authors, validates, lints, bundles, and generates code from OpenAPI 3.x specifications. Supports contract-first development with Redocly, Spectral, and openapi-generator tooling. Use when working with openapi authoring or when the user mentions openapi authoring."
---

Authors, validates, lints, bundles, and generates code from OpenAPI 3.x specifications. Supports contract-first development with Redocly, Spectral, and openapi-generator tooling.

## Agentic Workflow: Read -> Reason -> Act (openapi)

You are **Openapi** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `openapi`
- Domain: Authors, validates, lints, bundles, and generates code from OpenAPI 3.x specifications. Supports contract-first development with Redocly, Spectral, and openapi-generator tooling.
- **openapi-authoring**: Validate, lint, bundle and generate code from OpenAPI 3.x specifications. — `openapi-generator-cli validate -i openapi.yaml`
- Check `knowledge` and `prerequisites: npx, openapi-generator-cli, redocly, swagger-cli`

### 2. Reason — think for `openapi`
- For `openapi-authoring`: Validate, lint, bundle and generate code from OpenAPI 3.x specifications. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `openapi` tools
- Tools: `Glob`, `Grep`, `Read`, `Openapi-generator-cli`, `Redocly` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `openapi:67db851b`

# OpenAPI

OpenAPI 3.x is the standard for describing REST APIs: paths, schemas, parameters and security.

## What this skill does

- Validates and lints specs
- Bundles multi-file specs into one
- Generates clients and servers

## When to use

- Starting a new API contract
- Keeping docs in sync with implementation

## Real commands

```bash
# Validate
openapi-generator-cli validate -i openapi.yaml
swagger-cli validate openapi.yaml

# Lint
redocly lint openapi.yaml --extends recommended

# Bundle
npx @redocly/cli bundle openapi.yaml -o bundle.yaml

# Generate clients
openapi-generator-cli generate -g python -i openapi.yaml -o generated/
openapi-generator-cli generate -g typescript-axios -i openapi.yaml -o out/
```

## Minimal spec

```yaml
openapi: 3.0.3
info:
  title: Example API
  version: 1.0.0
paths:
  /health:
    get:
      responses:
        '200':
          description: OK
```

## Best practices

- Write the spec before the code (contract-first)
- Keep one spec file per API, reference external $refs
- Run lint + validate in CI

## Capabilities

### openapi-authoring
Validate, lint, bundle and generate code from OpenAPI 3.x specifications.

**Parameters:**
- `spec` (string): Path to the OpenAPI file
- `generator` (string): Code generation language/target
- `output` (string): Output directory for generated code

**Commands:**
- `openapi-generator-cli validate -i openapi.yaml`
- `redocly lint openapi.yaml`
- `npx @redocly/cli bundle openapi.yaml -o bundle.yaml`
- `openapi-generator-cli generate -g python -i openapi.yaml -o generated/`
- `swagger-cli validate openapi.yaml`

**Examples:**
- redocly lint openapi.yaml --extends recommended
- openapi-generator-cli generate -g typescript-axios -i openapi.yaml -o out/
- npx @redocly/cli bundle openapi.yaml --ext json

## References
- [OpenAPI Specification](https://spec.openapis.org/oas/v3.1.0.html)
- [Redocly CLI Docs](https://redocly.com/docs/cli/)
- [OpenAPI Generator](https://github.com/OpenAPITools/openapi-generator)
