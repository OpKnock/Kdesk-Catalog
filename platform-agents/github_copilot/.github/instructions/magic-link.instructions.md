---
applyTo: "**/*.go **/*.json **/*.py **/*.r **/*.sh"
---

# Magic Link

Implement passwordless login with magic links: JWT signing, one-time token storage with Redis, email delivery, and verification endpoints.

## Instructions

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
