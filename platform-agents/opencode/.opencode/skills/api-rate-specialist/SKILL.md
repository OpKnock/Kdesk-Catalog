---
name: "api-rate-specialist"
description: "Implements application-level rate limiting with express-rate-limit and @fastify/rate-limit: window configuration, skip logic, headers, and standardizer patterns. Use when working with express rate limit, fastify rate limit or when the user mentions express rate limit, fastify rate limit."
---

Implements application-level rate limiting with express-rate-limit and @fastify/rate-limit: window configuration, skip logic, headers, and standardizer patterns.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npm install express-rate-limit`, `npm install @fastify/rate-limit`
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
