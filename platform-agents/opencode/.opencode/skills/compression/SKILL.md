---
name: "compression"
description: "Compress API responses to cut bandwidth and latency using gzip, Brotli, and zstd, with curl verification and server configuration. Use when working with compression verify, cli tools, api or when the user mentions compression verify, cli tools, api."
---

Compress API responses to cut bandwidth and latency using gzip, Brotli, and zstd, with curl verification and server configuration.

## Agentic Workflow: Read -> Reason -> Act (compression)

You are **Compression** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `compression`
- Domain: Compress API responses to cut bandwidth and latency using gzip, Brotli, and zstd, with curl verification and server configuration.
- **compression-verify**: Verify compression headers and response size on API endpoints — `curl -s -H "Accept-Encoding: gzip" -D - -o /dev/null https://httpbin.org/get | g`
- **cli-tools**: Compress and decompress payloads with gzip, brotli, and zstd — `gzip -9 -k response.json`
- Check `knowledge` and `prerequisites: brotli, gunzip, gzip, zstd`

### 2. Reason — think for `compression`
- For `compression-verify`: Verify compression headers and response size on API endpoints — decide which checks to run
- For `cli-tools`: Compress and decompress payloads with gzip, brotli, and zstd — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `compression` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Gzip` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `compression:3dd985eb`

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

**Parameters:**
- `url` (string): Endpoint to check
- `accept_encoding` (string): Accept-Encoding header value

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

**Parameters:**
- `file` (string): File to compress
- `level` (string): Compression level, e.g. 9 for gzip, 11 for brotli

**Commands:**
- `gzip -9 -k response.json`
- `gunzip -k response.json.gz`
- `brotli -9 -o response.json.br response.json`
- `zstd -19 -o response.json.zst response.json`

**Examples:**
- gzip -9 -k response.json && ls -la response.json.gz
- brotli -9 -o response.json.br response.json
- zstd -19 response.json -o response.json.zst

## References
- [MDN Content-Encoding](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Encoding)
- [Brotli GitHub](https://github.com/google/brotli)
