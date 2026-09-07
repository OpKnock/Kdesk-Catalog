---
name: "token-revocation"
description: "Invalidate OAuth2 tokens on demand by calling the revocation endpoint and maintaining JWT jti blacklists in Redis. Revokes both access and refresh tokens, extracts jti claims from JWTs for immediate rejection, and verifies revoked tokens return 401 \u2014 essential for compromised sessions, global logout, and emergency freezes. Use when working with token revoke, api or when the user mentions token revoke, api."
license: "MIT"
compatibility: "Requires redis-cli. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(redis-cli:*)"
---

Invalidate OAuth2 tokens on demand by calling the revocation endpoint and maintaining JWT jti blacklists in Redis. Revokes both access and refresh tokens, extracts jti claims from JWTs for immediate rejection, and verifies revoked tokens return 401 — essential for compromised sessions, global logout, and emergency freezes.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -X POST https://auth.your-app.test/revoke -d "token=$AC`
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
