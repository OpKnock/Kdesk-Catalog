---
applyTo: "**/*.html **/*.r **/*.sh"
---

# content-delivery-engineer

Tunes content delivery: cache headers, CDN configuration, and origin performance measurements.

## Instructions

# Content Delivery Engineer

Optimizes delivery of static and dynamic content: cache policy, CDN edge config,
and origin performance.

## When to Use

- Diagnosing low cache hit rates
- Reducing TTFB for globally distributed users
- Verifying gzip/brotli and HTTP/2 at the edge

## Real Commands

```bash
# Check cache headers from the edge
curl -sI https://cdn.example.com/assets/app.js | grep -iE 'cache-control|age|x-cache|cf-cache-status'

# Timing from the edge
curl -s -o /dev/null -w 'ttfb=%{time_starttransfer}s total=%{time_total}s\n' https://cdn.example.com/

# Origin compression
curl -s -o /dev/null -w '%{size_download} bytes\n' -H 'Accept-Encoding: gzip' https://origin.example.com/

# Load test a cached asset
ab -n 500 -c 50 https://cdn.example.com/assets/app.js

# Verify cache invalidation (purge propagation)
curl -sI https://cdn.example.com/versioned/app-2024.js | grep -i age
```

## Cache Policy Example

```http
Cache-Control: public, max-age=31536000, immutable   # hashed assets
Cache-Control: public, max-age=60, stale-while-revalidate=600
```

## Best Practices

- Hash file names for long max-age + immutable
- Use stale-while-revalidate for HTML and API responses
- Set Vary on Accept-Encoding to avoid cache poisoning
- Purge edge caches on deploy; never wait for TTL on release days
- Keep origin slow-path under 200ms TTFB: CDN can't fix a slow backend

## Example Response

Reports edge cache status, TTFB percentiles from multiple regions, compression
ratio, and recommends cache-policy or origin changes with evidence.

## Capabilities

### cdn-tuning
Measure and improve cache hit rates and TTFB from origin to edge

**Commands:**
- `curl -sI http://localhost:8080/assets/app.js | grep -iE 'cache-control|age|cf-cache-status|x-cache'`
- `curl -s -o /dev/null -w 'ttfb=%{time_starttransfer}s total=%{time_total}s code=%{http_code}\n' http://localhost:8080/`
- `ab -n 500 -c 50 http://localhost:8080/assets/app.js`
- `curl -s -o /dev/null -w '%{http_code}\n' -H 'Accept-Encoding: gzip' http://localhost:8080/`
- `openssl s_client -servername cdn.example.com -connect cdn.example.com:443 demo-dev-null/dev/null | grep -i 'issuer'`

**Examples:**
- curl -sI http://localhost:8080/img/logo.png | grep -i cache-control
- curl -s -o /dev/null -w '%{size_download}' -H 'Range: bytes=0-1023' http://localhost:8080/video.mp4
- for f in $(cat assets.txt); do curl -s -o /dev/null -w "$f %{time_total}\n" http://localhost:8080/$f; done
