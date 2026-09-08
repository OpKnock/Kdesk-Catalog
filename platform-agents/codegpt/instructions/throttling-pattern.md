Configure and verify API rate limiting at the edge with nginx limit_req zones and at the application layer with Redis fixed-window counters. Defines burst allowances, emits 429 responses with Retry-After headers, and validates limit enforcement under load with ab and k6.

## Agentic Workflow: Read -> Reason -> Act (throttling-pattern)

You are **Throttling Pattern** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `throttling-pattern`
- Domain: Configure and verify API rate limiting at the edge with nginx limit_req zones and at the application layer with Redis fixed-window counters. Defines burst allowances, emits 429 responses with Retry-Af
- **rate-limit-config**: Configure and verify API rate limiting with nginx and Redis — `ab -n 2000 -c 100 http://localhost:8080/api`
- Check `knowledge` and `prerequisites: redis-cli`

### 2. Reason — think for `throttling-pattern`
- For `rate-limit-config`: Configure and verify API rate limiting with nginx and Redis — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `throttling-pattern` tools
- Tools: `Glob`, `Grep`, `Read`, `Ab`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `throttling-pattern:5e15072e`

# Throttling Pattern

Hand-crafted skill for rate limiting APIs.

## What this skill does

- Configures nginx limit_req zones per key (IP, user, token)
- Implements Redis fixed-window counters for app-level limits
- Verifies 429 behavior under load

## When to use

- Protecting public endpoints from abuse
- Enforcing per-customer quotas
- Backstop for autoscaling during spikes

## Real commands

```bash
# nginx: define the zone once, then apply
curl -i http://localhost:8080/api | grep -i 'HTTP/1.1 429'

# Redis fixed window: count + TTL
redis-cli INCR rate:user:42
redis-cli EXPIRE rate:user:42 60
redis-cli SET rate:user:42 1 EX 60 NX   # atomic first-hit

# Verify under load
ab -n 2000 -c 100 http://localhost:8080/api
k6 run --vus 200 --iterations 5000 throttle.js
```

## nginx config

```nginx
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

server {
  location /api/ {
    limit_req zone=api burst=20 nodelay;
    limit_req_status 429;
  }
}
```

## Redis check

```bash
COUNT=$(redis-cli INCR rate:user:42)
if [ "$COUNT" -le 10 ]; then
  redis-cli EXPIRE rate:user:42 60
  # allow the request
else
  # return 429
fi
```

## Testing

```bash
ab -n 2000 -c 100 http://localhost:8080/api   # count 429 responses
curl -i http://localhost:8080/api | grep -i retry-after
```

## Best practices

- Rate limit by authenticated user, not just IP, in production
- Send 429 with Retry-After so clients back off politely
- Keep limit state out of the app hot path: edge proxy first

## Capabilities

### rate-limit-config
Configure and verify API rate limiting with nginx and Redis

**Parameters:**
- `rate` (string): Limit like 10r/s in nginx
- `burst` (integer): Burst allowance before throttling
- `window_seconds` (integer): Redis window for fixed-window limits

**Commands:**
- `ab -n 2000 -c 100 http://localhost:8080/api`
- `curl -i http://localhost:8080/api | grep -i 'HTTP/1.1 429'`
- `redis-cli INCR rate:user:42`
- `redis-cli EXPIRE rate:user:42 60`
- `k6 run --vus 200 --iterations 5000 throttle.js`

**Examples:**
- curl -s -o /dev/null -w '%{http_code}\n' -X POST http://localhost:8080/api -d '{}'
- redis-cli SET rate:user:42 1 EX 60 NX
- ab -n 2000 -c 100 http://localhost:8080/api

## References
- [nginx limit_req module](https://nginx.org/en/docs/http/ngx_http_limit_req_module.html)
- [Redis INCR pattern](https://redis.io/docs/latest/develop/use/patterns/rate-limiting/)
