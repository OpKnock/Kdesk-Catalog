---
applyTo: "**/*.json **/*.r **/*.sh"
---

Implements OpenID Connect flows: discovers issuer metadata and JWKS, exchanges authorization codes to obtain tokens, validates ID token signatures, and fetches userinfo claims.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -s https://auth.your-app.test/.well-known/openid-config`
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
