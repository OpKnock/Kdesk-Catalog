---
name: "api-sec-jwt-auditing"
description: "Hardens API authentication security: JWT inspection and validation, token lifecycle, algorithm confusion tests, and auth header verification with jwt-cli. Use when working with jwt auditing, auth header checks or when the user mentions jwt auditing, auth header checks."
---

Hardens API authentication security: JWT inspection and validation, token lifecycle, algorithm confusion tests, and auth header verification with jwt-cli.

## Agentic Workflow: Read -> Reason -> Act (api-sec-jwt-auditing)

You are **Api Sec JWT Auditing** (security) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — security context for `api-sec-jwt-auditing`
- Domain: Hardens API authentication security: JWT inspection and validation, token lifecycle, algorithm confusion tests, and auth header verification with jwt-cli.
- **jwt-auditing**: Inspect and validate JWTs — `npm install -g jwt-cli`
- **auth-header-checks**: Verify bearer and basic auth enforcement — `curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8080/me`
- Check `knowledge` and `prerequisites: node.js, python, owasp-zap`

### 2. Reason — think for `api-sec-jwt-auditing`
- For `jwt-auditing`: Inspect and validate JWTs — decide which checks to run
- For `auth-header-checks`: Verify bearer and basic auth enforcement — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-sec-jwt-auditing` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Jwt` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-sec-jwt-auditing:db342051`

# API Security v2 - Auth Tokens

JWT security hardening.

## What This Skill Does
- Inspects tokens for weak signatures
- Tests algorithm confusion vectors
- Verifies endpoint enforcement

## When to Use
- Auditing authentication implementation
- Testing token expiry handling
- Investigating auth bypasses

## Real Commands

```bash
npm install -g jwt-cli
jwt decode $TOKEN
jwt encode --secret "s3cret" --alg HS256 '{"sub":"1234567890"}'
curl -s -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer $TOKEN" https://api.example.com/me
```

## Checks to Run
- alg none: does the server accept unsigned tokens?
- Expired tokens: are they rejected with 401?
- Tampered payloads: does signature validation catch them?
- Weak secrets: crackable HS256 keys

## Testing
- Confirm 401 without a token
- Confirm 401 with an expired token
- Verify the server pins the expected algorithm

## Best Practices
- Reject alg:none explicitly
- Use RS256/ES256 for issuance
- Rotate signing keys on rotation schedules

## Capabilities

### jwt-auditing
Inspect and validate JWTs

**Parameters:**
- `token` (string): JWT to decode
- `secret` (string): HMAC signing secret
- `claims` (object): Claims object to encode

**Commands:**
- `npm install -g jwt-cli`
- `jwt decode $TOKEN`
- `jwt encode --secret "s3cret" --alg HS256 '{"sub":"1234567890","name":"alice"}'`
- `jwt encode --secret "s3cret" --alg none '{"sub":"admin"}'`
- `curl -s -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer $TOKEN" http://localhost:8080/me`

**Examples:**
- jwt decode $TOKEN prints header and payload
- jwt encode with alg none probes algorithm confusion
- curl with the token checks endpoint enforcement

### auth-header-checks
Verify bearer and basic auth enforcement

**Commands:**
- `curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8080/me`
- `curl -s -o /dev/null -w '%{http_code}\n' -H 'Authorization: Bearer expired-token' http://localhost:8080/me`
- `node -e "const jwt=require('jsonwebtoken'); const t=jwt.sign({sub:'1'},'secret',{expiresIn:'1h'}); console.log(t.split('.')[0]); console.log(jwt.verify(t,'secret').sub)"`

**Examples:**
- -cli --help
- -api --help

## References
- [jwt-cli GitHub](https://github.com/mike-engel/jwt-cli)
- [JWT.io Introduction](https://jwt.io/introduction)
