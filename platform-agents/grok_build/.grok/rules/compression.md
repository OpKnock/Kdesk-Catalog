Compress API responses to cut bandwidth and latency using gzip, Brotli, and zstd, with curl verification and server configuration.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -s -H "Accept-Encoding: gzip" -D - -o /dev/null https:/`, `gzip -9 -k response.json`
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