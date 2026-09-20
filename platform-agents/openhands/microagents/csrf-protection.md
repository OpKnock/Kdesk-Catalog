---
name: "csrf-protection"
description: "Prevents cross-site request forgery on state-changing endpoints via double-submit cookie patterns, SameSite cookies, and curl-based validation."
type: knowledge
triggers: ["csrf-protection", "csrf-tokens", "csrf-middleware"]
---

# Csrf Protection

Prevents cross-site request forgery on state-changing endpoints via double-submit cookie patterns, SameSite cookies, and curl-based validation.

## Instructions

# CSRF Protection

Prevent cross-site request forgery on state-changing endpoints.

## When to Use

- Cookie-based authentication on web APIs
- Any mutating endpoint reachable from a browser
- Defense-in-depth alongside SameSite cookies

## Strategy

Double-submit cookie: server sets a CSRF cookie, client echoes it in a header, server compares both. SameSite=strict/lax cookies block most CSRF automatically.

## Express with csrf-csrf

```bash
npm install csrf-csrf
```

```js
const { doubleCsrf } = require('csrf-csrf');
const { invalidCsrfTokenError, generateToken, validateRequest } = doubleCsrf({
  getSecret: () => process.env.CSRF_SECRET,
  cookieName: 'csrf-token',
  cookieOptions: { sameSite: 'lax', secure: true, httpOnly: true },
});

app.get('/csrf-token', (req, res) => {
  res.json({ csrfToken: generateToken(res, req) });
});

app.post('/transfer', validateRequest, (req, res) => {
  // state change only runs with a valid token
});
```

## Test with curl

```bash
curl -c cookies.txt -X GET http://localhost:8080/csrf-token
TOKEN=$(grep csrf-token cookies.txt | awk '{print $NF}')
curl -b cookies.txt -c cookies.txt -X POST \
  -H "X-CSRF-Token: $TOKEN" \
  -d '{"amount":10}' http://localhost:8080/transfer

# Without the token this must fail
curl -s -b cookies.txt -X POST http://localhost:8080/transfer -o /dev/null -w "%{http_code}\n"
```

## Verify Cookies

```bash
curl -s -D - -o /dev/null -X GET http://localhost:8080/health | grep -i 'set-cookie\|samesite'
```

## Testing

```bash
# Tokenless POST must be rejected (403/419)
curl -s -b cookies.txt -X POST http://localhost:8080/transfer -o /dev/null -w "%{http_code}\ n"
# Valid token must pass
curl -b cookies.txt -c cookies.txt -X POST -H "X-CSRF-Token: $TOKEN" http://localhost:8080/transfer -o /dev/null -w "%{http_code}\n"
```

## Best Practices

- Use double-submit or synchronizer token patterns
- Rotate tokens on login and logout
- Set SameSite=strict or lax
- Use secure + httpOnly cookies
- Never accept tokens from query strings
- Combine with origin checks (Sec-Fetch-Site)
- Test the tokenless request fails every time

## Capabilities

### csrf-tokens
Issue CSRF tokens and verify double-submit cookie patterns with curl

**Commands:**
- `curl -c cookies.txt -X GET http://localhost:8080/csrf-token`
- `curl -b cookies.txt -c cookies.txt -X POST -H "X-CSRF-Token: $TOKEN" http://localhost:8080/submit`
- `curl -b cookies.txt -c cookies.txt -X POST -H "Content-Type: application/json" -H "X-CSRF-Token: $TOKEN" -d '{"amount":10}' http://localhost:8080/transfer`
- `curl -s -b cookies.txt -X POST http://localhost:8080/transfer -o /dev/null -w "%{http_code}\n"`

**Examples:**
- curl -c cookies.txt -X GET http://localhost:8080/csrf-token && TOKEN=$(grep csrf cookies.txt | awk '{print $NF}') && curl -b cookies.txt -X POST -H "X-CSRF-Token: $TOKEN" http://localhost:8080/submit
- curl -s -b cookies.txt -X POST http://localhost:8080/transfer -o /dev/null -w "%{http_code}\n"
- curl -c cookies.txt -X GET http://localhost:8080/csrf-token | jq '.csrfToken'

### csrf-middleware
Configure CSRF protection middleware and SameSite cookies

**Commands:**
- `npm install csrf-csrf`
- `node server.js`
- `curl -s -D - -o /dev/null -X GET http://localhost:8080/health | grep -i set-cookie`
- `curl -s -D - -o /dev/null -X GET http://localhost:8080/health | grep -i 'samesite'`

**Examples:**
- npm install csrf-csrf && node server.js
- curl -s -D - -o /dev/null -X GET http://localhost:8080/health | grep -i set-cookie
- curl -s -D - -o /dev/null -X GET http://localhost:8080/health | grep -i samesite
