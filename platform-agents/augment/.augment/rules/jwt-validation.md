---
type: agent_requested
description: "Decode, verify, and troubleshoot JWTs: inspect header/payload locally, validate signatures with openssl and PyJWT, and test bearer-auth APIs with curl."
---

# JWT Validation

Decode, verify, and troubleshoot JWTs: inspect header/payload locally, validate signatures with openssl and PyJWT, and test bearer-auth APIs with curl.

## Instructions

# JWT Validation

Inspect and verify JSON Web Tokens end to end.

## What this skill does

- Decodes JWT header and payload with jq, jwt-cli, or python.
- Verifies RS256/HS256/ES256 signatures with openssl and PyJWT.
- Tests bearer-token protected endpoints with curl.

## When to use

- Debugging 401/403 responses on API gateways.
- Verifying token expiry, issuer, and audience claims.
- Writing CI checks that a dev/QA token is still valid.

## Real commands

```bash
# Decode payload (add base64 padding if needed)
echo $JWT | cut -d. -f2 | base64 -d 2>/dev/null | jq .

# Decode header
echo $JWT | cut -d. -f1 | base64 -d 2>/dev/null | jq .

# Full decode with npx jwt-cli
npx jwt-cli decode $JWT

# Signature verification with openssl (RS256)
HEADER=$(echo $JWT | cut -d. -f1)
PAYLOAD=$(echo $JWT | cut -d. -f2)
echo -n "$HEADER.$PAYLOAD" | openssl dgst -sha256 -verify public.pem -signature sig.bin

# Python verification with PyJWT
python3 -c "import jwt; print(jwt.decode('$JWT', open('public.pem').read(), algorithms=['RS256'], audience='api'))"

# Smoke test the protected endpoint
curl -s -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer $JWT" http://localhost:8080/api/me
```

## Configuration example

```bash
export JWT_SECRET_B64=...            # HS256 shared secret
openssl genrsa -out private.pem 2048 # RS256 keypair
openssl rsa -in private.pem -pubout -out public.pem
```

## Testing

```bash
# Expired token should fail with a clear error
python3 -c "import jwt,time; print(jwt.decode('$JWT', open('public.pem').read(), algorithms=['RS256']))"

# Wrong key should raise InvalidSignatureError
python3 -c "import jwt; jwt.decode('$JWT', 'wrong-secret', algorithms=['HS256'])"
```

## Best practices

- Always verify exp, iss, and aud; never trust decoded payloads alone.
- Prefer RS256/ES256 for server-to-server; HS256 only with strong shared secrets.
- Keep token lifetimes short and use jti for revocation checks.

## Capabilities

### decode-inspect
Decode JWT header and payload locally without any library.

**Commands:**
- `echo $JWT | cut -d. -f2 | base64 -d 2>/dev/null | jq .`
- `echo $JWT | cut -d. -f1 | base64 -d 2>/dev/null | jq .`
- `npx jwt-cli decode $JWT`
- `echo "$JWT" | cut -d. -f2 | base64 -d 2>/dev/null | jq -r '.exp'`

**Examples:**
- echo $JWT | cut -d. -f2 | base64 -d | jq .
- npx jwt-cli decode $JWT
- jq -r '.sub' <<< "$(echo $JWT | cut -d. -f2 | base64 -d)"

### verify-signature
Verify JWT signatures with openssl, PyJWT, and curl against a real auth endpoint.

**Commands:**
- `echo -n "$HEADER.$PAYLOAD" | openssl dgst -sha256 -verify public.pem -signature sig.bin`
- `python3 -c "import jwt; print(jwt.decode('$JWT', open('public.pem').read(), algorithms=['RS256']))"`
- `curl -s -H "Authorization: Bearer $JWT" http://localhost:8080/api/me`
- `curl -s -i -H "Authorization: Bearer $JWT" http://localhost:8080/api/me | head -5`

**Examples:**
- python3 -c "import jwt; print(jwt.decode('$JWT', open('public.pem').read(), algorithms=['RS256']))"
- curl -s -H "Authorization: Bearer $JWT" http://localhost:8080/api/me
- echo -n "$HEADER.$PAYLOAD" | openssl dgst -sha256 -verify public.pem -signature sig.bin