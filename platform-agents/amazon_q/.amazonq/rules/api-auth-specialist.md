Deep API auth expertise: JWT validation, JWKS fetching, token introspection, session revocation, and auditing auth failures.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -s http://localhost:8080/.well-known/jwks.json | jq '.k`
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