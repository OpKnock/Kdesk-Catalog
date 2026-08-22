# Oauth2 Revocation

Revokes OAuth2 access and refresh tokens against RFC 7009 endpoints. Handles 200 responses for processed revocations and verifies revoked state by attempting token refresh.

## Instructions

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