---
name: "zipkin-tracing"
description: "Run and use Zipkin for distributed tracing: start the server, emit spans over the v2 API, query traces by ID or service, and review service dependencies. Use when working with zipkin tracing, api or when the user mentions zipkin tracing, api."
license: "MIT"
compatibility: "Requires docker. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(docker:*)"
---

Run and use Zipkin for distributed tracing: start the server, emit spans over the v2 API, query traces by ID or service, and review service dependencies.

## Agentic Workflow: Read -> Reason -> Act (zipkin-tracing)

You are **Zipkin Tracing** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `zipkin-tracing`
- Domain: Run and use Zipkin for distributed tracing: start the server, emit spans over the v2 API, query traces by ID or service, and review service dependencies.
- **zipkin-tracing**: Run Zipkin, emit spans, and query traces — `docker run -d -p 9411:9411 openzipkin/zipkin`
- Check `knowledge` and `prerequisites: docker`

### 2. Reason — think for `zipkin-tracing`
- For `zipkin-tracing`: Run Zipkin, emit spans, and query traces — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `zipkin-tracing` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `zipkin-tracing:c453a2c3`

# Zipkin Tracing

## What this skill does
Run and use Zipkin for distributed tracing: start the server, emit spans over the v2 API, query traces by ID or service, and review service dependencies.

## When to use
- Tracing requests across microservices
- Measuring per-service latency
- Debugging slow end-to-end calls

## Real commands
```bash
# Start Zipkin
 docker run -d -p 9411:9411 openzipkin/zipkin

# List services
curl -s http://localhost:9411/api/v2/services | jq '.'

# Emit a span
cat > span.json <<'EOF'
[{
  "traceId": "1234567890abcdef1234567890abcdef",
  "id": "1234567890abcdef",
  "name": "get /api/users",
  "timestamp": 1700000000000000,
  "duration": 35000,
  "localEndpoint": {"serviceName": "orders-api"},
  "kind": "SERVER"
}]
EOF
curl -s -X POST http://localhost:9411/api/v2/spans -H 'Content-Type: application/json' -d @span.json

# Query traces
curl -s http://localhost:9411/api/v2/traces | jq '.[0] | {id, duration}'

# Get one trace
curl -s 'http://localhost:9411/api/v2/trace/1234567890abcdef1234567890abcdef' | jq '.[] | {id, name, duration}'

# Dependencies
curl -s http://localhost:9411/api/v2/dependencies | jq '.[0] | {parent, child, callCount}'
```

## Span JSON essentials
- traceId (128-bit hex), id (64-bit hex)
- name, kind (CLIENT/SERVER/PRODUCER/CONSUMER)
- timestamp (microseconds), duration (microseconds)
- localEndpoint.serviceName
- tags, annotations

## Best practices
- Propagate the B3 headers (x-b3-traceid, x-b3-spanid) across calls
- Use client instrumentation (brave, opentelemetry) instead of handcrafted spans in prod
- Configure sampling (e.g. 10%) at high traffic
- Set ES storage for long retention

## Testing
```bash
curl -s http://localhost:9411/api/v2/traces | jq 'length'
curl -s http://localhost:9411/api/v2/services
```

## Capabilities

### zipkin-tracing
Run Zipkin, emit spans, and query traces

**Parameters:**
- `traceId` (string): 128-bit trace identifier
- `serviceName` (string): Service name to filter spans
- `spanId` (string): Span identifier

**Commands:**
- `docker run -d -p 9411:9411 openzipkin/zipkin`
- `curl -s http://localhost:9411/api/v2/traces | jq '.[0] | {id, duration}'`
- `curl -s -X POST http://localhost:9411/api/v2/spans -H 'Content-Type: application/json' -d @span.json`
- `curl -s 'http://localhost:9411/api/v2/trace/TRACE_ID' | jq '.[] | {id, name, duration}'`
- `curl -s http://localhost:9411/api/v2/dependencies | jq '.[0] | {parent, child, callCount}'`

**Examples:**
- docker run -d -p 9411:9411 -e STORAGE_TYPE=elasticsearch -e ES_HOSTS=http://localhost:9200 openzipkin/zipkin
- curl -s http://localhost:9411/api/v2/services | jq '.'
- curl -s 'http://localhost:9411/api/v2/spans?serviceName=orders-api' | jq '.[0].name'

## References
- [Zipkin Quickstart](https://zipkin.io/pages/quickstart.html)
- [Zipkin API v2](https://zipkin.io/zipkin-api/)
