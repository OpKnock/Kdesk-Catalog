---
name: "koa"
description: "Build async web applications with Koa: middleware composition, routers, body parsing, and error handling with the koa ecosystem. Use when working with koa app, verify endpoints, api or when the user mentions koa app, verify endpoints, api."
type: knowledge
triggers: ["koa", "koa-app", "verify-endpoints"]
---

Build async web applications with Koa: middleware composition, routers, body parsing, and error handling with the koa ecosystem.

## Agentic Workflow: Read -> Reason -> Act (koa)

You are **Koa** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `koa`
- Domain: Build async web applications with Koa: middleware composition, routers, body parsing, and error handling with the koa ecosystem.
- **koa-app**: Scaffold and run a Koa application with router and bodyparser. — `npm init -y`
- **verify-endpoints**: Test Koa endpoints with curl including JSON bodies and errors. — `curl -i http://localhost:3000/`
- Check `knowledge` and `prerequisites: node, npm`

### 2. Reason — think for `koa`
- For `koa-app`: Scaffold and run a Koa application with router and bodyparser. — decide which checks to run
- For `verify-endpoints`: Test Koa endpoints with curl including JSON bodies and errors. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `koa` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `koa:f5bf6904`

# Koa

Build async Node.js web apps with Koa's onion-style middleware.

## What this skill does

- Scaffolds Koa projects with router and bodyparser.
- Implements cascading middleware and error handling.
- Tests endpoints with curl.

## When to use

- Lightweight APIs that need async-first middleware.
- Serving as a BFF layer in Node microservice architectures.
- Learning middleware composition and ctx lifecycle.

## Real commands

```bash
# Scaffold
npm init -y
npm install koa koa-router koa-bodyparser

# Run
node app.js

# Watch mode
node --watch app.js

# Test endpoints
curl -i http://localhost:3000/
curl -i -X POST http://localhost:3000/api/users \
  -H 'Content-Type: application/json' -d '{"name":"alice"}'
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:3000/not-found
```

## app.js example

```js
const Koa = require('koa');
const Router = require('koa-router');
const bodyParser = require('koa-bodyparser');

const app = new Koa();
const router = new Router();

app.use(async (ctx, next) => {
  const start = Date.now();
  await next();
  ctx.set('X-Response-Time', String(Date.now() - start));
});

app.use(bodyParser());

router.get('/', ctx => { ctx.body = { ok: true }; });
router.post('/api/users', ctx => {
  ctx.status = 201;
  ctx.body = { id: 1, ...ctx.request.body };
});

app.use(router.routes());
app.use(router.allowedMethods());

app.listen(3000);
```

## Testing

```bash
node --check app.js   # syntax check
```

## Best practices

- Keep middleware small and ordered: logger, errors, body, then routes.
- Set ctx.body before awaiting downstream to avoid double sends.
- Use koa-jwt for auth and koa-helmet for security headers.

## Capabilities

### koa-app
Scaffold and run a Koa application with router and bodyparser.

**Parameters:**
- `port` (integer): Listen port, default 3000.
- `framework` (string): Package set: koa, koa-router, koa-bodyparser.

**Commands:**
- `npm init -y`
- `npm install koa koa-router koa-bodyparser`
- `node app.js`
- `node --watch app.js`
- `npm install -D nodemon`

**Examples:**
- npm init -y && npm install koa koa-router koa-bodyparser
- node app.js
- node --watch app.js

### verify-endpoints
Test Koa endpoints with curl including JSON bodies and errors.

**Parameters:**
- `endpoint` (string): Path to test.
- `method` (string): HTTP method.
- `body` (string): JSON request body.

**Commands:**
- `curl -i http://localhost:3000/`
- `curl -i -X POST http://localhost:3000/api/users -H 'Content-Type: application/json' -d '{"name":"alice"}'`
- `curl -s -o /dev/null -w '%{http_code}\n' http://localhost:3000/not-found`
- `curl -i http://localhost:3000/api/users/1`

**Examples:**
- curl -i http://localhost:3000/
- curl -i -X POST http://localhost:3000/api/users -H 'Content-Type: application/json' -d '{"name":"alice"}'
- curl -s -o /dev/null -w '%{http_code}\n' http://localhost:3000/not-found

## References
- [Koa Documentation](https://koajs.com/)
- [koa-router](https://github.com/koajs/router)
