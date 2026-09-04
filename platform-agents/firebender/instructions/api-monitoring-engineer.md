# api-monitoring-engineer

Instruments APIs with OpenTelemetry for distributed tracing: auto-instrumentation, OTLP export, otel-cli command injection, and Jaeger trace inspection.

## Instructions

# API Monitoring Engineer

Distributed tracing with OpenTelemetry.

## What This Skill Does
- Instruments APIs without code changes via auto-instrumentation
- Exports spans over OTLP to Jaeger or a collector
- Traces requests across services via context propagation

## When to Use
- Diagnosing latency across service boundaries
- Building trace-based SLOs
- Migrating to vendor-neutral observability

## Real Commands

```bash
npm install @opentelemetry/sdk-node @opentelemetry/auto-instrumentations-node
node -r @opentelemetry/auto-instrumentations-node/register app.js
docker run -d --name jaeger -p 16686:16686 -p 4317:4317 jaegertracing/all-in-one:latest
```

## Configuration

```bash
export OTEL_SERVICE_NAME=my-api
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
export OTEL_TRACES_SAMPLER=parentbased_traceidratio
export OTEL_TRACES_SAMPLER_ARG=0.1
```

## Testing
- Generate traffic, then query /api/traces?service=my-api
- Confirm parent-child span relationships across services
- Validate collector endpoint health on 4318

## Best Practices
- Start with auto-instrumentation before manual spans
- Propagate W3C traceparent headers at gateways
- Sample 10-25% at high QPS, 100% on canaries

## Capabilities

### otel-instrumentation
Add OpenTelemetry tracing to a Node.js API

**Commands:**
- `npm install @opentelemetry/sdk-node @opentelemetry/auto-instrumentations-node`
- `node -r @opentelemetry/auto-instrumentations-node/register app.js`
- `curl -s http://localhost:3000/api/users -o /dev/null -w '%{http_code}\n'`
- `npm install otel-cli`
- `otel-cli exec --service my-api --name "GET /api/users" -- curl http://localhost:3000/api/users`

**Examples:**
- node -r @opentelemetry/auto-instrumentations-node/register app.js auto-instruments HTTP and DB calls
- otel-cli exec wraps any command in a trace span
- export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317 routes spans to the collector

### trace-inspection
Query traces from Jaeger after export

**Commands:**
- `docker run -d --name jaeger -p 16686:16686 -p 4317:4317 -p 4318:4318 jaegertracing/all-in-one:latest`
- `curl -s 'http://localhost:16686/api/traces?service=my-api&limit=10' | jq '.data[0].spans | length'`
- `curl -s 'http://localhost:16686/api/services' | jq '.data'`
- `curl -s 'http://localhost:4318/v1/traces' -o /dev/null -w '%{http_code}\n'`

**Examples:**
- -cli --help
- -api --help
