---
type: agent_requested
description: "Infrastructure failover strategies: nginx upstream server groups with backup servers for automatic failover, DNS round-robin and failover records for multi-region routing, and CDN origin switching so static content remains available during outages."
---

# Fallback

Infrastructure failover strategies: nginx upstream server groups with backup servers for automatic failover, DNS round-robin and failover records for multi-region routing, and CDN origin switching so static content remains available during outages.

## Instructions

# Fallback

## What this skill does

Infrastructure-level failover routes traffic away from dead endpoints: nginx upstream server groups with backup servers, DNS-based multi-region routing, and CDN origin switching so content stays available during outages.

## When to use

- A single backend host fails and the gateway returns 502
- Adding multi-AZ or multi-region failover
- Verifying which origin a CDN currently serves

## Real commands

```bash
# Validate and reload nginx
nginx -t -c /etc/nginx/nginx.conf
nginx -s reload

# What does DNS actually return?
dig +short httpbin.org A

# Where is the CDN serving from?
curl -sI https://httpbin.org | grep -iE 'HTTP|x-cache'

# Health timing
curl -s -o /dev/null -w '%{http_code} %{time_total}s\n' https://httpbin.org/get
```

## nginx upstream failover example

```nginx
upstream api {
  server api-1.internal:8080 max_fails=3 fail_timeout=30s;
  server api-2.internal:8080 max_fails=3 fail_timeout=30s;
  server api-backup.internal:8080 backup;
}

server {
  listen 443 ssl;
  location / {
    proxy_pass http://api;
    proxy_next_upstream error timeout http_502 http_503;
  }
}
```

## DNS fallback

```dns
api.internal. 300 IN A 10.0.1.10   ; primary
api.internal. 300 IN A 10.0.2.10   ; failover region
```

## Testing failover

```bash
# Stop primary, confirm the gateway still answers
systemctl stop api-1
sleep 5
curl -s -o /dev/null -w '%{http_code}' https://api.internal/health
# expect 200 from api-2 or the backup
```

## Best practices

- Use `backup` servers for cheap disaster-standby instead of parallel traffic.
- Set `proxy_next_upstream` to the exact conditions that justify failover.
- Keep DNS TTL low (60-300s) for fast failover, but not so low it thrashes.
- Monitor 502/503 rates and upstream health checks, not just DNS.

## Capabilities

### infra-failover
Configure nginx upstream failover, test DNS fallback, and verify origin fallback behavior.

**Commands:**
- `nginx -t -c /etc/nginx/nginx.conf`
- `nginx -s reload`
- `curl -sI https://httpbin.org | grep -iE 'HTTP|x-cache'`
- `dig +short httpbin.org A`
- `dig +short httpbin.org @8.8.8.8 | head -3`
- `curl -s -o /dev/null -w '%{http_code} %{time_total}s\n' https://httpbin.org/get`

**Examples:**
- nginx -t -c /etc/nginx/nginx.conf && nginx -s reload
- dig +short httpbin.org A
- curl -sI https://httpbin.org | grep -iE 'HTTP|x-cache'