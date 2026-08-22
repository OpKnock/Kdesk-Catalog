---
type: agent_requested
description: "Compress API responses to cut bandwidth and latency using gzip, Brotli, and zstd, with curl verification and server configuration."
---

# Compression

Compress API responses to cut bandwidth and latency using gzip, Brotli, and zstd, with curl verification and server configuration.

## Instructions

# Compression

Compress API responses to cut bandwidth and latency.

## When to Use

- JSON-heavy APIs with large payloads
- Mobile clients on slow networks
- Reducing egress cost and p95 transfer time

## Encode Selection

Prefer Brotli (br) for text-heavy JSON, then gzip, then zstd; always set Vary: Accept-Encoding.

## Verify Endpoints

```bash
curl -s -H "Accept-Encoding: gzip" -D - -o /dev/null https://httpbin.org/get | grep -i content-encoding
curl -s -o /dev/null -w "compressed: %{size_download} bytes\n" -H "Accept-Encoding: gzip, br" https://httpbin.org/get
curl --compressed -s https://httpbin.org/get | wc -c
```

Compare with no encoding:

```bash
curl -s -o /dev/null -w "uncompressed: %{size_download} bytes\n" https://httpbin.org/get
```

## CLI Tools

```bash
gzip -9 -k response.json
brotli -9 -o response.json.br response.json
zstd -19 -o response.json.zst response.json
```

## Server Middleware (Express)

```bash
npm install compression
```

```js
const compression = require('compression');
app.use(compression({ threshold: 1024 }));
```

## Testing

```bash
curl -s -o /dev/null -w "gzip: %{size_download}\n" -H "Accept-Encoding: gzip" https://httpbin.org/get
curl -s -o /dev/null -w "br: %{size_download}\n" -H "Accept-Encoding: br" https://httpbin.org/get
```

## Best Practices

- Compress above a small threshold (1KB) only
- Do not compress already-compressed media (images, video)
- Set Vary: Accept-Encoding on cached responses
- Never send both Content-Length and chunked encoding
- Use brotli when clients support it
- Keep compression CPU cost off the hot path with CDN caching

## Capabilities

### compression-verify
Verify compression headers and response size on API endpoints

**Commands:**
- `curl -s -H "Accept-Encoding: gzip" -D - -o /dev/null https://httpbin.org/get | grep -i content-encoding`
- `curl -s -H "Accept-Encoding: gzip, br" -o /dev/null -w "%{size_download} bytes\n" https://httpbin.org/get`
- `curl -s -o /dev/null -w "%{http_code}\n" -H "Accept-Encoding: gzip" https://httpbin.org/get`
- `curl --compressed -s https://httpbin.org/get | wc -c`

**Examples:**
- curl -s -H "Accept-Encoding: gzip, br" -D - -o /dev/null https://httpbin.org/get | grep -i 'content-encoding'
- curl -s -o /dev/null -w "%{size_download}\n" -H "Accept-Encoding: gzip" https://httpbin.org/get
- curl -s -o /dev/null -w "%{size_download}\n" -H "Accept-Encoding: gzip, br, zstd" https://httpbin.org/get

### cli-tools
Compress and decompress payloads with gzip, brotli, and zstd

**Commands:**
- `gzip -9 -k response.json`
- `gunzip -k response.json.gz`
- `brotli -9 -o response.json.br response.json`
- `zstd -19 -o response.json.zst response.json`

**Examples:**
- gzip -9 -k response.json && ls -la response.json.gz
- brotli -9 -o response.json.br response.json
- zstd -19 response.json -o response.json.zst