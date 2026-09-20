# Cors

Configure and debug Cross-Origin Resource Sharing: setting CORS headers, preflight handling, and origin allowlists.

## Instructions

# CORS

Configure and debug Cross-Origin Resource Sharing for APIs.

## When to Use

- Allowing browser apps on other origins to call your API
- Handling preflight OPTIONS requests
- Restricting credentials sharing to trusted origins

## Inspect CORS Headers

```bash
curl -i -H "Origin: http://github.com" https://httpbin.org/get
curl -s -D - -o /dev/null -H "Origin: http://untrusted-origin.test" https://httpbin.org/get | grep -i access-control
```

A correct response includes:

```
Access-Control-Allow-Origin: http://github.com
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
Vary: Origin
```

## Express

```bash
npm install cors
```

```js
const cors = require('cors');
app.use(cors({
  origin: ['http://localhost:3000', 'https://app.github.com'],
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true
}));
```

```bash
node server.js &
curl -i -H "Origin: http://localhost:3000" http://localhost:8080/api
```

## Credentials

When `credentials: true`, the Allow-Origin header must echo the exact origin, never `*`.

## Testing

```bash
curl -i -X OPTIONS http://localhost:8080/api -H "Origin: http://localhost:3000" -H "Access-Control-Request-Method: POST"
curl -s -D - -o /dev/null -H "Origin: http://blocked-origin.test" http://localhost:8080/api | grep -i access-control-allow-origin
```

## Best Practices

- Never use `Access-Control-Allow-Origin: *` with credentials
- Set `Vary: Origin` to enable caching
- Keep the allowlist minimal
- Test both allowed and disallowed origins
- Handle OPTIONS preflight explicitly or via middleware

## Capabilities

### cors-headers
Configure CORS headers on API responses and test them with curl

**Commands:**
- `curl -i -H "Origin: http://github.com" https://httpbin.org/get`
- `curl -s -D - -o /dev/null -H "Origin: http://github.com" https://httpbin.org/get | grep -i access-control`
- `curl -s -o /dev/null -w "%{http_code}" -H "Origin: http://github.com" https://httpbin.org/get`
- `curl -sI -H "Origin: http://github.com" https://httpbin.org/get`

**Examples:**
- curl -i -H "Origin: http://localhost:3000" http://localhost:8080/api/users
- curl -s -D - -o /dev/null -H "Origin: http://github.com" https://httpbin.org/get | grep -i access-control
- curl -s -D - -o /dev/null -H "Origin: http://untrusted-origin.test" https://httpbin.org/get | grep -i access-control

### express-cors
Configure CORS with the cors npm package and restrict allowed origins

**Commands:**
- `npm install cors`
- `node server.js`
- `curl -i -H "Origin: http://localhost:3000" http://localhost:8080/api`
- `curl -i -X OPTIONS http://localhost:8080/api -H "Origin: http://localhost:3000" -H "Access-Control-Request-Method: GET"`

**Examples:**
- npm install cors && node server.js
- curl -i -H "Origin: http://localhost:3000" http://localhost:8080/api
- curl -s -D - -o /dev/null -H "Origin: http://blocked-origin.test" http://localhost:8080/api | grep -i access-control-allow-origin