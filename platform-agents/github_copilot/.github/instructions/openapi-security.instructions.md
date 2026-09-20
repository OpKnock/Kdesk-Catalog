---
applyTo: "**/*.r **/*.sh **/*.{yaml,yml}"
---

# Openapi Security

Authors OpenAPI security schemes including apiKey, HTTP bearer JWT, OAuth2 flows, and mutual TLS. Validates schemes with Spectral, Redocly, and openapi-generator in CI.

## Instructions

# OpenAPI Security

Security schemes describe HOW clients authenticate; security requirements describe WHERE.

## What this skill does

- Writes securitySchemes for every auth style
- Applies security requirements globally or per-operation
- Validates with linters and generators

## When to use

- Documenting auth on a new API
- Catching missing or misapplied security in CI

## Real commands

```bash
openapi-generator-cli validate -i openapi.yaml
spectral lint openapi.yaml
redocly lint openapi.yaml --extends recommended
```

## Example schemes

```yaml
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
    apiKeyHeader:
      type: apiKey
      in: header
      name: X-API-Key
    oauth:
      type: oauth2
      flows:
        clientCredentials:
          tokenUrl: https://auth.your-app.test/token
          scopes:
            read: Read access
            write: Write access
security:
  - bearerAuth: []
```

## Per-operation override

```yaml
paths:
  /public:
    get:
      security: []
```

## Best practices

- Always add a global `security` block
- Test client generation with `openapi-generator-cli generate`
- Lint in CI so every PR re-validates schemes

## Capabilities

### openapi-security-schemes
Author security schemes and requirements, then lint and validate them with Spectral and openapi-generator.

**Commands:**
- `openapi-generator-cli validate -i openapi.yaml`
- `spectral lint openapi.yaml`
- `npx @stoplight/spectral-cli lint openapi.yaml -r security.rules.yaml`
- `redocly lint openapi.yaml --extends recommended`
- `curl -s https://api.your-app.test/.well-known/openapi.yaml | openapi-generator-cli validate -i /dev/stdin`

**Examples:**
- spectral lint openapi.yaml
- openapi-generator-cli validate -i openapi.yaml
- redocly lint openapi.yaml
