# Api Middleware Fastify Plugins

Builds Fastify APIs with the official plugin ecosystem: @fastify/cors, @fastify/rate-limit, @fastify/jwt, @fastify/helmet, and @fastify/sensible for unified error responses.

## Instructions

# API Middleware v3 - Fastify Plugins

Middleware via the official Fastify plugin ecosystem.

## What This Skill Does
- Registers CORS, rate limiting, JWT auth, helmet, and error plugins
- Uses Fastify encapsulation to scope plugins to route prefixes
- Provides uniform error envelopes with @fastify/sensible

## When to Use
- Starting a new Fastify service that needs cross-cutting concerns
- Migrating Express middleware to Fastify plugins
- Adding scoped auth to admin route subsets

## Real Commands

```bash
npm install fastify @fastify/cors @fastify/rate-limit @fastify/jwt @fastify/helmet @fastify/sensible
node server.js
curl -s -H 'Origin: https://app.example.com' -D- http://localhost:3000/api | grep -i 'access-control'
```

## Plugin Registration

```js
const app = require('fastify')({ logger: true });
await app.register(require('@fastify/helmet'));
await app.register(require('@fastify/cors'), { origin: ['https://app.example.com'] });
await app.register(require('@fastify/rate-limit'), { max: 60, timeWindow: '1 minute' });
await app.register(require('@fastify/jwt'), { secret: process.env.JWT_SECRET });
```

## Testing
- Check CORS preflight returns Access-Control-Allow-Origin for allowed origins
- Hammer an endpoint to confirm 429 after the limit
- Verify unauthorized requests return 401 without a valid JWT

## Best Practices
- Register auth plugins before routes that need protection
- Scope heavy plugins (rate limit) to prefixes with encapsulation
- Use sensible's httpErrors for consistent error shapes

## Capabilities

### fastify-plugins
Register and configure Fastify plugin middleware

**Commands:**
- `npm install fastify @fastify/cors @fastify/rate-limit @fastify/jwt @fastify/helmet @fastify/sensible`
- `npm init fastify`
- `node server.js`
- `curl -s -H 'Origin: http://localhost:8080' -D- http://localhost:3000/api | grep -i 'access-control'`
- `curl -s -o /dev/null -w '%{http_code}\n' http://localhost:3000/api`

**Examples:**
- await app.register(require('@fastify/cors'), { origin: ['http://localhost:8080'] })
- await app.register(require('@fastify/rate-limit'), { max: 60, timeWindow: '1 minute' })
- await app.register(require('@fastify/jwt'), { secret: process.env.JWT_SECRET })

### plugin-encapsulation
Use Fastify plugin encapsulation to scope middleware to route subsets

**Commands:**
- `fastify start -p 3000 app.js`
- `node -e "const f=require('fastify')(); console.log(f.register ? 'fastify ready' : 'no')"`
- `curl -s http://localhost:3000/docs -o /dev/null -w '%{http_code}\n'`

**Examples:**
- -cli --help
- -api --help
