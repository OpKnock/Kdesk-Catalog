---
type: agent_requested
description: "HTTP echo and request debugging: sends requests to public echo services (httpbin, Postman Echo) and local containers to verify headers, methods, and payloads during API development."
---

# Echo

HTTP echo and request debugging: sends requests to public echo services (httpbin, Postman Echo) and local containers to verify headers, methods, and payloads during API development.

## Instructions

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