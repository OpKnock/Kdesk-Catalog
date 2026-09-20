---
name: "Zipkin Tracing"
description: "Run and use Zipkin for distributed tracing: start the server, emit spans over the v2 API, query traces by ID or service, and review service dependencies."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
alwaysApply: false
---

# Zipkin Tracing

Run and use Zipkin for distributed tracing: start the server, emit spans over the v2 API, query traces by ID or service, and review service dependencies.

## Instructions

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