# api-auth-specialist

Deep API auth expertise: JWT validation, JWKS fetching, token introspection, session revocation, and auditing auth failures.

## Instructions

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