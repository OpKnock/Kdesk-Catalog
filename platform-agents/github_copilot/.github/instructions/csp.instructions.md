---
applyTo: "**/*.json **/*.r **/*.sh"
---

Hardens API and web endpoints with Content-Security-Policy headers, using Helmet middleware and curl verification against real echo services.

## Agentic Workflow: Read -> Reason -> Act (csp)

You are **Csp** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `csp`
- Domain: Hardens API and web endpoints with Content-Security-Policy headers, using Helmet middleware and curl verification against real echo services.
- **header-verification**: Inspect and verify Content-Security-Policy response headers on live endpoints — `curl -sI https://httpbin.org/headers | grep -i content-security-policy`
- **helmet-config**: Configure CSP and related security headers with helmet in Node.js — `npm install helmet`
- Check `knowledge` and `prerequisites: node, npm`

### 2. Reason — think for `csp`
- For `header-verification`: Inspect and verify Content-Security-Policy response headers on live endpoints — decide which checks to run
- For `helmet-config`: Configure CSP and related security headers with helmet in Node.js — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `csp` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `csp:0c64db9e`

# Content Security Policy (CSP)

Implement and verify Content-Security-Policy headers for APIs and web endpoints.

## When to Use

- Hardening API responses against XSS and injection
- Enforcing a strict allowlist of origins and scripts
- Auditing which headers a deployed endpoint actually returns

## Verify Existing Headers

```bash
curl -sI https://httpbin.org/headers | grep -i content-security-policy
curl -s -D - -o /dev/null https://httpbin.org/headers
```

## Minimal Policy

```
Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none';
  frame-ancestors 'none'
```

## Node.js with Helmet

```bash
npm install helmet
```

```js
const express = require('express');
const helmet = require('helmet');
const app = express();
app.use(helmet.contentSecurityPolicy({
  directives: {
    "default-src": ["'self'"],
    "script-src": ["'self'"],
    "object-src": ["'none'"],
    "frame-ancestors": ["'none'"]
  }
}));
app.get('/health', (req, res) => res.json({ ok: true }));
app.listen(8080);
```

```bash
node server.js &
curl -sI http://localhost:8080/health | grep -i content-security-policy
```

## Rollout Strategy

```
# Start with report-only mode to observe violations
Content-Security-Policy-Report-Only: default-src 'self'
# Then enforce after reviewing violation reports
Content-Security-Policy: default-src 'self'
```

## Testing

```bash
curl -s -D - -o /dev/null http://localhost:8080/health | grep -i content-security
```

## Best Practices

- Start with report-only mode before enforcing
- Keep a violation-report-uri to monitor breakage
- Avoid unsafe-inline and unsafe-eval in production
- Use nonces or hashes for inline scripts
- Verify headers on every environment, not just production

## Capabilities

### header-verification
Inspect and verify Content-Security-Policy response headers on live endpoints

**Parameters:**
- `url` (string): URL to check for CSP headers

**Commands:**
- `curl -sI https://httpbin.org/headers | grep -i content-security-policy`
- `curl -s -D - -o /dev/null https://httpbin.org/headers | grep -i 'content-security-policy\|x-frame-options'`
- `curl -s -H "Accept: application/json" https://httpbin.org/headers -D - -o /dev/null | grep -i content-security`
- `curl -sI http://localhost:8080 | grep -i content-security-policy`

**Examples:**
- curl -sI https://httpbin.org/headers | grep -i content-security-policy
- curl -s -D - -o /dev/null https://httpbin.org/headers | grep -i 'content-security'
- curl -sI http://localhost:8080 | awk 'tolower($1) ~ /content-security/{print}'

### helmet-config
Configure CSP and related security headers with helmet in Node.js

**Parameters:**
- `directives` (string): CSP directives such as default-src 'self'

**Commands:**
- `npm install helmet`
- `node -e "const helmet=require('helmet'); console.log(typeof helmet.contentSecurityPolicy)"`
- `npm run start`
- `curl -sI http://localhost:8080/health | grep -i content-security-policy`

**Examples:**
- npm install helmet && npm run start
- curl -sI http://localhost:8080 | grep -i content-security-policy
- npm test

## References
- [MDN CSP Guide](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)
- [Helmet Docs](https://helmetjs.github.io/)
