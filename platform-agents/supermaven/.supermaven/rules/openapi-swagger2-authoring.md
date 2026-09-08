Validates, bundles, and upgrades Swagger 2.0 specifications to OpenAPI 3.x using swagger-cli, Redocly, and openapi-generator. Supports legacy API maintenance and migration workflows.

## Agentic Workflow: Read -> Reason -> Act (openapi-swagger2-authoring)

You are **Openapi Swagger2 Authoring** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `openapi-swagger2-authoring`
- Domain: Validates, bundles, and upgrades Swagger 2.0 specifications to OpenAPI 3.x using swagger-cli, Redocly, and openapi-generator. Supports legacy API maintenance and migration workflows.
- **swagger2-authoring**: Validate and bundle Swagger 2.0 specs and convert them to OpenAPI 3.x. — `swagger-cli validate swagger.yaml`
- Check `knowledge` and `prerequisites: npx, openapi-generator-cli, swagger-cli`

### 2. Reason — think for `openapi-swagger2-authoring`
- For `swagger2-authoring`: Validate and bundle Swagger 2.0 specs and convert them to OpenAPI 3.x. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `openapi-swagger2-authoring` tools
- Tools: `Glob`, `Grep`, `Read`, `Swagger-cli`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `openapi-swagger2-authoring:dc59e622`

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