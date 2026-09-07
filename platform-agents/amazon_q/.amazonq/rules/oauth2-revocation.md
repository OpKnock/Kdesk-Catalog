Revokes OAuth2 access and refresh tokens against RFC 7009 endpoints. Handles 200 responses for processed revocations and verifies revoked state by attempting token refresh.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -X POST https://auth.your-app.test/revoke -d "token=eyJ`
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

# OAuth2 Token Revocation

Revocation (RFC 7009) invalidates a token so it can no longer be used.

## What this skill does

- Revokes access and refresh tokens
- Handles 200 responses (even for unknown tokens)
- Verifies revocation by attempting refresh

## When to use

- Logout flows that must kill server-side sessions
- Suspending a compromised client's tokens

## Real commands

```bash
# Revoke access token
curl -X POST https://auth.your-app.test/revoke \
  -d "token=eyJhbGciOi..." -u client-id:client-secret

# Revoke refresh token (common for logout)
curl -X POST https://auth.your-app.test/revoke \
  -d "token=eyJhbGciOi..." -d "token_type_hint=refresh_token" -u client-id:client-secret

# Keycloak
curl -X POST http://localhost:8080/realms/myrealm/protocol/openid-connect/revoke \
  -d "token=xyz" -u svc:svcsecret

# Verify: refresh should now fail
curl -s -X POST http://localhost:8080/realms/myrealm/protocol/openid-connect/token \
  -d "grant_type=refresh_token" -d "refresh_token=xyz" -d "client_id=svc"
```

## Response semantics

- 200 means processed (even if token was invalid or already revoked)
- `token_type_hint` is a hint; servers may ignore it

## Best practices

- Always revoke the refresh token on logout
- Treat any non-2xx as a failure to retry
- Combine with introspection to confirm state

## Capabilities

### token-revocation
Revoke OAuth2 tokens against RFC 7009 endpoints and verify revoked state.

**Parameters:**
- `endpoint` (string): Revocation endpoint URL
- `token` (string): Token to revoke
- `token_type_hint` (string): access_token or refresh_token

**Commands:**
- `curl -X POST https://auth.your-app.test/revoke -d "token=eyJhbGciOi..." -u client-id:client-secret`
- `curl -X POST https://auth.your-app.test/revoke -d "token=eyJhbGciOi..." -d "token_type_hint=refresh_token" -u client-id:client-secret`
- `curl -X POST http://localhost:8080/realms/myrealm/protocol/openid-connect/revoke -d "token=xyz" -u svc:svcsecret`
- `curl -i -X POST https://auth.your-app.test/revoke -d "token=xyz" -u client:secret`
- `curl -s -X POST http://localhost:8080/realms/myrealm/protocol/openid-connect/token -d "grant_type=refresh_token" -d "refresh_token=xyz" -d "client_id=svc" | jq .`

**Examples:**
- curl -X POST https://auth.your-app.test/revoke -d "token=xyz" -d "token_type_hint=refresh_token" -u client:secret
- curl -i -X POST http://localhost:8080/realms/myrealm/protocol/openid-connect/revoke -d "token=xyz" -u svc:svcsecret
- curl -X POST https://auth.your-app.test/revoke -d "token=xyz" -u client:secret -w "%{http_code}\n"

## References
- [RFC 7009 Token Revocation](https://datatracker.ietf.org/doc/html/rfc7009)
- [Keycloak Revocation](https://www.keycloak.org/docs/latest/securing_apps/)