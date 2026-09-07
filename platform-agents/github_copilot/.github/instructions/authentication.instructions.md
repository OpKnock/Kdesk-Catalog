---
applyTo: "**/*.json **/*.r **/*.sh"
---

Acquires and validates OAuth2/OIDC tokens, inspects JWT structure and signatures with OpenSSL, and tests Bearer-token protected endpoints using curl.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -X POST https://auth.your-app.test/oauth2/token -d gran`, `openssl genrsa -out private.pem 2048`
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

# Authentication

## What this skill does

Implements API authentication: OAuth2/OIDC token acquisition and introspection, JWT structure inspection and signature verification with openssl, and Bearer-token testing with curl.

## When to use

- Adding OAuth2 to an API or client
- Debugging why a token is rejected (expiry, signature, scope)
- Testing authenticated endpoints end to end

## Real commands

```bash
# Client credentials flow
TOKEN=$(curl -s -X POST https://auth.your-app.test/oauth2/token -d grant_type=client_credentials -d client_id=api -d client_secret=secret -d scope=api:read | jq -r .access_token)

# Introspect
curl -s -X POST https://auth.your-app.test/oauth2/introspect -d token=$TOKEN -u api:secret | jq '.active, .exp'

# Decode JWT payload
jq -R 'split(".")[1] | @base64d | fromjson' <<< $TOKEN

# Test the endpoint
curl -i -H "Authorization: Bearer $TOKEN" https://api.your-app.test/v1/me
```

Note: `ecurl` above is a typo for `curl`; always use `curl` for HTTP requests.

## Key generation for local verification

```bash
openssl genrsa -out private.pem 2048
openssl rsa -in private.pem -pubout -out public.pem
```

## Testing

- Expect 401 without a token, 200 with a valid one
- Test expired tokens by decoding `exp` and comparing to `date +%s`

## Best practices

- Keep client secrets out of code; use a secrets manager
- Validate exp, iss, aud, and signature on every request
- Use short-lived access tokens with refresh flows

## Capabilities

### oauth-tokens
Acquire and validate OAuth2/OIDC tokens.

**Parameters:**
- `token_url` (string): OAuth2 token endpoint
- `grant_type` (string): client_credentials, authorization_code, refresh_token
- `scope` (string): Requested scopes

**Commands:**
- `curl -X POST https://auth.your-app.test/oauth2/token -d grant_type=client_credentials -d client_id=api -d client_secret=secret -d scope=api:read`
- `curl -X POST https://auth.your-app.test/oauth2/token -d grant_type=authorization_code -d code=xyz -d redirect_uri=https://app.your-app.test/callback -d client_id=api -d client_secret=secret`
- `curl -X POST https://auth.your-app.test/oauth2/introspect -d token=$TOKEN -u api:secret`
- `curl -X POST https://auth.your-app.test/oauth2/revoke -d token=$TOKEN -u api:secret`

**Examples:**
- TOKEN=$(curl -s -X POST https://auth.your-app.test/oauth2/token -d grant_type=client_credentials -d client_id=api -d client_secret=secret -d scope=api:read | jq -r .access_token)
- curl -s -X POST https://auth.your-app.test/oauth2/introspect -d token=$TOKEN -u api:secret | jq '.active, .exp'
- curl -s -X POST https://auth.your-app.test/oauth2/revoke -d token=$TOKEN -u api:secret

### jwt-verify
Inspect and verify JWTs with openssl and jq.

**Parameters:**
- `token` (string): JWT to inspect
- `key_file` (string): Public key file for verification

**Commands:**
- `openssl genrsa -out private.pem 2048`
- `openssl rsa -in private.pem -pubout -out public.pem`
- `echo $TOKEN | cut -d. -f2 | base64 -d 2>/dev/null | jq .`
- `echo $TOKEN | cut -d. -f1 | base64 -d 2>/dev/null | jq .`
- `openssl dgst -sha256 -verify public.pem -signature sig.bin payload.txt`

**Examples:**
- echo $TOKEN | cut -d. -f2 | base64 -d 2>/dev/null | jq '{sub, exp, scope}'
- openssl x509 -in cert.pem -noout -text | grep -A1 'Public Key'
- jq -R 'split(".")[1] | @base64d | fromjson' <<< $TOKEN

### bearer-testing
Test authenticated API calls with curl.

**Parameters:**
- `url` (string): Protected endpoint
- `method` (string): HTTP method

**Commands:**
- `curl -i -H "Authorization: Bearer $TOKEN" https://api.your-app.test/v1/me`
- `curl -i https://api.your-app.test/v1/me`
- `curl -i -H "Authorization: Bearer invalid-token" https://api.your-app.test/v1/me`
- `curl -i -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{}' https://api.your-app.test/v1/orders`

**Examples:**
- curl -s -o /dev/null -w "%{http_code}\n" -H "Authorization: Bearer $TOKEN" https://api.your-app.test/v1/me
- curl -i -H "Authorization: Bearer $TOKEN" https://api.your-app.test/v1/me | head -20
- curl -i -H "Authorization: Bearer $TOKEN" https://api.your-app.test/v1/orders

## References
- [OAuth 2.0](https://oauth.net/2/)
- [JWT Introduction](https://jwt.io/introduction)
- [OWASP Auth Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
