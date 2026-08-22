---
trigger: glob
description: "Build async web applications with Koa: middleware composition, routers, body parsing, and error handling with the koa ecosystem."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
---

# Koa

Build async web applications with Koa: middleware composition, routers, body parsing, and error handling with the koa ecosystem.

## Instructions

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

**Commands:**
- `curl -i http://localhost:3000/`
- `curl -i -X POST http://localhost:3000/api/users -H 'Content-Type: application/json' -d '{"name":"alice"}'`
- `curl -s -o /dev/null -w '%{http_code}\n' http://localhost:3000/not-found`
- `curl -i http://localhost:3000/api/users/1`

**Examples:**
- curl -i http://localhost:3000/
- curl -i -X POST http://localhost:3000/api/users -H 'Content-Type: application/json' -d '{"name":"alice"}'
- curl -s -o /dev/null -w '%{http_code}\n' http://localhost:3000/not-found
