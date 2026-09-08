---
trigger: glob
description: "Implement passwordless login with magic links: JWT signing, one-time token storage with Redis, email delivery, and verification endpoints. Use when working with token issuance, verify exchange, api or when the user mentions token issuance, verify exchange, api."
globs: ["**/*.go", "**/*.json", "**/*.py", "**/*.r", "**/*.sh"]
---

Implement passwordless login with magic links: JWT signing, one-time token storage with Redis, email delivery, and verification endpoints.

## Agentic Workflow: Read -> Reason -> Act (magic-link)

You are **Magic Link** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `magic-link`
- Domain: Implement passwordless login with magic links: JWT signing, one-time token storage with Redis, email delivery, and verification endpoints.
- **token-issuance**: Generate and sign short-lived magic link tokens. — `openssl rand -base64 32`
- **verify-exchange**: Exercise the magic link flow: request, verify, and one-time use. — `curl -s -X POST http://localhost:8080/auth/magic-link -H 'Content-Type: applicat`
- Check `knowledge` and `prerequisites: npx, openssl, python3, redis-cli`

### 2. Reason — think for `magic-link`
- For `token-issuance`: Generate and sign short-lived magic link tokens. — decide which checks to run
- For `verify-exchange`: Exercise the magic link flow: request, verify, and one-time use. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `magic-link` tools
- Tools: `Glob`, `Grep`, `Read`, `Openssl`, `Python3` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `magic-link:b1cbe02d`

# Magic Link Authentication

Implement passwordless login with signed, single-use magic links.

## What this skill does

- Issues short-lived signed tokens for emails.
- Stores one-time tokens in Redis with TTL.
- Verifies tokens on the callback endpoint.

## When to use

- Passwordless login flows.
- Lowering login friction while keeping security.
- Replacing emailed passwords with expiring links.

## Real commands

```bash
# Generate a random secret or keypair
openssl rand -base64 32
openssl genrsa -out private.pem 2048

# Issue an RS256 token (15 min TTL)
python3 -c "import jwt,datetime; print(jwt.encode({'sub':'alice@myapp.test','aud':'magic-link','exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=15)}, open('private.pem').read(), algorithm='RS256'))"

# Request a link (app endpoint)
curl -s -X POST http://localhost:8080/auth/magic-link \
  -H 'Content-Type: application/json' \
  -d '{"email":"alice@myapp.test"}'

# Store a one-time token in Redis (900s TTL)
redis-cli SETEX magic:alice@myapp.test 900 TOKEN

# Verify callback
curl -s http://localhost:8080/auth/verify?token=TOKEN

# Replay protection: second use must fail
curl -s http://localhost:8080/auth/verify?token=USED_TOKEN
```

## Flow example

```text
POST /auth/magic-link {email}  ->  generate token, email link
GET  /auth/verify?token=...    ->  validate signature+exp, consume token, issue session
```

## Testing

```bash
# Negative tests
curl -s http://localhost:8080/auth/verify?token=EXPIRED   # 401
curl -s http://localhost:8080/auth/verify?token=USED      # 401 (single use)
```

## Best practices

- Sign tokens (RS256 preferred) and enforce aud/iss claims.
- Make links single-use: consume the token after successful verification.
- Rate-limit the request endpoint; leaky magic links enable spam.
- Keep TTL short (10-15 min); reissue on expiry.

## Capabilities

### token-issuance
Generate and sign short-lived magic link tokens.

**Parameters:**
- `email` (string): User email for the token subject.
- `ttl_minutes` (integer): Token validity in minutes.
- `algorithm` (string): JWT algorithm: RS256 or HS256.

**Commands:**
- `openssl rand -base64 32`
- `python3 -c "import jwt,datetime; print(jwt.encode({'sub':'alice@myapp.test','aud':'magic-link','exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=15)}, open('private.pem').read(), algorithm='RS256'))"`
- `npx jwt-cli encode --secret=dev-secret -P sub=alice@myapp.test -P exp=... `
- `python3 -c "import secrets; print(secrets.token_urlsafe(32))"`

**Examples:**
- python3 -c "import jwt,datetime; print(jwt.encode({'sub':'alice@myapp.test','aud':'magic-link','exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=15)}, open('private.pem').read(), algorithm='RS256'))"
- openssl rand -base64 32
- python3 -c "import secrets; print(secrets.token_urlsafe(32))"

### verify-exchange
Exercise the magic link flow: request, verify, and one-time use.

**Parameters:**
- `email` (string): Email to send the link to.
- `token` (string): Magic link token.

**Commands:**
- `curl -s -X POST http://localhost:8080/auth/magic-link -H 'Content-Type: application/json' -d '{"email":"alice@myapp.test"}'`
- `curl -s http://localhost:8080/auth/verify?token=TOKEN`
- `redis-cli SETEX magic:alice@myapp.test 900 TOKEN`
- `redis-cli GET magic:alice@myapp.test`
- `curl -s http://localhost:8080/auth/verify?token=USED_TOKEN`

**Examples:**
- curl -s -X POST http://localhost:8080/auth/magic-link -H 'Content-Type: application/json' -d '{"email":"alice@myapp.test"}'
- curl -s http://localhost:8080/auth/verify?token=TOKEN
- redis-cli SETEX magic:alice@myapp.test 900 TOKEN

## References
- [JWT Best Practices](https://auth0.com/blog/implementing-magic-links/)
- [PyJWT](https://pyjwt.readthedocs.io/en/stable/)
- [redis SETEX](https://redis.io/docs/latest/commands/setex/)
