---
type: agent_requested
description: "Designs and builds Node.js API middleware pipelines for Express and Fastify: logging, authentication, validation, error handling, and rate limiting with production ordering."
---

# api-middleware-engineer

Designs and builds Node.js API middleware pipelines for Express and Fastify: logging, authentication, validation, error handling, and rate limiting with production ordering.

## Instructions

# API Middleware Engineer

Builds layered middleware pipelines for Express and Fastify APIs.

## What This Skill Does
- Writes logging, authentication, validation, error-handling, and rate-limiting middleware
- Orders middleware correctly so early layers (logs, security headers, body parsing) run before business logic
- Provides centralized error handlers and async error propagation

## When to Use
- Adding cross-cutting concerns to an existing API
- Standardizing request/response logging across services
- Enforcing auth and rate limits on selected route prefixes

## Real Commands

```bash
# Scaffold and install
npm init -y
npm install express morgan helmet cors express-rate-limit

# Run and probe the pipeline
node app.js
curl -i http://localhost:3000/api/health

# Verify middleware ordering with lint and tests
npx eslint . --ext .js
npm test
```

## Pipeline Example

```js
const express = require('express');
const morgan = require('morgan');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const app = express();
app.use(helmet());
app.use(morgan('combined'));
app.use(express.json());
app.use('/api', rateLimit({ windowMs: 60 * 1000, limit: 60 }));
app.use((err, req, res, next) => res.status(500).json({ error: err.message }));
app.listen(3000);
```

## Testing
- Use supertest to mount the app and assert status codes, headers, and error bodies
- Test that the rate limiter returns 429 after the configured limit
- Verify error middleware runs for both sync and async handlers

## Best Practices
- Auth middleware must run before route handlers, never after
- Always call next() in non-terminating middleware or the pipeline stalls
- Wrap async handlers so rejected promises reach the error handler

## Capabilities

### express-pipeline
Assemble a layered Express middleware pipeline (logging -> security headers -> body parsing -> auth -> validation -> routes -> errors)

**Commands:**
- `npm init -y && npm install express morgan helmet cors express-rate-limit`
- `node app.js`
- `curl -i http://localhost:3000/api/health`
- `npx eslint . --ext .js`
- `npm test`

**Examples:**
- npm install morgan; app.use(morgan('combined')) for request logging
- app.use(helmet()) to set security headers before routes
- app.use('/api', rateLimit({ windowMs: 60000, limit: 60 }))

### pipeline-testing
Verify middleware behavior with supertest against a mounted app instance

**Commands:**
- `npm install supertest jest`
- `npx jest --coverage`
- `curl -s -X POST http://localhost:3000/api/items -d '{}' -H 'Content-Type: application/json'`
- `curl -s http://localhost:3000/api/protected`

**Examples:**
- -cli --help
- -api --help