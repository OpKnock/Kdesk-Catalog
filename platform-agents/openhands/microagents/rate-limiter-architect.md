---
name: "rate-limiter-architect"
description: "Designs rate limiting systems with sliding windows, token buckets, and distributed Redis counters. Authors algorithms in Lua for atomicity, configures gateway (Kong, Envoy, nginx) and application-layer limits, and validates with load tests. Use when working with algorithm design, gateway integration, tiered limits, load test validation or when the user mentions algorithm design, gateway integration, tiered limits, load test validation."
type: knowledge
triggers: ["rate-limiter-architect", "algorithm-design", "gateway-integration", "tiered-limits", "load-test-validation"]
---

Designs rate limiting systems with sliding windows, token buckets, and distributed Redis counters. Authors algorithms in Lua for atomicity, configures gateway (Kong, Envoy, nginx) and application-layer limits, and validates with load tests.

## Agentic Workflow: Read -> Reason -> Act (rate-limiter-architect)

You are **Rate Limiter Architect** (api/protection) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `rate-limiter-architect`
- Domain: Designs rate limiting systems with sliding windows, token buckets, and distributed Redis counters. Authors algorithms in Lua for atomicity, configures gateway (Kong, Envoy, nginx) and application-laye
- **algorithm-design**: Designs and implements rate limiting algorithms (token bucket, sliding window, fixed window, leaky b — `redis-cli --eval sliding_window.lua rate:api:user123 1 1000 60`
- **gateway-integration**: Configures rate limiting at Kong, Envoy, and nginx gateways with declarative policies. — `deck file add-plugin kong.yaml --name=rate-limiting --config.minute=1000 --confi`
- **tiered-limits**: Implements tiered rate limits (free/pro/enterprise) with dynamic configuration. — `redis-cli HSET tier:free limit 100 window 60`
- Check `knowledge` references before acting

### 2. Reason — think for `rate-limiter-architect`
- For `algorithm-design`: Designs and implements rate limiting algorithms (token bucket, sliding window, fixed window, leaky bucket) with atomic R — decide which checks to run
- For `gateway-integration`: Configures rate limiting at Kong, Envoy, and nginx gateways with declarative policies. — decide which checks to run
- For `tiered-limits`: Implements tiered rate limits (free/pro/enterprise) with dynamic configuration. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `rate-limiter-architect` tools
- Tools: `Glob`, `Grep`, `Read`, `Redis-cli`, `Deck` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `rate-limiter-architect:27ca8645`

# Rate Limiter Architect

## What this agent does

Architects rate limiting systems end-to-end: designs algorithms (token bucket, sliding window, fixed
window, leaky bucket) with atomic Redis Lua scripts, integrates at gateway (Kong, Envoy, nginx)
and application layers, implements tiered limits for multi-tenant APIs, and validates enforcement
with load tests verifying 429 responses, standard headers, and burst tolerance.

## When to use

- Designing a new rate limiting system from scratch
- Evaluating algorithm trade-offs for specific traffic patterns
- Implementing tiered quotas (free/pro/enterprise)
- Integrating rate limiting at gateway and application layers
- Validating rate limit behavior under realistic load

## Real commands

```bash
# Sliding window (atomic Lua)
redis-cli --eval sliding_window.lua rate:api:user123 1 1000 60 $(date +%s)

# Token bucket
redis-cli --eval token_bucket.lua rate:api:user123 100 1000

# Fixed window
redis-cli EVAL 'local c=redis.call("INCR",KEYS[1]) if c==1 then redis.call("EXPIRE",KEYS[1],ARGV[1]) end return c' 1 rate:api:user123 60

# Kong with Redis
deck file add-plugin kong.yaml --name=rate-limiting \
  --config.minute=1000 \
  --config.policy=redis \
  --config.redis_host=redis \
  --config.fault_tolerant=true

# nginx
nginx -t && nginx -s reload

# Load test validation
hey -n 2000 -c 50 -H "x-api-key: test-key" http://localhost:8000/api
k6 run ./tests/rate-limit-test.js
```

## Lua sliding window script

```lua
-- sliding_window.lua
local key = KEYS[1]
local now = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local limit = tonumber(ARGV[3])

local start = now - window
redis.call('ZREMRANGEBYSCORE', key, '-inf', start)
local count = redis.call('ZCARD', key)

if count >= limit then
  return {0, count}
end

redis.call('ZADD', key, now, now .. '-' .. math.random())
redis.call('EXPIRE', key, window + 1)
return {1, count + 1}
```

## Tiered limits in Redis

```bash
# Store tier config
HSET tier:free limit 100 window 60
HSET tier:pro limit 1000 window 60
HSET tier:enterprise limit 10000 window 60

# Lookup at request time
EVAL "local t=redis.call('HGET',KEYS[1],'limit') local w=redis.call('HGET',KEYS[1],'window') return {t,w}" 1 tier:pro
```

## Testing

- Drive traffic at 2x limit, assert 429 rate matches expectation
- Verify RateLimit-Limit, RateLimit-Remaining, Retry-After headers
- Test burst tolerance: burst requests should succeed up to burst allowance
- Test tier switching: same key, different tier config
- Verify fault tolerance: Redis down -> fail-open or fail-closed per config

## Best practices

- Use sliding window for accuracy; token bucket for burst tolerance
- Return standard RateLimit headers (draft-ietf-httpapi-ratelimit-headers)
- Combine gateway (per-IP) + application (per-user) for defense in depth
- Store tier config in Redis for runtime updates without deploy
- Monitor: `rate(http_requests_total{status="429"}[5m])`

## Capabilities

### algorithm-design
Designs and implements rate limiting algorithms (token bucket, sliding window, fixed window, leaky bucket) with atomic Redis Lua scripts.

**Parameters:**
- `algorithm` (string): Algorithm (sliding-window, token-bucket, fixed-window, leaky-bucket)
- `key` (string): Redis key pattern
- `limit` (number): Maximum requests
- `window_or_rate` (number): Window seconds or refill rate

**Commands:**
- `redis-cli --eval sliding_window.lua rate:api:user123 1 1000 60`
- `redis-cli --eval token_bucket.lua rate:api:user123 100 1000`
- `redis-cli --eval fixed_window.lua rate:api:user123 1000 60`
- `redis-cli --eval leaky_bucket.lua rate:api:user123 100 10`

**Examples:**
- redis-cli --eval sliding_window.lua rate:api:user123 1 1000 60 $(date +%s)
- redis-cli --eval token_bucket.lua rate:api:user123 100 1000
- redis-cli EVAL "local c=redis.call(\"INCR\",KEYS[1]) if c==1 then redis.call(\"EXPIRE\",KEYS[1],ARGV[1]) end return c" 1 rate:api:user123 60

### gateway-integration
Configures rate limiting at Kong, Envoy, and nginx gateways with declarative policies.

**Parameters:**
- `gateway` (string): Gateway (kong, envoy, nginx)
- `policy` (string): Kong policy (local, redis, cluster)
- `limit` (number): Request limit per window

**Commands:**
- `deck file add-plugin kong.yaml --name=rate-limiting --config.minute=1000 --config.policy=redis --config.redis_host=redis --config.fault_tolerant=true`
- `kubectl apply -f envoy-ratelimit-config.yaml`
- `nginx -t && nginx -s reload`
- `printf "limit_req_zone \$binary_remote_addr zone=api:10m rate=100r/s;\nserver { location /api/ { limit_req zone=api burst=200 nodelay; limit_req_status 429; proxy_pass http://backend; } }\n" > /etc/nginx/conf.d/ratelimit.conf`
- `nginx -t && nginx -s reload`

**Examples:**
- deck file add-plugin kong.yaml --name=rate-limiting --config.minute=1000 --config.policy=redis --config.redis_host=redis --config.fault_tolerant=true
- kubectl apply -f ./envoy/ratelimit-filter.yaml
- printf "limit_req_zone \$binary_remote_addr zone=api:10m rate=100r/s;\nserver { location /api/ { limit_req zone=api burst=200 nodelay; limit_req_status 429; proxy_pass http://backend; } }\n" > /etc/nginx/conf.d/ratelimit.conf
- nginx -t && nginx -s reload

### tiered-limits
Implements tiered rate limits (free/pro/enterprise) with dynamic configuration.

**Parameters:**
- `tier` (string): Tier name (free, pro, enterprise)
- `limit` (number): Request limit for tier
- `window_seconds` (number): Window in seconds

**Commands:**
- `redis-cli HSET tier:free limit 100 window 60`
- `redis-cli HSET tier:pro limit 1000 window 60`
- `redis-cli HSET tier:enterprise limit 10000 window 60`
- `redis-cli HGETALL tier:pro`

**Examples:**
- redis-cli HSET tier:free limit 100 window 60
- redis-cli HSET tier:pro limit 1000 window 60
- redis-cli HGETALL tier:pro
- redis-cli EVAL "local t=redis.call(\"HGET\",KEYS[1],\"limit\") local w=redis.call(\"HGET\",KEYS[1],\"window\") return {t,w}" 1 tier:pro

### load-test-validation
Validates rate limiting behavior under load with k6, hey, and header assertions.

**Parameters:**
- `tool` (string): Load test tool (hey, k6, vegeta)
- `target_rate` (number): Target requests per second
- `expected_429_rate` (number): Expected 429 percentage

**Commands:**
- `hey -n 2000 -c 50 -H "x-api-key: test-key" http://localhost:8000/api`
- `k6 run rate-limit-test.js`

**Examples:**
- hey -n 2000 -c 50 -H "x-api-key: test-key" http://localhost:8000/api
- k6 run ./tests/rate-limit-test.js
- curl -i -H "x-api-key: test-key" http://localhost:8000/api | grep -i "ratelimit\|retry"

## References
- [Rate Limiting Patterns](https://www.figma.com/blog/rate-limiting/)
- [Redis Rate Limiting](https://redis.io/docs/latest/develop/use-cases/rate-limiting/)
- [Kong Rate Limiting Plugin](https://docs.konghq.com/hub/kong-inc/rate-limiting/)
- [Envoy Rate Limit Service](https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/rate_limit_filter)
- [Rate Limit Headers Standard](https://datatracker.ietf.org/doc/html/draft-ietf-httpapi-ratelimit-headers)

## Progressive Disclosure
This skill has many capabilities. For detailed reference:
- `references/REFERENCE.md` — full capability docs and edge cases
- `scripts/` — executable helpers (see `allowed-tools`)
- `assets/` — templates and data files
Load references on demand via relative paths, not at startup.
