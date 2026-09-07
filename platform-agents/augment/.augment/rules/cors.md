---
type: agent_requested
description: "Configure and debug Cross-Origin Resource Sharing: setting CORS headers, preflight handling, and origin allowlists. Use when working with cors headers, express cors, api or when the user mentions cors headers, express cors, api."
---

Configure and debug Cross-Origin Resource Sharing: setting CORS headers, preflight handling, and origin allowlists.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -i -H "Origin: http://github.com" https://httpbin.org/g`, `npm install cors`
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

**Parameters:**
- `origin` (string): Origin header to test, e.g. http://github.com

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

**Parameters:**
- `allowed_origins` (string): Comma-separated list of allowed origins

**Commands:**
- `npm install cors`
- `node server.js`
- `curl -i -H "Origin: http://localhost:3000" http://localhost:8080/api`
- `curl -i -X OPTIONS http://localhost:8080/api -H "Origin: http://localhost:3000" -H "Access-Control-Request-Method: GET"`

**Examples:**
- npm install cors && node server.js
- curl -i -H "Origin: http://localhost:3000" http://localhost:8080/api
- curl -s -D - -o /dev/null -H "Origin: http://blocked-origin.test" http://localhost:8080/api | grep -i access-control-allow-origin

## References
- [MDN CORS Guide](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [cors npm package](https://www.npmjs.com/package/cors)