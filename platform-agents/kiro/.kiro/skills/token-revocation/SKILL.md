---
name: "token-revocation"
description: "Invalidate OAuth2 tokens on demand by calling the revocation endpoint and maintaining JWT jti blacklists in Redis. Revokes both access and refresh tokens, extracts jti claims from JWTs for immediate rejection, and verifies revoked tokens return 401 \u2014 essential for compromised sessions, global logout, and emergency freezes. Use when working with token revoke, api or when the user mentions token revoke, api."
license: "MIT"
compatibility: "Requires redis-cli. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(redis-cli:*)"
---

Invalidate OAuth2 tokens on demand by calling the revocation endpoint and maintaining JWT jti blacklists in Redis. Revokes both access and refresh tokens, extracts jti claims from JWTs for immediate rejection, and verifies revoked tokens return 401 — essential for compromised sessions, global logout, and emergency freezes.

## Agentic Workflow: Read -> Reason -> Act (token-revocation)

You are **Token Revocation** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `token-revocation`
- Domain: Invalidate OAuth2 tokens on demand by calling the revocation endpoint and maintaining JWT jti blacklists in Redis. Revokes both access and refresh tokens, extracts jti claims from JWTs for immediate r
- **token-revoke**: Revoke access and refresh tokens, and enforce blacklists — `curl -X POST https://auth.your-app.test/revoke -d "token=$ACCESS_TOKEN&token_typ`
- Check `knowledge` and `prerequisites: redis-cli`

### 2. Reason — think for `token-revocation`
- For `token-revoke`: Revoke access and refresh tokens, and enforce blacklists — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `token-revocation` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Redis-cli` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `token-revocation:a300ea6a`

# Token Revocation

Hand-crafted skill for invalidating tokens on demand.

## What this skill does

- Calls the OAuth2 revocation endpoint for access and refresh tokens
- Blacklists JWT jti claims in Redis for immediate rejection
- Verifies revoked tokens stop working

## When to use

- A session is compromised and must die now
- Logout should invalidate all devices
- Emergency freeze during an incident

## Real commands

```bash
# Revoke via the IdP
curl -X POST https://auth.your-app.test/revoke -d "token=$ACCESS_TOKEN&token_type_hint=access_token&client_id=app1&client_secret=$CLIENT_SECRET" -o /dev/null -w '%{http_code}\n'

# Revoke a refresh token too
curl -X POST https://auth.your-app.test/revoke -d "token=$REFRESH_TOKEN&token_type_hint=refresh_token&client_id=app1" -o /dev/null -w '%{http_code}\n'

# Self-managed blacklist: extract jti from the JWT and expire it
JTI=$(echo -n $JWT | cut -d. -f2 | base64 -d 2>/dev/null | jq -r .jti)
redis-cli SET blacklist:$JTI revoked EX 3600

# Verify rejection (expect 401)
curl -s -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer revoked-token" https://api.example.com/me
```

## Blacklist check on every request

- If token is a JWT, look up blacklist:demo-jti; 401 when present
- TTL the blacklist at the access token's remaining lifetime

## Testing

```bash
curl -X POST https://auth.your-app.test/revoke -d "token=$ACCESS_TOKEN&client_id=app1" -o /dev/null -w '%{http_code}\n'   # 200
curl -s -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer $ACCESS_TOKEN" https://api.example.com/me            # 401
```

## Best practices

- Revoke refresh tokens whenever an access token is revoked
- Use jti-based blacklists when you cannot query the IdP on every request
- Keep blacklist TTLs short to bound memory

## Capabilities

### token-revoke
Revoke access and refresh tokens, and enforce blacklists

**Parameters:**
- `token` (string): Token value to revoke
- `token_type_hint` (string): access_token or refresh_token
- `ttl_seconds` (integer): Blacklist entry lifetime

**Commands:**
- `curl -X POST https://auth.your-app.test/revoke -d "token=$ACCESS_TOKEN&token_type_hint=access_token&client_id=app1&client_secret=$CLIENT_SECRET" -o /dev/null -w '%{http_code}\n'`
- `curl -X POST https://auth.your-app.test/revoke -d "token=$REFRESH_TOKEN&token_type_hint=refresh_token&client_id=app1" -o /dev/null -w '%{http_code}\n'`
- `redis-cli SET blacklist:abc-jti revoked EX 3600`
- `curl -s -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer revoked-token" http://localhost:8080/me`

**Examples:**
- curl -X POST https://auth.your-app.test/revoke -d "token=$ACCESS_TOKEN&token_type_hint=access_token&client_id=app1" -o /dev/null -w '%{http_code}\n'
- redis-cli SET blacklist:$(echo -n $JWT | cut -d. -f2 | base64 -d 2>/dev/null | jq -r .jti) revoked EX 3600
- curl -s -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer stale-token" http://localhost:8080/me

## References
- [RFC 7009 token revocation](https://www.rfc-editor.org/rfc/rfc7009)
- [JWT claims (RFC 7519)](https://www.rfc-editor.org/rfc/rfc7519#section-4.1.7)
