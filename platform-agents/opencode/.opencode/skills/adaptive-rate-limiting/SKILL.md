---
name: "adaptive-rate-limiting"
description: "Implements adaptive rate limiting with nginx limit_req zones, Redis sliding-window counters, and load-test verification with ab. Use when working with nginx limits, redis counters, api or when the user mentions nginx limits, redis counters, api."
---

Implements adaptive rate limiting with nginx limit_req zones, Redis sliding-window counters, and load-test verification with ab.

## Agentic Workflow: Read -> Reason -> Act (adaptive-rate-limiting)

You are **Adaptive Rate Limiting** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `adaptive-rate-limiting`
- Domain: Implements adaptive rate limiting with nginx limit_req zones, Redis sliding-window counters, and load-test verification with ab.
- **nginx-limits**: Configure and hot-reload nginx request-rate and connection limits. — `nginx -t`
- **redis-counters**: Use Redis fixed-window and Lua sliding-window counters to adapt limits per client. — `redis-cli INCR rate:{userId}:{window}`
- Check `knowledge` and `prerequisites: nginx, redis-cli, tail`

### 2. Reason — think for `adaptive-rate-limiting`
- For `nginx-limits`: Configure and hot-reload nginx request-rate and connection limits. — decide which checks to run
- For `redis-counters`: Use Redis fixed-window and Lua sliding-window counters to adapt limits per client. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `adaptive-rate-limiting` tools
- Tools: `Glob`, `Grep`, `Read`, `Nginx`, `Ab` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `adaptive-rate-limiting:475a7116`

# Adaptive Rate Limiting

## What this skill does

Designs rate limits that adapt to traffic: nginx limit_req zones enforce per-IP limits, Redis counters implement per-user sliding windows, and load tests verify thresholds.

## When to use

- A public API is being hammered by a single client
- Adding per-user or per-tenant quotas
- Tuning burst allowance so legitimate spikes are not rejected

## Real commands

```bash
nginx -t
nginx -s reload

# Verify configured zones
nginx -T | grep -E "limit_req|limit_conn"

# Watch rejections under load
ab -n 2000 -c 100 http://localhost:8080/api/users
```

## nginx config

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

## Redis fixed window

```bash
redis-cli INCR rate:$USER:$(date +%s)
redis-cli EXPIRE rate:$USER:$(date +%s) 60
```

Run a Lua script for atomic sliding-window decisions: `redis-cli --eval sliding_window.lua rate:$USER:60 1 100 $(date +%s)`.

## Testing

- Drive 2x the limit with ab and assert 429 share grows
- Assert normal traffic never sees 429

## Best practices

- Return Retry-After with 429 so clients back off
- Store limits in config, not code
- Combine nginx (per-IP) with Redis (per-user) for defense in depth

## Capabilities

### nginx-limits
Configure and hot-reload nginx request-rate and connection limits.

**Parameters:**
- `rate` (string): Rate in nginx syntax, e.g. 10r/s
- `burst` (number): Burst capacity above the rate
- `status_code` (number): Rejection status, e.g. 429

**Commands:**
- `nginx -t`
- `nginx -s reload`
- `nginx -T | grep limit_req`
- `ab -n 2000 -c 100 http://localhost:8080/api/users`
- `tail -f /var/log/nginx/error.log`

**Examples:**
- nginx -t && nginx -s reload
- ab -n 2000 -c 100 http://localhost:8080/api/users
- curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/api

### redis-counters
Use Redis fixed-window and Lua sliding-window counters to adapt limits per client.

**Parameters:**
- `key_pattern` (string): Redis key pattern, e.g. rate:{userId}:{window}
- `window` (number): Window size in seconds
- `limit` (number): Max requests per window

**Commands:**
- `redis-cli INCR rate:{userId}:{window}`
- `redis-cli EXPIRE rate:{userId}:{window} 60`
- `redis-cli --eval sliding_window.lua rate:{userId}:{window} 1 100 $(date +%s)`
- `redis-cli GET rate:{userId}:{window}`
- `redis-cli FLUSHDB`

**Examples:**
- redis-cli INCR rate:42:1736500000 && redis-cli EXPIRE rate:42:1736500000 60
- redis-cli --eval sliding_window.lua rate:42:1736500000 1 60 100 1736500030
- redis-cli GET rate:42:1736500000

## References
- [nginx limit_req Module](https://nginx.org/en/docs/http/ngx_http_limit_req_module.html)
- [Redis Commands](https://redis.io/docs/latest/commands/)
- [AWS Rate Limiting Strategies](https://aws.amazon.com/blogs/architecture/rate-limiting-strategies-for-scalable-apis/)
