---
name: "api-auth-oidc"
description: "API auth with OpenID Connect - discovery, authorization code flow with PKCE, ID token validation, and userinfo retrieval. Use when working with oidc flow or when the user mentions oidc flow."
---

API auth with OpenID Connect - discovery, authorization code flow with PKCE, ID token validation, and userinfo retrieval.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -s http://localhost:8080/realms/demo/.well-known/openid`
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

# API Auth (OpenID Connect)

## What this skill does
Implement OpenID Connect on top of OAuth2: run discovery, drive the authorization code flow with PKCE, validate ID tokens, and call the userinfo endpoint.

## When to use
- Building SPAs that need identity (not just access)
- Federating login with an external IdP
- Moving from opaque sessions to OIDC

## Real commands
```bash
# Discovery
curl -s http://localhost:8080/realms/demo/.well-known/openid-configuration | jq '.authorization_endpoint, .userinfo_endpoint, .jwks_uri'

# Generate PKCE pair
node -e "const c=require('crypto');\
const v=c.randomBytes(32).toString('base64url');\
console.log('verifier:',v);\
console.log('challenge:',c.createHash('sha256').update(v).digest('base64url'))"

# Authorization request
curl -s 'http://localhost:8080/realms/demo/protocol/openid-connect/auth?client_id=spa&redirect_uri=http://localhost:3000/cb&response_type=code&scope=openid%20profile&code_challenge=CHALLENGE&code_challenge_method=S256' -o /dev/null -w '%{redirect_url}'

# Exchange code
curl -s -X POST http://localhost:8080/realms/demo/protocol/openid-connect/token \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=authorization_code&client_id=spa&code=$CODE&redirect_uri=http://localhost:3000/cb&code_verifier=VERIFIER' | jq -r '.id_token'

# Userinfo
curl -s http://localhost:8080/realms/demo/protocol/openid-connect/userinfo -H "Authorization: Bearer $ACCESS" | jq '.preferred_username'

# JWKS for ID token validation
curl -s http://localhost:8080/realms/demo/protocol/openid-connect/certs | jq '.keys | length'

# Logout
curl -s http://localhost:8080/realms/demo/protocol/openid-connect/logout?post_logout_redirect_uri=http://localhost:3000 -o /dev/null -w '%{http_code}'
```

## ID token validation
- Verify signature against the JWKS
- Check iss, aud, exp, nonce, azp if present
- Always use the code flow with PKCE for SPAs

## Best practices
- Never expose client secrets in SPAs (use PKCE)
- Validate the nonce to prevent replay
- Use `openid` scope so an ID token is returned

## Testing
```bash
curl -s http://localhost:8080/realms/demo/.well-known/openid-configuration | jq -e '.issuer' && echo OK
```

## Capabilities

### oidc-flow
Implement and test OpenID Connect flows

**Parameters:**
- `realm` (string): OIDC realm/tenant
- `scope` (string): Scopes, e.g. openid profile email
- `code_challenge` (string): PKCE S256 challenge

**Commands:**
- `curl -s http://localhost:8080/realms/demo/.well-known/openid-configuration | jq '.authorization_endpoint, .userinfo_endpoint'`
- `curl -s 'http://localhost:8080/realms/demo/protocol/openid-connect/auth?client_id=spa&redirect_uri=http://localhost:3000/cb&response_type=code&scope=openid%20profile&code_challenge=CHALLENGE&code_challenge_method=S256' -o /dev/null -w '%{redirect_url}'`
- `curl -s -X POST http://localhost:8080/realms/demo/protocol/openid-connect/token -H 'Content-Type: application/x-www-form-urlencoded' -d 'grant_type=authorization_code&client_id=spa&code=$CODE&redirect_uri=http://localhost:3000/cb&code_verifier=VERIFIER' | jq -r '.id_token'`
- `curl -s http://localhost:8080/realms/demo/protocol/openid-connect/userinfo -H "Authorization: Bearer $ACCESS" | jq '.preferred_username'`
- `curl -s http://localhost:8080/realms/demo/protocol/openid-connect/certs | jq '.keys | length'`

**Examples:**
- node -e "const c=require('crypto');const v=c.randomBytes(32).toString('base64url');console.log(v);console.log(c.createHash('sha256').update(v).digest('base64url'))"
- curl -s -X POST http://localhost:8080/realms/demo/protocol/openid-connect/token -d 'grant_type=authorization_code&client_id=spa&code=$CODE&redirect_uri=http://localhost:3000/cb&code_verifier=VERIFIER' | jq '.expires_in'
- curl -s http://localhost:8080/realms/demo/protocol/openid-connect/logout?post_logout_redirect_uri=http://localhost:3000 -o /dev/null -w '%{http_code}'

## References
- [OpenID Connect Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html)
- [OAuth 2.0 PKCE (RFC 7636)](https://datatracker.ietf.org/doc/html/rfc7636)
