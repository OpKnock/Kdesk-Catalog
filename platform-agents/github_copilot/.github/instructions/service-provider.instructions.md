---
applyTo: "**/*.json **/*.r **/*.sh"
---

Implements the relying party side of OpenID Connect: performs dynamic endpoint discovery, trades authorization codes for access tokens at the token endpoint, retrieves identity claims from userinfo, and verifies ID token signatures using published JWKS.

## Agentic Workflow: Read -> Reason -> Act (service-provider)

You are **Service Provider** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `service-provider`
- Domain: Implements the relying party side of OpenID Connect: performs dynamic endpoint discovery, trades authorization codes for access tokens at the token endpoint, retrieves identity claims from userinfo, a
- **oidc-sp-integration**: Executes the complete OIDC relying party flow from discovery through token validation — `curl -s https://auth.example.org/.well-known/openid-configuration | jq -r '.auth`
- Check `knowledge` references before acting

### 2. Reason — think for `service-provider`
- For `oidc-sp-integration`: Executes the complete OIDC relying party flow from discovery through token validation — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `service-provider` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `service-provider:8847583f`

# OIDC Service Provider

Implements the relying party side of OpenID Connect.

## What this skill does

- Discovers IdP endpoints from the well-known configuration
- Exchanges authorization codes for tokens
- Fetches userinfo and validates signatures with JWKS

## When to use

- Wiring a new app into corporate SSO as the RP side
- Debugging token endpoint failures
- Verifying user claims after login

## Real commands

```bash
# Discovery: find all endpoints dynamically
curl -s https://auth.example.org/.well-known/openid-configuration | jq -r '.authorization_endpoint,.token_endpoint,.jwks_uri'

# Exchange the authorization code
curl -s -X POST https://auth.example.org/token -d "grant_type=authorization_code&code=$CODE&redirect_uri=https://app.example.org/callback&client_id=app1&client_secret=$CLIENT_SECRET" | jq -r .access_token

# Read the user's claims
curl -s -H "Authorization: Bearer $TOKEN" https://auth.example.org/userinfo | jq

# Inspect signing keys
curl -s https://auth.example.org/.well-known/jwks.json | jq -r '.keys[].kid'
```

## RP checklist

- Redirect to the authorization_endpoint with scope=openid profile email
- Validate the id_token signature against JWKS and the issuer claim
- Use userinfo only for non-critical profile data

## Testing

```bash
curl -s https://auth.example.org/.well-known/openid-configuration | jq -r '.token_endpoint'
curl -s -H "Authorization: Bearer $TOKEN" https://auth.example.org/userinfo | jq '.email'
```

## Best practices

- Never hardcode endpoints; resolve them from discovery
- Store client_secret server-side only
- Cache JWKS and refresh on kid changes

## Capabilities

### oidc-sp-integration
Executes the complete OIDC relying party flow from discovery through token validation

**Parameters:**
- `issuer` (string): IdP issuer URL for discovery
- `client_id` (string): Registered RP client ID
- `redirect_uri` (string): Callback URL registered with the IdP

**Commands:**
- `curl -s https://auth.example.org/.well-known/openid-configuration | jq -r '.authorization_endpoint,.token_endpoint,.jwks_uri'`
- `curl -s -X POST https://auth.example.org/token -d "grant_type=authorization_code&code=$CODE&redirect_uri=https://app.example.org/callback&client_id=app1&client_secret=$CLIENT_SECRET" | jq -r .access_token`
- `curl -s -H "Authorization: Bearer $TOKEN" https://auth.example.org/userinfo | jq`
- `curl -s https://auth.example.org/.well-known/jwks.json | jq -r '.keys[].kid'`

**Examples:**
- curl -s https://auth.example.org/.well-known/openid-configuration | jq -r '.authorization_endpoint'
- curl -s -H "Authorization: Bearer $TOKEN" https://auth.example.org/userinfo | jq
- curl -s https://auth.example.org/.well-known/jwks.json | jq -r '.keys[].alg'

## References
- [OIDC Core Specification](https://openid.net/specs/openid-connect-core-1_0.html)
- [OIDC Discovery Specification](https://openid.net/specs/openid-connect-discovery-1_0.html)
- [OAuth 2.0 Token Revocation](https://www.rfc-editor.org/rfc/rfc7009.html)
