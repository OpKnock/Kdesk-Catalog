---
name: "Rate Limiting"
description: "Implements API rate limiting with Redis sliding windows, token buckets, and nginx/AWS strategies to protect services from abuse."
globs: ["**/*.go", "**/*.r", "**/*.sh"]
alwaysApply: false
---

# Rate Limiting

Implements API rate limiting with Redis sliding windows, token buckets, and nginx/AWS strategies to protect services from abuse.

## Instructions

# Rate Limiting

Protect APIs from abuse with rate limits.

## When to Use

- Public APIs where abuse costs money (LLM calls, SMS, scraping)
- Login and auth endpoints against credential stuffing
- Protecting downstream services from cascading load

## Algorithms

- Fixed window: count per bucket; bursts at boundaries
- Sliding window: exact counts over rolling period
- Token bucket: steady rate with burst allowance
- Leaky bucket: smooth output regardless of input

## Redis Fixed Window

```bash
redis-cli INCR ratelimit:user:42
redis-cli EXPIRE ratelimit:user:42 60
```

## Nginx Example

```nginx
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

server {
    location /api/ {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://backend;
    }
}
```

## Commands

```bash
nginx -t
nginx -s reload

# Load test your limits
ab -n 1000 -c 50 http://localhost:8000/api
wrk -t4 -c100 -d10s http://localhost:8000/api
```

## Best Practices

- Return 429 with Retry-After so clients back off correctly
- Rate limit by identity (API key/user) and by IP as fallback
- Use Lua scripts or INCR+EXPIRE atomically; avoid TOCTOU races
- Add per-route limits, not just global ones
- Load test with ab/wrk to verify headers and behavior
- Store counters in Redis, not app memory, in multi-instance deploys

## Capabilities

### redis-rate-limit
Enforce rate limits with Redis primitives.

**Commands:**
- `redis-cli incr ratelimit:user:42`
- `redis-cli expire ratelimit:user:42 60`
- `redis-cli eval "local c=redis.call(\"incr\",KEYS[1]); if c==1 then redis.call(\"expire\",KEYS[1],ARGV[1]) end; return c" 1 ratelimit:user:42 60`
- `redis-cli ttl ratelimit:user:42`

**Examples:**
- redis-cli INCR ratelimit:user:42
- redis-cli --scan --pattern "ratelimit:*"
- redis-cli DEL ratelimit:user:42

### proxy-limiting
Configure limits at the reverse proxy layer.

**Commands:**
- `nginx -t`
- `nginx -s reload`
- `ab -n 1000 -c 50 http://localhost:8000/api`
- `curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api`

**Examples:**
- ab -n 5000 -c 100 http://localhost:8000/
- wrk -t4 -c100 -d10s http://localhost:8000/api