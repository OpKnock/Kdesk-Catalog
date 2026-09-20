---
name: "api-auth-specialist"
description: "Deep API auth expertise: JWT validation, JWKS fetching, token introspection, session revocation, and auditing auth failures. Use when working with auth deep or when the user mentions auth deep."
type: knowledge
triggers: ["api-auth-specialist", "auth-deep"]
---

Deep API auth expertise: JWT validation, JWKS fetching, token introspection, session revocation, and auditing auth failures.

## Agentic Workflow: Read -> Reason -> Act (api-auth-specialist)

You are **api-auth-specialist** (security) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — security context for `api-auth-specialist`
- Domain: Deep API auth expertise: JWT validation, JWKS fetching, token introspection, session revocation, and auditing auth failures.
- **auth-deep**: Validate tokens, introspect, and audit auth flows — `curl -s http://localhost:8080/.well-known/jwks.json | jq '.keys[0] | {kid, kty}'`
- Check `knowledge` and `prerequisites: node.js, python, jsonwebtoken`

### 2. Reason — think for `api-auth-specialist`
- For `auth-deep`: Validate tokens, introspect, and audit auth flows — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-auth-specialist` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-auth-specialist:5f5688b2`

# API Auth Specialist

## What this skill does
Expert-level authentication: validate JWTs against JWKS, introspect opaque tokens, decode and check claims, revoke sessions, and audit failed logins.

## When to use
- Debugging rejected tokens
- Enforcing revocation policies
- Auditing authentication security

## Real commands
```bash
# Fetch the JWKS
curl -s http://localhost:8080/.well-known/jwks.json | jq '.keys[0] | {kid, kty}'

# Decode JWT payload (no signature check!)
node -e "const t=process.argv[1];console.log(JSON.parse(Buffer.from(t.split('.')[1],'base64url')))" $TOKEN

# Introspect an opaque token
curl -s -X POST http://localhost:8080/oauth/introspect \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'token=$TOKEN' | jq '.active'

# Revoke a token
curl -s -X POST http://localhost:8080/oauth/revoke -d 'token=$TOKEN' | jq '.revoked'

# Audit logins
curl -s 'http://localhost:8080/api/auth/audit?action=login' | jq '.events[-1] | {user, ip, result}'

# Count failed logins
curl -s 'http://localhost:8080/api/auth/audit?result=failed' | jq '.events | length'
```

## JWT validation checklist
- Verify signature with the JWKS key matching `kid`
- Check `exp` (with leeway), `nbf`, `iat`
- Validate `iss` and `aud`
- Check scope/role claims against the route

## Best practices
- Cache JWKS and refresh on unknown `kid`
- Use opaque tokens + introspection for instant revocation
- Log failures with reason codes but never the token
- Rate-limit auth endpoints against brute force

## Testing
```bash
TOKEN=$(curl -s -X POST http://localhost:8080/oauth/token -d 'grant_type=password&username=a&password=b' | jq -r '.access_token')
curl -s -X POST http://localhost:8080/oauth/introspect -d "token=$TOKEN" | jq '.active'
```

## Capabilities

### auth-deep
Validate tokens, introspect, and audit auth flows

**Parameters:**
- `token` (string): Access or refresh token to inspect
- `audience` (string): Expected audience for validation
- `issuer` (string): Expected token issuer

**Commands:**
- `curl -s http://localhost:8080/.well-known/jwks.json | jq '.keys[0] | {kid, kty}'`
- `curl -s -X POST http://localhost:8080/oauth/introspect -H 'Content-Type: application/x-www-form-urlencoded' -d 'token=$TOKEN' | jq '.active'`
- `node -e "const t=process.argv[1];console.log(JSON.parse(Buffer.from(t.split('.')[1],'base64url')))" $TOKEN`
- `curl -s http://localhost:8080/api/auth/audit?action=login | jq '.events[-1] | {user, ip, result}'`
- `curl -s -X POST http://localhost:8080/oauth/revoke -H 'Content-Type: application/x-www-form-urlencoded' -d 'token=$TOKEN' | jq '.revoked'`

**Examples:**
- curl -s 'http://localhost:8080/oauth/introspect?token=$TOKEN' | jq '.exp'
- echo $TOKEN | cut -d. -f2 | base64 -d 2>/dev/null | jq '.exp, .scope'
- curl -s http://localhost:8080/api/auth/audit?result=failed | jq '.events | length'

## References
- [JWT RFC 7519](https://datatracker.ietf.org/doc/html/rfc7519)
- [Token Introspection RFC 7662](https://datatracker.ietf.org/doc/html/rfc7662)
