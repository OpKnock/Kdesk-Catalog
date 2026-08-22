---
name: "curl-devtools"
description: "Makes HTTP requests with curl: headers, methods, auth, redirects, timeouts, retries, and output formatting for API debugging."
---

# curl-devtools

Makes HTTP requests with curl: headers, methods, auth, redirects, timeouts, retries, and output formatting for API debugging.

## Instructions

# curl HTTP Client

Interact with HTTP APIs and download files using curl.

## What This Skill Does

- Sends requests with methods, headers, and bodies
- Handles auth (basic, bearer, cookies)
- Follows redirects and handles TLS variations
- Measures latency and status with -w
- Retries flaky requests and enforces timeouts

## When to Use

- Debugging REST APIs from the shell
- Health checks and smoke tests in scripts
- Downloads with headers/redirects

## Real Commands

```bash
# Requests
curl -I https://example.com
curl -X POST https://api.example.com/items   -H 'Content-Type: application/json' -d '{"name":"x"}'
curl -u user:pass https://api.example.com/me
curl -H 'Authorization: Bearer token123' https://api.example.com/data
curl -L https://example.com/redirect

# Downloads
curl -O https://example.com/file.zip
curl -o file.zip https://example.com/file.zip

# Timing and resilience
curl -w '%{http_code} %{time_total}\n' -o /dev/null https://example.com
curl --retry 5 --retry-delay 2 --retry-all-errors https://example.com/flaky
curl --max-time 30 https://example.com/slow
curl -s https://api.example.com/data | jq .
```

## Best Practices

- Use -w with -o /dev/null for clean timing checks
- Always set --max-time in scripts to avoid hangs
- Use -f to fail on HTTP errors for scripting exit codes
- Never put credentials in URLs; use -u or Authorization headers
- Add -sS to suppress progress but keep errors visible in cron

## Capabilities

### http-requests
Send GET/POST/PUT requests with headers, bodies, and auth.

**Commands:**
- `curl -I http://localhost:8080`
- `curl -X POST http://localhost:8080/items -H 'Content-Type: application/json' -d '{"name":"x"}'`
- `curl -u user:pass http://localhost:8080/me`
- `curl -H 'Authorization: Bearer token123' http://localhost:8080/data`
- `curl -k https://selfsigned.local`
- `curl -L http://localhost:8080/redirect`

**Examples:**
- curl -X POST http://localhost:8080/items -d '{"name":"x"}'
- curl -H 'Authorization: Bearer token123' http://localhost:8080/data
- curl -I http://localhost:8080

### downloads-and-metrics
Download files and measure request timing and status.

**Commands:**
- `curl -o file.zip http://localhost:8080/file.zip`
- `curl -O http://localhost:8080/file.zip`
- `curl -w '%{http_code} %{time_total}\n' -o /dev/null http://localhost:8080`
- `curl --retry 5 --retry-delay 2 --retry-all-errors http://localhost:8080/flaky`
- `curl --max-time 30 http://localhost:8080/slow`
- `curl -s http://localhost:8080/api | jq .`

**Examples:**
- curl -w '%{http_code} %{time_total}\n' -o /dev/null http://localhost:8080
- curl --retry 5 --retry-delay 2 http://localhost:8080/flaky
- curl -s http://localhost:8080/api | jq .
