---
name: "openapi-security"
description: "Authors OpenAPI security schemes including apiKey, HTTP bearer JWT, OAuth2 flows, and mutual TLS. Validates schemes with Spectral, Redocly, and openapi-generator in CI. Use when working with openapi security schemes or when the user mentions openapi security schemes."
---

Authors OpenAPI security schemes including apiKey, HTTP bearer JWT, OAuth2 flows, and mutual TLS. Validates schemes with Spectral, Redocly, and openapi-generator in CI.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `openapi-generator-cli validate -i openapi.yaml`
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
