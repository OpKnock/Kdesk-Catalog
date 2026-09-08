---
applyTo: "**/*.r **/*.sh"
---

Implements application-level rate limiting with express-rate-limit and @fastify/rate-limit: window configuration, skip logic, headers, and standardizer patterns.

## Agentic Workflow: Read -> Reason -> Act (api-rate-specialist)

You are **api-rate-specialist** (security) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — security context for `api-rate-specialist`
- Domain: Implements application-level rate limiting with express-rate-limit and @fastify/rate-limit: window configuration, skip logic, headers, and standardizer patterns.
- **express-rate-limit**: Configure express-rate-limit middleware options — `npm install express-rate-limit`
- **fastify-rate-limit**: Configure the Fastify rate limit plugin — `npm install @fastify/rate-limit`
- Check `knowledge` and `prerequisites: redis, node.js, python`

### 2. Reason — think for `api-rate-specialist`
- For `express-rate-limit`: Configure express-rate-limit middleware options — decide which checks to run
- For `fastify-rate-limit`: Configure the Fastify rate limit plugin — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-rate-specialist` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `For` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-rate-specialist:a4b09dd8`

# API Rate Specialist

App-level rate limiting libraries.

## What This Skill Does
- Adds in-process rate limiting to Express and Fastify
- Emits standard RateLimit headers
- Supports custom key generation and skip rules

## When to Use
- Single-instance services needing quick throttling
- Per-route limits (login, uploads)
- Building blocks before a gateway strategy

## Real Commands

```bash
npm install express-rate-limit
curl -s -D- -o /dev/null http://localhost:3000/api | grep -i 'x-ratelimit'
for i in $(seq 1 120); do curl -s -o /dev/null -w '%{http_code}\n' http://localhost:3000/api; done | sort | uniq -c
```

## Configuration

```js
app.use('/api', rateLimit({
  windowMs: 60 * 1000,
  limit: 100,
  standardHeaders: 'draft-8',
  keyGenerator: (req) => req.headers['x-client-id'] || req.ip
}));
```

## Testing
- Confirm 429 after exceeding the limit
- Validate RateLimit-Reset header math
- Verify skip rules bypass counting for health checks

## Best Practices
- Mount tight limits on auth endpoints first
- Use a shared store (Redis) for multi-instance deployments
- Return informative Retry-After with 429s

## Capabilities

### express-rate-limit
Configure express-rate-limit middleware options

**Parameters:**
- `windowMs` (integer): Window duration in milliseconds
- `limit` (integer): Maximum requests per window
- `keyGenerator` (function): Client key derivation function

**Commands:**
- `npm install express-rate-limit`
- `node -e "const rateLimit=require('express-rate-limit'); console.log(rateLimit({windowMs:60000,limit:100}).name)"`
- `curl -s -D- -o /dev/null http://localhost:3000/api | grep -i 'x-ratelimit'`
- `curl -s -o /dev/null -w '%{http_code}\n' -X POST http://localhost:3000/api/login`
- `for i in $(seq 1 120); do curl -s -o /dev/null -w '%{http_code}\n' http://localhost:3000/api; done | sort | uniq -c`

**Examples:**
- rateLimit({ windowMs: 60000, limit: 100 }) allows 100 req/min
- standardHeaders: true emits RateLimit-* headers
- skip: (req) => req.ip === '127.0.0.1' bypasses localhost

### fastify-rate-limit
Configure the Fastify rate limit plugin

**Commands:**
- `npm install @fastify/rate-limit`
- `curl -s -o /dev/null -w '%{http_code}\n' http://localhost:3000/api`
- `node -e "const rl=require('@fastify/rate-limit'); console.log(typeof rl)"`

**Examples:**
- -cli --help
- -api --help

## References
- [express-rate-limit](https://expressjs.com/en/resources/middleware/rate-limit.html)
- [@fastify/rate-limit](https://github.com/fastify/fastify-rate-limit)
