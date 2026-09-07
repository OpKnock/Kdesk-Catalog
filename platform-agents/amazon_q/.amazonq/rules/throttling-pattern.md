Configure and verify API rate limiting at the edge with nginx limit_req zones and at the application layer with Redis fixed-window counters. Defines burst allowances, emits 429 responses with Retry-After headers, and validates limit enforcement under load with ab and k6.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `ab -n 2000 -c 100 http://localhost:8080/api`
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