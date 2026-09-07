Implements application-level rate limiting with Redis-backed sliding windows, token buckets, and fixed windows. Configures Express/Fastify middleware, nginx limits, and validates enforcement with load tests and header assertions.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `redis-cli --eval sliding_window.lua rate:user:123 1 100 60`, `npm install express-rate-limit`
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

# API Rate Limiter

## What this agent does

Implements rate limiting at the application layer: Redis-backed sliding window and token bucket
algorithms with atomic Lua scripts, Express/Fastify middleware integration, and nginx edge limiting.
Validates enforcement with load tests, verifies standard headers (RateLimit-Limit, RateLimit-Remaining,
Retry-After), and handles 429 responses with proper JSON error bodies.

## When to use

- Protecting API endpoints from abuse and DoS
- Enforcing per-user, per-API-key, or per-IP quotas
- Implementing tiered limits (free/pro/enterprise)
- Adding rate limit headers for client-side backoff
- Combining edge (nginx) and application-level limits

## Real commands

```bash
# Redis sliding window (atomic Lua)
redis-cli --eval sliding_window.lua rate:user:42 1 100 60 $(date +%s)

# Redis token bucket
redis-cli --eval token_bucket.lua rate:user:42 10 100

# Fixed window with INCR/EXPIRE
redis-cli EVAL 'local c=redis.call("INCR",KEYS[1]) if c==1 then redis.call("EXPIRE",KEYS[1],ARGV[1]) end return c' 1 rate:user:42 60

# Express middleware
npm install express-rate-limit

# Fastify plugin
npm install @fastify/rate-limit @fastify/redis

# nginx config
nginx -t && nginx -s reload
```

## Express rate limiter example

```javascript
const rateLimit = require("express-rate-limit");

const limiter = rateLimit({
  windowMs: 60 * 1000,
  max: 100,
  keyGenerator: (req) => req.headers["x-api-key"] || req.ip,
  handler: (req, res) => res.status(429).json({ error: "Too Many Requests" }),
  standardHeaders: true,
  legacyHeaders: false,
});

app.use("/api/", limiter);
```

## Fastify rate limiter example

```javascript
await fastify.register(require("@fastify/rate-limit"), {
  max: 100,
  timeWindow: "1 minute",
  keyGenerator: (req) => req.headers["x-api-key"] || req.ip,
  redis: fastify.redis,
  addHeaders: {
    "x-ratelimit-limit": true,
    "x-ratelimit-remaining": true,
    "retry-after": true,
  },
});
```

## nginx rate limiting

```nginx
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

server {
  location /api/ {
    limit_req zone=api burst=20 nodelay;
    limit_req_status 429;
    proxy_pass http://backend;
  }
}
```

## Testing

- Drive traffic at 2x limit with `hey` or `k6`, assert 429 rate
- Verify `RateLimit-Limit`, `RateLimit-Remaining`, `Retry-After` headers
- Test keyGenerator: different API keys get independent limits
- Verify Redis connection failure behavior (fail-open vs fail-closed)

## Best practices

- Use sliding window for accuracy; token bucket for burst tolerance
- Return standard RateLimit headers (draft-ietf-httpapi-ratelimit-headers)
- Combine nginx (per-IP) with app middleware (per-user/key) for defense in depth
- Monitor limit exhaustion: `rate(http_requests_total{status="429"}[5m])`
- Store limits in config, not code; support runtime updates

## Capabilities

### redis-sliding-window
Implements Redis-backed sliding window rate limiting with Lua scripts for atomicity.

**Parameters:**
- `key` (string): Redis key pattern (e.g., rate:user:{id})
- `limit` (number): Max requests per window
- `window_seconds` (number): Window size in seconds

**Commands:**
- `redis-cli --eval sliding_window.lua rate:user:123 1 100 60`
- `redis-cli --eval token_bucket.lua rate:user:123 10 100`
- `redis-cli GET rate:user:123`
- `redis-cli ZRANGEBYSCORE rate:user:123 0 $(date +%s)`

**Examples:**
- redis-cli --eval sliding_window.lua rate:user:42 1 100 60 $(date +%s)
- redis-cli --eval token_bucket.lua rate:user:42 10 100
- redis-cli EVAL "local c=redis.call(\"INCR\",KEYS[1]) if c==1 then redis.call(\"EXPIRE\",KEYS[1],ARGV[1]) end return c" 1 rate:user:42 60

### express-middleware
Configures express-rate-limit middleware with custom key generators and handlers.

**Parameters:**
- `window_ms` (number): Window size in milliseconds
- `max_requests` (number): Maximum requests per window
- `key_generator` (string): Function to extract rate limit key (ip, user, apikey)

**Commands:**
- `npm install express-rate-limit`
- `printf "const rateLimit = require(\"express-rate-limit\");\nmodule.exports = rateLimit({\n  windowMs: 60 * 1000,\n  max: 100,\n  keyGenerator: (req) => req.ip,\n  handler: (req, res) => res.status(429).json({error: \"Too Many Requests\"}),\n  standardHeaders: true,\n  legacyHeaders: false\n});" > rate-limiter.js`

**Examples:**
- npm install express-rate-limit
- printf "const rateLimit = require(\"express-rate-limit\");\nmodule.exports = rateLimit({\n  windowMs: 60 * 1000,\n  max: 100,\n  keyGenerator: (req) => req.headers[\"x-api-key\"] || req.ip,\n  handler: (req, res) => res.status(429).json({error: \"Too Many Requests\"}),\n  standardHeaders: true,\n  legacyHeaders: false\n});" > rate-limiter.js

### fastify-middleware
Configures @fastify/rate-limit plugin with Redis store.

**Parameters:**
- `max` (number): Maximum requests per window
- `time_window` (string): Window duration (e.g., "1 minute", "1 hour")
- `redis` (string): Redis client instance

**Commands:**
- `npm install @fastify/rate-limit @fastify/redis`
- `printf "async function rateLimitPlugin(fastify) {\n  await fastify.register(require(\"@fastify/rate-limit\"), {\n    max: 100,\n    timeWindow: \"1 minute\",\n    keyGenerator: (req) => req.headers[\"x-api-key\"] || req.ip,\n    redis: fastify.redis\n  });\n}\nmodule.exports = rateLimitPlugin;" > rate-limit.js`

**Examples:**
- npm install @fastify/rate-limit @fastify/redis
- printf "async function rateLimitPlugin(fastify) {\n  await fastify.register(require(\"@fastify/rate-limit\"), {\n    max: 100,\n    timeWindow: \"1 minute\",\n    keyGenerator: (req) => req.headers[\"x-api-key\"] || req.ip,\n    redis: fastify.redis\n  });\n}\nmodule.exports = rateLimitPlugin;" > rate-limit.js

### nginx-limits
Configures nginx limit_req_zone and limit_req for edge rate limiting.

**Parameters:**
- `zone_name` (string): Shared memory zone name
- `rate` (string): Rate limit (e.g., 10r/s, 100r/m)
- `burst` (number): Burst allowance

**Commands:**
- `nginx -t`
- `nginx -s reload`
- `curl -i http://localhost/api`
- `printf "limit_req_zone \$binary_remote_addr zone=api:10m rate=10r/s;\nserver {\n  location /api/ {\n    limit_req zone=api burst=20 nodelay;\n    limit_req_status 429;\n    proxy_pass http://backend;\n  }\n}" > /etc/nginx/conf.d/ratelimit.conf`
- `nginx -t && nginx -s reload`

**Examples:**
- printf "limit_req_zone \$binary_remote_addr zone=api:10m rate=10r/s;\nserver {\n  location /api/ {\n    limit_req zone=api burst=20 nodelay;\n    limit_req_status 429;\n    proxy_pass http://backend;\n  }\n}" > /etc/nginx/conf.d/ratelimit.conf
- nginx -t && nginx -s reload

## References
- [express-rate-limit](https://github.com/express-rate-limit/express-rate-limit)
- [fastify-rate-limit](https://github.com/fastify/fastify-rate-limit)
- [nginx limit_req Module](https://nginx.org/en/docs/http/ngx_http_limit_req_module.html)
- [Redis Rate Limiting Patterns](https://redis.io/docs/latest/develop/use-cases/rate-limiting/)
- [Rate Limiting Headers](https://datatracker.ietf.org/doc/html/draft-ietf-httpapi-ratelimit-headers)

## Progressive Disclosure
This skill has many capabilities. For detailed reference:
- `references/REFERENCE.md` — full capability docs and edge cases
- `scripts/` — executable helpers (see `allowed-tools`)
- `assets/` — templates and data files
Load references on demand via relative paths, not at startup.