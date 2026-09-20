---
type: agent_requested
description: "Build high-performance Node.js APIs with Fastify: plugins, schema validation, hooks, and benchmarking with autocannon."
---

# Fastify

Build high-performance Node.js APIs with Fastify: plugins, schema validation, hooks, and benchmarking with autocannon.

## Instructions

# Fastify

## What this skill does

Fastify is a fast, low-overhead Node.js framework with JSON Schema validation built in. It is plugin-based, encapsulated, and ships with benchmarks-first performance tooling (autocannon).

## When to use

- Building APIs where latency and throughput matter
- Organizing code into plugins with shared decorators and hooks
- Validating payloads with JSON Schema without extra libraries

## Real commands

```bash
# Scaffold
npm create fastify@latest my-app
cd my-app

# Run dev/prod
npm run dev
npm start

# Plugins
npm install @fastify/cors @fastify/jwt

# Load test
npx autocannon -c 50 -d 10 http://localhost:3000/api/orders
```

## Route with schema example

```javascript
const fastify = require('fastify')({ logger: true })

fastify.get('/api/orders/:id', {
  schema: {
    params: { type: 'object', properties: { id: { type: 'string' } } },
    response: { 404: { type: 'object', properties: { message: { type: 'string' } } } }
  }
}, async (request, reply) => {
  const order = await db.find(request.params.id)
  if (!order) return reply.code(404).send({ message: 'not found' })
  return order
})

fastify.listen({ port: 3000 })
```

## Testing

```bash
npm run test
# or manual smoke
curl -s localhost:3000/api/orders/1 | jq
```

## Best practices

- Encapsulate features in plugins; pass shared state via decorators.
- Always define JSON Schema for routes to get serialization speedups.
- Use fastify.addHook for auth/logging instead of middleware wrappers.
- Benchmark every change with autocannon and keep a baseline file.
- Register plugins with fastify-plugin when they must cross encapsulation.

## Capabilities

### fastify-development
Scaffold, run, extend, and benchmark Fastify applications.

**Commands:**
- `npm create fastify@latest my-app`
- `npm install fastify @fastify/cors @fastify/jwt`
- `npm run dev`
- `npm start`
- `npx autocannon -c 50 -d 10 http://localhost:3000/api/orders`
- `npm run test`

**Examples:**
- npm create fastify@latest my-app && cd my-app && npm run dev
- npx autocannon -c 50 -d 10 http://localhost:3000/api/orders
- npm install @fastify/cors @fastify/jwt && npm start