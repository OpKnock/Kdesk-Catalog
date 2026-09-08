---
trigger: glob
description: "API auth with JWT-based authentication - issue tokens with jsonwebtoken, validate signatures and claims, and enforce expiry and audience. Use when issuing or validating JWTs for API access. Don't use for API-key auth (see api-auth-keys) or mutual-TLS auth (see api-auth-mtls)."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
---

API auth with JWT-based authentication - issue tokens with jsonwebtoken, validate signatures and claims, and enforce expiry and audience. Use when issuing or validating JWTs for API access. Don't use for API-key auth (see api-auth-keys) or mutual-TLS auth (see api-auth-mtls).

## Agentic Workflow: Read -> Reason -> Act (api-auth-jwt)

You are **Api Auth JWT** (security) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — security context for `api-auth-jwt`
- Domain: API auth with JWT-based authentication - issue tokens with jsonwebtoken, validate signatures and claims, and enforce expiry and audience. Use when issuing or validating JWTs for API access. Don't use 
- **jwt-auth**: Issue and validate JWT tokens for API access — `npm install jsonwebtoken`
- Check `knowledge` and `prerequisites: node.js, python, jsonwebtoken`

### 2. Reason — think for `api-auth-jwt`
- For `jwt-auth`: Issue and validate JWT tokens for API access — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-auth-jwt` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-auth-jwt:a5081012`

# API Auth (JWT)

## What this skill does
Issue and validate JWTs for API authentication with the jsonwebtoken library. Covers signing, verification with audience/issuer enforcement, decoding for debugging, and expiry handling.

## When to use
- Replacing opaque session tokens with JWTs
- Adding stateless auth to an API
- Debugging token expiry issues

## Real commands
```bash
# Install
npm install jsonwebtoken

# Sign a token (1h, audience=api)
node -e "const jwt=require('jsonwebtoken');\
const t=jwt.sign({sub:'user-1',role:'admin'},process.env.SECRET,\
{expiresIn:'1h',audience:'api',issuer:'auth-api'});console.log(t)"

# Verify (fails on bad signature, wrong audience, or expiry)
node -e "const jwt=require('jsonwebtoken');\
const t=process.argv[1];\
try{jwt.verify(t,process.env.SECRET,{audience:'api'});console.log('valid')}\ncatch(e){console.error(e.message)}" $TOKEN

# Decode without verifying (debugging only)
node -e "const jwt=require('jsonwebtoken');console.log(jwt.decode(process.argv[1]))" $TOKEN

# Shell decode
echo $TOKEN | cut -d. -f2 | base64 -d | jq '.exp, .scope'

# Use the token
curl -s http://localhost:8080/api/users -H "Authorization: Bearer $TOKEN" | jq '.user'
```

## Best practices
- Prefer RS256 with a JWKS; use HS256 only for single-service setups
- Always verify signature AND audience AND issuer
- Keep tokens short-lived (15m-1h); refresh via refresh token
- Never log tokens or put secrets in claims

## Testing
```bash
BAD=invalid.token.here
curl -s http://localhost:8080/api/users -H "Authorization: Bearer $BAD" -o /dev/null -w '%{http_code}\n'
# Expect 401
```

## Capabilities

### jwt-auth
Issue and validate JWT tokens for API access

**Parameters:**
- `secret` (string): HMAC secret for signing
- `expiresIn` (string): Token lifetime, e.g. 1h, 15m, 7d
- `audience` (string): Expected audience claim

**Commands:**
- `npm install jsonwebtoken`
- `node -e "const jwt=require('jsonwebtoken');const t=jwt.sign({sub:'user-1',role:'admin'},process.env.SECRET,{expiresIn:'1h',audience:'api',issuer:'auth-api'});console.log(t)"`
- `node -e "const jwt=require('jsonwebtoken');const t=process.argv[1];try{jwt.verify(t,process.env.SECRET,{audience:'api'});console.log('valid')}catch(e){console.error(e.message)}" $TOKEN`
- `node -e "const jwt=require('jsonwebtoken');console.log(jwt.decode(process.argv[1]))" $TOKEN`
- `curl -s http://localhost:8080/api/users -H "Authorization: Bearer $TOKEN" | jq '.user'`

**Examples:**
- node -e "const jwt=require('jsonwebtoken');console.log(jwt.sign({scope:['read:orders']},process.env.SECRET,{expiresIn:'5m',audience:'api'}))"
- echo $TOKEN | cut -d. -f2 | base64 -d | jq '.exp, .scope'
- curl -s http://localhost:8080/api/users -H 'Authorization: Bearer invalid.token.here' -o /dev/null -w '%{http_code}'

## References
- [jwt.io Introduction](https://jwt.io/introduction)
- [jsonwebtoken npm](https://www.npmjs.com/package/jsonwebtoken)
