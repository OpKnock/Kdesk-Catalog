---
name: "api-monitoring-engineer"
description: "Instruments APIs with OpenTelemetry for distributed tracing: auto-instrumentation, OTLP export, otel-cli command injection, and Jaeger trace inspection. Use when working with otel instrumentation, trace inspection or when the user mentions otel instrumentation, trace inspection."
license: "MIT"
compatibility: "Requires prometheus, grafana, node.js, python, new-relic, datadog. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "sre"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(docker:*) Bash(node:*) Bash(npm:*) Bash(otel-cli:*)"
---

Instruments APIs with OpenTelemetry for distributed tracing: auto-instrumentation, OTLP export, otel-cli command injection, and Jaeger trace inspection.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npm install @opentelemetry/sdk-node @opentelemetry/auto-inst`, `docker run -d --name jaeger -p 16686:16686 -p 4317:4317 -p 4`
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

**Parameters:**
- `service-name` (string): Name of the traced service in spans
- `exporter-endpoint` (string): OTLP endpoint (gRPC 4317 or HTTP 4318)
- `sample-ratio` (number): Fraction of requests to sample (0-1)

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

## References
- [OpenTelemetry Node.js Docs](https://opentelemetry.io/docs/languages/js/getting-started/nodejs/)
- [Jaeger Getting Started](https://www.jaegertracing.io/docs/latest/getting-started/)
