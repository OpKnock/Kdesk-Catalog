---
name: "cors-preflight"
description: "Handle and debug CORS preflight OPTIONS requests: correct status codes, Access-Control-Allow headers, and caching."
type: knowledge
triggers: ["cors-preflight", "preflight-debug", "preflight-config"]
---

# Cors Preflight

Handle and debug CORS preflight OPTIONS requests: correct status codes, Access-Control-Allow headers, and caching.

## Instructions

# CORS Preflight

Handle and debug preflight OPTIONS requests correctly.

## When to Use

- Browser requests fail with CORS errors on non-simple methods or custom headers
- Verifying the OPTIONS route returns 200 or 204 with the right headers
- Optimizing preflight cost with Access-Control-Max-Age

## When a Preflight Happens

Browsers preflight when the request is not simple: PUT/DELETE/PATCH methods, custom headers, or Content-Type other than text/plain, multipart/form-data, or application/x-www-form-urlencoded.

## Debug with curl

```bash
curl -i -X OPTIONS http://localhost:8080/api \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: PUT" \
  -H "Access-Control-Request-Headers: X-Custom-Header,Content-Type"

curl -s -o /dev/null -w "preflight status: %{http_code}\n" \
  -X OPTIONS http://localhost:8080/api \
  -H "Origin: http://localhost:3000" -H "Access-Control-Request-Method: POST"
```

A correct preflight response:

```
HTTP/1.1 204 No Content
Access-Control-Allow-Origin: http://localhost:3000
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization, X-Custom-Header
Access-Control-Max-Age: 86400
Vary: Origin
```

## Express Middleware

```js
const cors = require('cors');
app.use(cors({
  origin: ['http://localhost:3000'],
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization', 'X-Custom-Header'],
  maxAge: 86400
}));
```

## Testing

```bash
curl -s -D - -o /dev/null -X OPTIONS http://localhost:8080/api \
  -H "Origin: http://localhost:3000" -H "Access-Control-Request-Method: DELETE" | grep -i access-control
curl -s -D - -o /dev/null -X OPTIONS http://localhost:8080/api \
  -H "Origin: http://evil.com" -H "Access-Control-Request-Method: POST"
```

## Best Practices

- Return 204 for preflight, with no body
- Include Vary: Origin for caching correctness
- Set Access-Control-Max-Age to reduce repeated preflights
- Echo only allowed headers and methods
- Never reflect arbitrary origins when credentials are used

## Capabilities

### preflight-debug
Send preflight OPTIONS requests with curl and inspect the Access-Control response headers

**Commands:**
- `curl -i -X OPTIONS http://localhost:8080/api -H "Origin: http://localhost:3000" -H "Access-Control-Request-Method: PUT" -H "Access-Control-Request-Headers: X-Custom-Header,Content-Type"`
- `curl -s -o /dev/null -w "%{http_code}" -X OPTIONS http://localhost:8080/api -H "Origin: http://localhost:3000" -H "Access-Control-Request-Method: POST"`
- `curl -s -D - -o /dev/null -X OPTIONS http://localhost:8080/api -H "Origin: http://localhost:3000" -H "Access-Control-Request-Method: DELETE" | grep -i access-control`
- `curl -i -X OPTIONS http://localhost:8080/api -H "Origin: http://evil.com" -H "Access-Control-Request-Method: POST"`

**Examples:**
- curl -i -X OPTIONS http://localhost:8080/api -H "Origin: http://localhost:3000" -H "Access-Control-Request-Method: POST"
- curl -s -D - -o /dev/null -X OPTIONS http://localhost:8080/api -H "Origin: http://localhost:3000" -H "Access-Control-Request-Method: PUT" -H "Access-Control-Request-Headers: Authorization" | grep -i access-control
- curl -s -o /dev/null -w "preflight status: %{http_code}\n" -X OPTIONS http://localhost:8080/api -H "Origin: http://localhost:3000" -H "Access-Control-Request-Method: GET"

### preflight-config
Configure preflight handling with middleware and caching headers

**Commands:**
- `npm install cors`
- `node server.js`
- `curl -s -D - -o /dev/null -X OPTIONS http://localhost:8080/api -H "Origin: http://localhost:3000" -H "Access-Control-Request-Method: POST" | grep -i access-control-max-age`
- `curl -s -D - -o /dev/null -X OPTIONS http://localhost:8080/api -H "Origin: http://localhost:3000" -H "Access-Control-Request-Method: POST" | grep -i 'access-control-allow-\|access-control-max-age'`

**Examples:**
- npm install cors && node server.js
- curl -s -D - -o /dev/null -X OPTIONS http://localhost:8080/api -H "Origin: http://localhost:3000" -H "Access-Control-Request-Method: POST" | grep -i access-control-max-age
- curl -s -D - -o /dev/null -X OPTIONS http://localhost:8080/api -H "Origin: http://localhost:3000" -H "Access-Control-Request-Method: DELETE" | grep -ci 'access-control-allow-'

