---
name: "rate-limiting"
description: "Core rate limiting: nginx limit_req/limit_conn, 429 responses, headers, and per-IP vs per-key scoping."
---

# Rate Limiting

Core rate limiting: nginx limit_req/limit_conn, 429 responses, headers, and per-IP vs per-key scoping.

## Instructions

# Rate Limiting

Limit how often clients may hit endpoints, protecting services from abuse and overload.

## What this skill does

- Configures nginx rate and connection limits
- Handles 429s with Retry-After
- Scopes limits per IP or API key

## When to use

- Protecting endpoints from bursts
- Enforcing fair usage

## Real commands

```bash
# Apply config
nginx -t && nginx -s reload

# Verify limits
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/api
ab -n 200 -c 20 http://localhost:8080/api
curl -sI http://localhost:8080/api | grep -i retry-after
```

## nginx config

```nginx
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
limit_conn_zone $binary_remote_addr zone=conn:10m;

server {
    location /api {
        limit_req zone=api burst=20 nodelay;
        limit_conn conn 10;
        limit_req_status 429;
    }
}
```

## Scoping

- `$binary_remote_addr` - per IP
- `$http_x_api_key` - per key
- Combine with `limit_conn` for connection caps

## Best practices

- Always return 429 with Retry-After
- Test with ab/curl before going live
- Log limit hits for abuse analysis

## Capabilities

### rate-limiting-basics
Configure nginx request and connection limits with burst handling and verify 429 responses.

**Commands:**
- `nginx -t`
- `nginx -s reload`
- `curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/api`
- `ab -n 200 -c 20 http://localhost:8080/api`
- `curl -sI http://localhost:8080/api | grep -i retry-after`

**Examples:**
- nginx -t && nginx -s reload
- ab -n 300 -c 30 http://localhost:8080/api
- curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/api
