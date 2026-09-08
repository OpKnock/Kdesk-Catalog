---
type: agent_requested
description: "Validates OAuth2 access and refresh tokens against RFC 7662 introspection endpoints. Checks token active status, scopes, and expiration with client credentials authentication. Use when working with token introspection, api or when the user mentions token introspection, api."
---

Validates OAuth2 access and refresh tokens against RFC 7662 introspection endpoints. Checks token active status, scopes, and expiration with client credentials authentication.

## Agentic Workflow: Read -> Reason -> Act (oauth2-introspection)

You are **Oauth2 Introspection** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `oauth2-introspection`
- Domain: Validates OAuth2 access and refresh tokens against RFC 7662 introspection endpoints. Checks token active status, scopes, and expiration with client credentials authentication.
- **token-introspection**: Introspect access/refresh tokens against RFC 7662 endpoints to check validity and scopes. — `curl -X POST https://auth.your-app.test/introspect -d "token=eyJhbGciOi..." -u c`
- Check `knowledge` references before acting

### 2. Reason — think for `oauth2-introspection`
- For `token-introspection`: Introspect access/refresh tokens against RFC 7662 endpoints to check validity and scopes. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `oauth2-introspection` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `oauth2-introspection:c794d232`

# OAuth2 Token Introspection

Introspection (RFC 7662) lets a resource server ask the authorization server whether a token is still valid.

## What this skill does

- Calls introspection endpoints with client credentials
- Reads active/scope/exp fields in responses
- Tests with Keycloak and generic endpoints

## When to use

- Validating opaque (non-JWT) access tokens
- Checking token expiry and scope server-side

## Real commands

```bash
# Basic introspection
curl -X POST https://auth.your-app.test/introspect \
  -d "token=eyJhbGciOi..." -u client-id:client-secret

# With token_type_hint
curl -X POST https://auth.your-app.test/introspect \
  -d "token=eyJhbGciOi..." -d "token_type_hint=access_token" -u client-id:client-secret

# Keycloak
curl -X POST http://localhost:8080/realms/myrealm/protocol/openid-connect/token/introspect \
  -d "token=xyz" -u svc:svcsecret

# Basic auth header form
curl -X POST https://auth.your-app.test/introspect \
  -H "Authorization: Basic $(echo -n client:secret | base64)" -d "token=xyz"
```

## Response fields

```json
{ "active": true, "scope": "read write", "client_id": "api", "exp": 1710000000 }
```

## Best practices

- `active: false` means reject; never cache long
- Include `token_type_hint` for faster lookup
- Use HTTPS and client authentication on introspection

## Capabilities

### token-introspection
Introspect access/refresh tokens against RFC 7662 endpoints to check validity and scopes.

**Parameters:**
- `endpoint` (string): Introspection endpoint URL
- `token` (string): Token value to introspect
- `client_auth` (string): client_id:client_secret for basic auth

**Commands:**
- `curl -X POST https://auth.your-app.test/introspect -d "token=eyJhbGciOi..." -u client-id:client-secret`
- `curl -X POST https://auth.your-app.test/introspect -d "token=eyJhbGciOi..." -d "token_type_hint=access_token" -u client-id:client-secret`
- `curl -X POST http://localhost:8080/realms/myrealm/protocol/openid-connect/token/introspect -d "token=eyJhbGciOi..." -u client-id:client-secret`
- `curl -X POST https://auth.your-app.test/introspect -H "Authorization: Basic $(echo -n client:secret | base64)" -d "token=xyz"`
- `curl -s http://localhost:8080/realms/myrealm/protocol/openid-connect/certs`

**Examples:**
- curl -X POST https://auth.your-app.test/introspect -d "token=xyz" -d "token_type_hint=access_token" -u api-client:secret | jq .
- curl -X POST http://localhost:8080/realms/myrealm/protocol/openid-connect/token/introspect -d "token=xyz" -u svc:svcsecret | jq '.active,.scope'

## References
- [RFC 7662 Token Introspection](https://datatracker.ietf.org/doc/html/rfc7662)
- [Keycloak Token Introspection](https://www.keycloak.org/docs/latest/securing_apps/)