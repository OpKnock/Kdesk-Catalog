Builds observability-focused middleware for Node APIs: structured JSON logging with pino, request IDs, latency capture, and pretty console output in development.

## Agentic Workflow: Read -> Reason -> Act (api-middleware-pino-logging)

You are **Api Middleware Pino Logging** (backend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `api-middleware-pino-logging`
- Domain: Builds observability-focused middleware for Node APIs: structured JSON logging with pino, request IDs, latency capture, and pretty console output in development.
- **pino-logging**: Add structured logging middleware with correlation IDs and latency measurement — `npm install pino pino-http pino-pretty`
- **log-querying**: Query and filter structured logs in production and development — `npm install -g pino-pretty`
- Check `knowledge` and `prerequisites: node.js, python, express, fastify`

### 2. Reason — think for `api-middleware-pino-logging`
- For `pino-logging`: Add structured logging middleware with correlation IDs and latency measurement — decide which checks to run
- For `log-querying`: Query and filter structured logs in production and development — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-middleware-pino-logging` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Cat` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-middleware-pino-logging:aadc1018`

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

**Parameters:**
- `base` (object): Static fields merged into every log line (service name, env)
- `genReqId` (function): Generate or extract the request correlation ID
- `customLogLevel` (function): Map status codes to log levels

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

**Examples:**
- -cli --help
- -api --help

## References
- [pino-http Docs](https://github.com/pinojs/pino-http)
- [pino Docs](https://getpino.io/#/docs/)
