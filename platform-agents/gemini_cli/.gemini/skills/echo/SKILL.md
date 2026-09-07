---
name: "echo"
description: "HTTP echo and request debugging: sends requests to public echo services (httpbin, Postman Echo) and local containers to verify headers, methods, and payloads during API development. Use when working with http echo, api or when the user mentions http echo, api."
license: "MIT"
compatibility: "Requires docker. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(docker:*)"
---

HTTP echo and request debugging: sends requests to public echo services (httpbin, Postman Echo) and local containers to verify headers, methods, and payloads during API development.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl https://httpbin.org/get?foo=bar`
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

# Echo

## What this skill does

Echo services like httpbin and Postman Echo accept a request and return everything about it (headers, query args, body, client IP). They are the fastest way to debug clients, proxies, and webhooks.

## When to use

- Verifying what headers your client actually sends
- Testing webhook receivers against a known-good sender
- Debugging proxy rewrites or load balancer header injection

## Real commands

```bash
# Echo GET with query args
curl https://httpbin.org/get?foo=bar | jq '.args'

# Echo POST body and headers
curl -X POST https://httpbin.org/post -d '{"hello":"world"}' -H 'Content-Type: application/json' | jq '.json, .headers'

# See your client IP and origin
curl -s https://postman-echo.com/get | jq '.headers'

# Run a local echo server in Docker
 docker run -d -p 8080:80 mccutchen/go-httpbin
curl -s localhost:8080/anything | jq
```

## Common use cases

```bash
# Webhook debugging: point the sender at httpbin and capture
curl -X POST https://httpbin.org/anything/webhook -H 'Content-Type: application/json' -d '{"event":"deploy","status":"ok"}' | jq '.json'
```

## Testing

```bash
# Verify the request your SDK sends
curl -X PUT https://httpbin.org/put -H 'X-Custom: value' | jq '.headers["X-Custom"]'
```

## Best practices

- Use `-i` to see both the response headers and body.
- Prefer local go-httpbin for anything involving real payloads or credentials.
- Never send production secrets to public echo services.
- Combine with `--trace-ascii -` in curl for byte-level request dumps.

## Capabilities

### http-echo
Use echo services and local echo containers to verify how requests arrive at a server.

**Parameters:**
- `method` (string): HTTP method to test: GET, POST, PUT, DELETE
- `headers` (array): Custom headers to inspect in the echo response
- `payload` (string): JSON body echoed back by the service

**Commands:**
- `curl https://httpbin.org/get?foo=bar`
- `curl -X POST https://httpbin.org/post -d '{"hello":"world"}' -H 'Content-Type: application/json'`
- `curl -s https://postman-echo.com/get?foo=bar | jq '.args'`
- `docker run -d -p 8080:80 mccutchen/go-httpbin`
- `curl -i -X PUT https://httpbin.org/put -H 'X-Custom: value' | head -20`

**Examples:**
- curl -X POST https://httpbin.org/post -d '{"hello":"world"}' -H 'Content-Type: application/json' | jq '.json'
- curl -s https://postman-echo.com/get?foo=bar | jq '.args'
- curl -i -X PUT https://httpbin.org/put -H 'X-Custom: value' | head -20

## References
- [httpbin docs](https://httpbin.org/)
