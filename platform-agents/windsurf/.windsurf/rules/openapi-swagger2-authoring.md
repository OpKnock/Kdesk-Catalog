---
trigger: glob
description: "Validates, bundles, and upgrades Swagger 2.0 specifications to OpenAPI 3.x using swagger-cli, Redocly, and openapi-generator. Supports legacy API maintenance and migration workflows. Use when working with swagger2 authoring, api or when the user mentions swagger2 authoring, api."
globs: ["**/*.go", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

Validates, bundles, and upgrades Swagger 2.0 specifications to OpenAPI 3.x using swagger-cli, Redocly, and openapi-generator. Supports legacy API maintenance and migration workflows.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `swagger-cli validate swagger.yaml`
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

# OpenAPI v2 (Swagger 2.0)

Legacy APIs still run on Swagger 2.0; know how to validate, bundle and upgrade them.

## What this skill does

- Validates v2 documents
- Bundles multi-file v2 specs
- Upgrades v2 to OpenAPI 3.x

## When to use

- Maintaining legacy swagger files
- Migrating tooling to OpenAPI 3

## Real commands

```bash
# Validate
swagger-cli validate swagger.yaml

# Bundle
npx swagger-cli bundle swagger.yaml -o bundle.yaml

# Lint
npx @redocly/cli lint swagger.yaml

# Generate
openapi-generator-cli generate -g go -i swagger.yaml -o out/

# Upgrade to v3
npx @redocly/cli bundle swagger.yaml --upgrade -o openapi.yaml
```

## Key v2 differences

- `swagger: "2.0"` instead of openapi version key
- `host`, `basePath`, `schemes` at root
- `securityDefinitions` instead of components/securitySchemes

## Example

```yaml
swagger: "2.0"
info: { title: Legacy API, version: "1.0" }
host: api.your-app.test
basePath: /v1
schemes: [https]
paths:
  /ping:
    get:
      responses:
        '200': { description: OK }
securityDefinitions:
  api_key:
    type: apiKey
    in: header
    name: X-Api-Key
```

## Best practices

- Validate before upgrading to catch schema issues
- Upgrade one spec at a time and diff generated clients
- Keep v2 tooling pinned while migrating

## Capabilities

### swagger2-authoring
Validate and bundle Swagger 2.0 specs and convert them to OpenAPI 3.x.

**Parameters:**
- `spec` (string): Path to the Swagger 2.0 file
- `generator` (string): Code generation target
- `output` (string): Output file or directory

**Commands:**
- `swagger-cli validate swagger.yaml`
- `npx swagger-cli bundle swagger.yaml -o bundle.yaml`
- `openapi-generator-cli generate -g go -i swagger.yaml -o out/`
- `npx @redocly/cli lint swagger.yaml`
- `npx @redocly/cli bundle swagger.yaml --upgrade`

**Examples:**
- swagger-cli validate swagger.yaml
- openapi-generator-cli generate -g spring -i swagger.yaml -o out/
- npx @redocly/cli bundle swagger.yaml --upgrade -o openapi.yaml

## References
- [Swagger 2.0 Specification](https://swagger.io/specification/v2/)
- [swagger-cli](https://github.com/APIDevTools/swagger-cli)
