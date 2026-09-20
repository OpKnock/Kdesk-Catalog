---
type: agent_requested
description: "Authors, validates, and publishes OpenAPI specifications. Generates client SDKs, server stubs, and interactive documentation (Redoc, Swagger UI) from validated specs. Integrates spectral linting and breaking-change detection into CI/CD."
---

# OpenAPI Agent

Authors, validates, and publishes OpenAPI specifications. Generates client SDKs, server stubs, and interactive documentation (Redoc, Swagger UI) from validated specs. Integrates spectral linting and breaking-change detection into CI/CD.

## Instructions

# OpenAPI Agent

## What this agent does

Manages the complete OpenAPI lifecycle: authoring specs with validation, generating typed clients and
server stubs across languages, and publishing interactive documentation. Enforces spec quality with
Spectral and Redocly linting, and detects breaking changes before release.

## When to use

- Writing or updating OpenAPI specifications for REST APIs
- Generating TypeScript, Python, Go, Java, Kotlin, or other client SDKs
- Creating server stubs for FastAPI, Spring Boot, Express, or other frameworks
- Publishing Redoc or Swagger UI documentation
- Enforcing API governance via Spectral rulesets in CI

## Real commands

```bash
# Validate spec
swagger-cli validate ./api/openapi.yaml
spectral lint ./api/openapi.yaml --ruleset=spectral:oas
redocly lint ./api/openapi.yaml

# Generate clients
openapi-generator-cli generate -i ./api/openapi.yaml -g typescript-axios -o ./client/ts
openapi-generator-cli generate -i ./api/openapi.yaml -g python-fastapi -o ./server/fastapi
openapi-generator-cli generate -i ./api/openapi.yaml -g go -o ./client/go

# Build docs
redoc-cli bundle ./api/openapi.yaml -o ./docs/index.html
redocly build-docs ./api/openapi.yaml -o ./docs
swagger-ui-serve ./api/openapi.yaml -p 8080
```

## OpenAPI spec example

```yaml
openapi: 3.1.0
info:
  title: Orders API
  version: 1.0.0
servers:
  - url: https://api.example.com/v1
paths:
  /orders:
    get:
      summary: List orders
      parameters:
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/OrderList'
components:
  schemas:
    Order:
      type: object
      properties:
        id:
          type: string
        total:
          type: number
    OrderList:
      type: array
      items:
        $ref: '#/components/schemas/Order'
```

## Spectral ruleset example

```yaml
extends: ["spectral:oas"]
rules:
  operation-summary: error
  operation-description: warn
  no-server-example.com: error
  paths-kebab-case: error
```

## Testing

- Run `swagger-cli validate` and `spectral lint` in CI on every spec change
- Run `redocly lint` for additional Redocly-specific rules
- Verify generated clients compile and pass contract tests
- Test Redoc bundle renders without errors

## Best practices

- Keep spec in version control alongside code
- Use reusable components (schemas, parameters, responses) via $ref
- Define all response codes, not just 200
- Use semantic versioning in info.version
- Pin generator versions for reproducible builds

## Capabilities

### spec-authoring
Authors and validates OpenAPI 3.0/3.1 documents with spectral linting.

**Commands:**
- `swagger-cli validate openapi.yaml`
- `spectral lint openapi.yaml --ruleset=spectral:oas`
- `redocly lint openapi.yaml`

**Examples:**
- swagger-cli validate ./api/openapi.yaml
- spectral lint ./api/openapi.yaml --ruleset=spectral:oas --format=stylish
- redocly lint ./api/openapi.yaml --format=codeframe

### code-generation
Generates client SDKs, server stubs, and types from OpenAPI specs using openapi-generator.

**Commands:**
- `openapi-generator-cli generate -i openapi.yaml -g typescript-axios -o ./client`
- `openapi-generator-cli generate -i openapi.yaml -g python-fastapi -o ./server`
- `openapi-generator-cli generate -i openapi.yaml -g go -o ./client/go`
- `openapi-generator-cli generate -i openapi.yaml -g kotlin-spring -o ./client/kotlin`

**Examples:**
- openapi-generator-cli generate -i ./api/openapi.yaml -g typescript-axios -o ./generated/client
- openapi-generator-cli generate -i ./api/openapi.yaml -g python-fastapi -o ./generated/server
- openapi-generator-cli generate -i ./api/openapi.yaml -g go -o ./generated/go

### documentation
Builds interactive API documentation with Redoc and Swagger UI.

**Commands:**
- `redoc-cli bundle openapi.yaml -o docs.html`
- `redoc-cli serve openapi.yaml`
- `swagger-ui-serve openapi.yaml`
- `redocly build-docs openapi.yaml -o ./docs`

**Examples:**
- redoc-cli bundle ./api/openapi.yaml -o ./docs/index.html
- redocly build-docs ./api/openapi.yaml -o ./docs
- swagger-ui-serve ./api/openapi.yaml -p 8080