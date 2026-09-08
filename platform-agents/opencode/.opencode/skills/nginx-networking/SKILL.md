---
name: "nginx-networking"
description: "Engineers nginx as a reverse proxy and API gateway: location routing, headers, rate limiting, and caching layers. Use when working with proxy, gateway, networking or when the user mentions proxy, gateway, networking."
---

Engineers nginx as a reverse proxy and API gateway: location routing, headers, rate limiting, and caching layers.

## Agentic Workflow: Read -> Reason -> Act (nginx-networking)

You are **Nginx** (networking/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — networking context for `nginx-networking`
- Domain: Engineers nginx as a reverse proxy and API gateway: location routing, headers, rate limiting, and caching layers.
- **proxy**: Route and transform traffic with nginx locations. — `nginx -t -c /etc/nginx/nginx.conf`
- **gateway**: Apply rate limits, caching, and header policies. — `ab -n 200 -c 20 http://127.0.0.1/api/v1/search | grep -E 'Failed|Requests per se`
- Check `knowledge` and `prerequisites: nginx, tail`

### 2. Reason — think for `nginx-networking`
- For `proxy`: Route and transform traffic with nginx locations. — decide which checks to run
- For `gateway`: Apply rate limits, caching, and header policies. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `nginx-networking` tools
- Tools: `Glob`, `Grep`, `Read`, `Nginx`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `nginx-networking:9dea52f2`

# Nginx (Networking)

Engineer nginx as the L7 edge: proxies, limits, and cache.

## When to Use

- Reverse proxying to services with path routing
- Rate limiting public endpoints
- Caching static and API responses

## Proxy config

```nginx
upstream api_servers {
  least_conn;
  server 10.0.1.11:8080 max_fails=3 fail_timeout=10s;
  server 10.0.1.12:8080 max_fails=3 fail_timeout=10s;
}

server {
  listen 80;
  server_name api.example.com;

  location /api/v1/ {
    proxy_pass http://api_servers;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Request-Id $request_id;
  }
}
```

## Rate limiting

```nginx
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
location /api/ {
  limit_req zone=api burst=20 nodelay;
  proxy_pass http://api_servers;
}
```

## Cache headers

```nginx
location /static/ {
  alias /srv/static/;
  expires 7d;
  add_header Cache-Control 'public, max-age=604800';
}
```

## Verify behavior

```bash
nginx -t && nginx -s reload
curl -sI -H 'Host: api.example.com' http://127.0.0.1/api/v1/healthz
ab -n 200 -c 20 http://127.0.0.1/api/v1/search
```

## Best practices

- Add X-Request-Id at the edge for tracing.
- Rate limit at the edge AND at the app.
- Test 429 responses in load tests.
- Keep upstream health checks tight (5s interval).

## Testing

Run ab/hey against limited endpoints and confirm 429s beyond the burst.

## Capabilities

### proxy
Route and transform traffic with nginx locations.

**Parameters:**
- `config` (string): nginx config path
- `host` (string): Host header for vhost routing
- `url` (string): URL to probe

**Commands:**
- `nginx -t -c /etc/nginx/nginx.conf`
- `nginx -s reload`
- `nginx -T | grep -E 'server_name|proxy_pass|location'`
- `curl -sI -H 'Host: api.example.com' http://127.0.0.1/api/v1/healthz`
- `curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1/api/v1/healthz`

**Examples:**
- nginx -T | grep proxy_pass | head -20
- curl -sI http://127.0.0.1/api/ | head -8
- nginx -t && nginx -s reload

### gateway
Apply rate limits, caching, and header policies.

**Parameters:**
- `requests` (number): Load test request count
- `concurrency` (number): Load test concurrency
- `header` (string): Header to inspect in response

**Commands:**
- `ab -n 200 -c 20 http://127.0.0.1/api/v1/search | grep -E 'Failed|Requests per second'`
- `curl -s -o /dev/null -w '%{size_download}' -H 'Cache-Control: max-age=60' http://127.0.0.1/static/app.js`
- `curl -sI http://127.0.0.1/static/app.js | grep -i cache`
- `ab -n 1000 -c 50 http://127.0.0.1/api/v1/ | grep -E 'Non-2xx|Requests per second'`
- `tail -n 50 /var/log/nginx/access.log | awk '{print $9}' | sort | uniq -c`

**Examples:**
- ab -n 500 -c 50 http://127.0.0.1/api/ | grep 'Non-2xx responses'
- curl -sI -H 'Host: api.example.com' http://127.0.0.1/api/v1/healthz | grep -i x-rate
- tail -n 200 /var/log/nginx/access.log | grep ' 429 ' | wc -l

## References
- [ngx_http_proxy_module](https://nginx.org/en/docs/http/ngx_http_proxy_module.html)
- [ngx_http_limit_req_module](https://nginx.org/en/docs/http/ngx_http_limit_req_module.html)
- [ngx_http_headers_module](https://nginx.org/en/docs/http/ngx_http_headers_module.html)
