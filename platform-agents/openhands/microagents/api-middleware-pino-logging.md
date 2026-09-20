---
name: "api-middleware-pino-logging"
description: "Builds observability-focused middleware for Node APIs: structured JSON logging with pino, request IDs, latency capture, and pretty console output in development."
type: knowledge
triggers: ["api-middleware-pino-logging", "pino-logging", "log-querying"]
---

# Api Middleware Pino Logging

Builds observability-focused middleware for Node APIs: structured JSON logging with pino, request IDs, latency capture, and pretty console output in development.

## Instructions

# API Middleware v2 - Observability

Logging and correlation middleware for Node.js APIs.

## What This Skill Does
- Adds pino-http middleware for JSON request logging
- Propagates X-Request-Id correlation IDs through the pipeline
- Measures per-request latency and status mapping

## When to Use
- Debugging distributed request traces
- Switching from text logs to structured JSON
- Adding service metadata to all log lines

## Real Commands

```bash
npm install pino pino-http pino-pretty
node app.js | npx pino-pretty
curl -s -H "X-Request-Id: 123e4567" http://localhost:3000/api/health
```

## Middleware Setup

```js
const pinoHttp = require('pino-http');
app.use(pinoHttp({
  genReqId: (req) => req.headers['x-request-id'],
  base: { service: 'billing-api' },
  customLogLevel: (req, res, err) => err ? 'error' : res.statusCode >= 400 ? 'warn' : 'info'
}));
```

## Testing
- Send a request with an X-Request-Id header and confirm it appears in log output
- Verify 5xx responses produce error-level log lines
- Confirm logs parse with jq for field extraction

## Best Practices
- Never log bodies of auth endpoints
- Use genReqId to honor incoming correlation headers
- Keep pino as a direct dependency so serializers are stable

## Capabilities

### pino-logging
Add structured logging middleware with correlation IDs and latency measurement

**Commands:**
- `npm install pino pino-http pino-pretty`
- `node app.js | npx pino-pretty`
- `curl -s -H "X-Request-Id: 123e4567" http://localhost:3000/api/health`
- `curl -s -o /dev/null -w "%{http_code} %{time_total}s\n" http://localhost:3000/api`

**Examples:**
- node app.js | npx pino-pretty renders human-readable logs in dev
- app.use(pinoHttp({ genReqId: (req) => req.headers['x-request-id'] }))
- curl -H 'X-Request-Id: abc' localhost:3000/ traces a single request across logs

### log-querying
Query and filter structured logs in production and development

**Commands:**
- `npm install -g pino-pretty`
- `cat app.log | pino-pretty --translateTime`
- `jq 'select(.level >= 40)' app.log`
- `node -r pino-pretty app.js`
