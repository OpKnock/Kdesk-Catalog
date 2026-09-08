---
type: agent_requested
description: "Authors OpenAPI security schemes including apiKey, HTTP bearer JWT, OAuth2 flows, and mutual TLS. Validates schemes with Spectral, Redocly, and openapi-generator in CI. Use when working with openapi security schemes or when the user mentions openapi security schemes."
---

Authors OpenAPI security schemes including apiKey, HTTP bearer JWT, OAuth2 flows, and mutual TLS. Validates schemes with Spectral, Redocly, and openapi-generator in CI.

## Agentic Workflow: Read -> Reason -> Act (openapi-security)

You are **Openapi Security** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `openapi-security`
- Domain: Authors OpenAPI security schemes including apiKey, HTTP bearer JWT, OAuth2 flows, and mutual TLS. Validates schemes with Spectral, Redocly, and openapi-generator in CI.
- **openapi-security-schemes**: Author security schemes and requirements, then lint and validate them with Spectral and openapi-gene — `openapi-generator-cli validate -i openapi.yaml`
- Check `knowledge` and `prerequisites: npx, openapi-generator-cli, redocly, spectral`

### 2. Reason — think for `openapi-security`
- For `openapi-security-schemes`: Author security schemes and requirements, then lint and validate them with Spectral and openapi-generator. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `openapi-security` tools
- Tools: `Glob`, `Grep`, `Read`, `Openapi-generator-cli`, `Spectral` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `openapi-security:8e38eeb4`

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

**Parameters:**
- `scheme_type` (string): apiKey, http, oauth2, openIdConnect, mutualTLS
- `flows` (object): OAuth2 flows: implicit, password, clientCredentials, authorizationCode
- `scopes` (array): Scopes referenced by security requirements

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

## References
- [OpenAPI Security Schemes](https://swagger.io/docs/specification/authentication/)
- [Spectral Rules](https://docs.stoplight.io/docs/spectral/reference/rules)