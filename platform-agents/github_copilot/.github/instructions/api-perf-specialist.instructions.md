---
applyTo: "**/*.r **/*.sh"
---

# api-perf-specialist

Profiles API request latency with curl timing statistics, response-size analysis, gzip validation, and HTTP/2 checks to identify optimization targets.

## Instructions

# API Perf Specialist

Profiling API latency with curl.

## What This Skill Does
- Measures every network phase of a request
- Compares endpoints, versions, and payload sizes
- Produces reproducible perf evidence for changes

## When to Use
- Triaging slow-endpoint reports
- Comparing a fix before/after
- Building a baseline latency map of the API

## Real Commands

```bash
curl -w "dns:%{time_namelookup}s connect:%{time_connect}s tls:%{time_appconnect}s ttfb:%{time_starttransfer}s total:%{time_total}s\n" -o /dev/null -s https://api.example.com/v1/items
```

## Reading the Phases
- time_namelookup: DNS resolution
- time_connect: TCP handshake
- time_appconnect: TLS handshake
- time_starttransfer: server time to first byte
- time_total: end-to-end including body download

## Testing
- Run 5-10 samples and take the median
- Test from multiple regions for network variance
- Compare gzip vs raw body sizes for payload wins

## Best Practices
- Always use -o /dev/null to isolate server time
- Vary the query params to catch expensive filters
- Save curl -w outputs to a CSV for trend tracking

## Capabilities

### curl-profiling
Measure DNS, TCP, TLS, TTFB, and total time per request

**Commands:**
- `curl -w "dns:%{time_namelookup}s connect:%{time_connect}s tls:%{time_appconnect}s ttfb:%{time_starttransfer}s total:%{time_total}s size:%{size_download}\n" -o /dev/null -s https://api.example.com/v1/items`
- `curl -s -o /dev/null -w '%{http_code} %{time_total} %{speed_download} bytes/s\n' http://localhost:8080/`
- `curl -s -H 'Accept-Encoding: gzip' -o /dev/null -w 'compressed:%{size_download} raw:%{size_download}_of_%{size_upload}\n' https://api.example.com/v1/items`
- `curl -sI --http2 http://localhost:8080/ | head -1`
- `curl -s -o /dev/null -w '%{time_starttransfer}\n' http://localhost:8080/v1/items?limit=1000`

**Examples:**
- curl -w with time_appconnect isolates TLS handshake cost
- TTFB over total shows server processing vs transfer time
- gzip header comparison shows compression savings

### bottleneck-identification
Compare endpoints and payloads to rank bottlenecks

**Commands:**
- `curl -s -o /dev/null -w '%{time_total}\n' http://localhost:8080/v1/items/1`
- `curl -s -o /dev/null -w '%{time_total}\n' http://localhost:8080/v2/items/1`
- `curl -s http://localhost:8080/v1/items | jq '.data | length'`
- `curl -s http://localhost:8080/v1/items | wc -c`

**Examples:**
- -cli --help
- -api --help
