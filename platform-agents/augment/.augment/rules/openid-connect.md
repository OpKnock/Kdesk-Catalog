---
type: agent_requested
description: "Implements OpenID Connect flows: discovers issuer metadata and JWKS, exchanges authorization codes to obtain tokens, validates ID token signatures, and fetches userinfo claims. Use when working with oidc flows, api or when the user mentions oidc flows, api."
---

Implements OpenID Connect flows: discovers issuer metadata and JWKS, exchanges authorization codes to obtain tokens, validates ID token signatures, and fetches userinfo claims.

## Agentic Workflow: Read -> Reason -> Act (openid-connect)

You are **Openid Connect** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `openid-connect`
- Domain: Implements OpenID Connect flows: discovers issuer metadata and JWKS, exchanges authorization codes to obtain tokens, validates ID token signatures, and fetches userinfo claims.
- **oidc-flows**: Discover OIDC metadata, exchange codes for tokens, validate JWTs against JWKS and call userinfo. — `curl -s https://auth.your-app.test/.well-known/openid-configuration | jq .`
- Check `knowledge` references before acting

### 2. Reason — think for `openid-connect`
- For `oidc-flows`: Discover OIDC metadata, exchange codes for tokens, validate JWTs against JWKS and call userinfo. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `openid-connect` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `openid-connect:42198cab`

# OpenID Connect

OIDC builds on OAuth2 by adding an ID token with verified identity claims.

## What this skill does

- Discovers issuer metadata and JWKS
- Runs the authorization code flow
- Validates ID tokens and fetches userinfo

## When to use

- SSO for web apps (Keycloak, Okta, Auth0)
- Verifying JWTs with a public key

## Real commands

```bash
# Discovery
curl -s https://auth.your-app.test/.well-known/openid-configuration | jq .
curl -s https://auth.your-app.test/.well-known/jwks.json | jq '.keys[].alg'

# Token exchange (authorization code flow)
curl -X POST https://auth.your-app.test/realms/realm/protocol/openid-connect/token \
  -d "grant_type=authorization_code" \
  -d "code=AUTH_CODE" \
  -d "redirect_uri=https://app.your-app.test/callback" \
  -d "client_id=app" -d "client_secret=secret"

# Service-to-service
curl -X POST https://auth.your-app.test/realms/realm/protocol/openid-connect/token \
  -d "grant_type=client_credentials" -d "client_id=svc" -d "client_secret=secret"

# Userinfo
curl -s https://auth.your-app.test/realms/realm/protocol/openid-connect/userinfo \
  -H "Authorization: Bearer ACCESS_TOKEN"
```

## ID token validation

- Verify signature with JWKS keys (`kid` match)
- Check `iss`, `aud`, `exp`, `nonce`

## Best practices

- Always validate the signature, not just decode
- Use PKCE for public clients
- Cache JWKS and discovery metadata

## Capabilities

### oidc-flows
Discover OIDC metadata, exchange codes for tokens, validate JWTs against JWKS and call userinfo.

**Parameters:**
- `issuer` (string): OIDC issuer URL
- `client_id` (string): Client identifier
- `grant_type` (string): authorization_code, client_credentials or refresh_token

**Commands:**
- `curl -s https://auth.your-app.test/.well-known/openid-configuration | jq .`
- `curl -s https://auth.your-app.test/.well-known/jwks.json | jq '.keys[].alg'`
- `curl -X POST https://auth.your-app.test/realms/realm/protocol/openid-connect/token -d "grant_type=authorization_code" -d "code=AUTH_CODE" -d "redirect_uri=https://app.your-app.test/callback" -d "client_id=app" -d "client_secret=secret"`
- `curl -s https://auth.your-app.test/realms/realm/protocol/openid-connect/userinfo -H "Authorization: Bearer ACCESS_TOKEN"`
- `curl -s https://auth.your-app.test/realms/realm/protocol/openid-connect/token -d "grant_type=client_credentials" -d "client_id=svc" -d "client_secret=secret"`

**Examples:**
- curl -s https://auth.your-app.test/.well-known/openid-configuration | jq '.issuer,.authorization_endpoint'
- curl -s https://auth.your-app.test/realms/realm/protocol/openid-connect/userinfo -H "Authorization: Bearer $TOKEN" | jq .
- curl -X POST https://auth.your-app.test/realms/realm/protocol/openid-connect/token -d "grant_type=authorization_code" -d "code=$CODE" -d "redirect_uri=..." -d "client_id=app"

## References
- [OpenID Connect Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html)
- [OIDC Discovery 1.0](https://openid.net/specs/openid-connect-discovery-1_0.html)