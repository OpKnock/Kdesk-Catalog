---
name: "Tracing"
description: "Run the OTel Collector and route traces to backends. Use when working with otel pipeline, api or when the user mentions otel pipeline, api."
globs: ["**/*.json", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
alwaysApply: false
---

Run the OTel Collector and route traces to backends.

## Agentic Workflow: Read -> Reason -> Act (tracing)

You are **Tracing** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `tracing`
- Domain: Run the OTel Collector and route traces to backends.
- **otel-pipeline**: Run the OTel Collector and route traces to backends — `otelcol-contrib --config otel-collector.yaml`
- Check `knowledge` and `prerequisites: docker, otelcol-contrib`

### 2. Reason — think for `tracing`
- For `otel-pipeline`: Run the OTel Collector and route traces to backends — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `tracing` tools
- Tools: `Glob`, `Grep`, `Read`, `Otelcol-contrib`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `tracing:59485c4a`

# Tracing

Hand-crafted skill for running a complete tracing pipeline.

## What this skill does

- Boots the OpenTelemetry Collector with a full pipeline
- Ingests OTLP traces and ships them to backends
- Runs Jaeger and Zipkin backends locally for debugging

## When to use

- Standing up tracing from scratch (SDK -> collector -> backend)
- Verifying collectors accept and export traces
- Local reproduction of a distributed request

## Real commands

```bash
# Run the collector
otelcol-contrib --config otel-collector.yaml

# Ingest a minimal trace (validates the OTLP endpoint)
curl -X POST localhost:4318/v1/traces -H 'Content-Type: application/json' -d '{"resourceSpans":[]}'

# Backends
docker run -d -p 16686:16686 jaegertracing/all-in-one
docker run -d -p 9411:9411 openzipkin/zipkin

# Zipkin ingest check
curl -X POST -H 'Content-Type: application/json' localhost:9411/api/v2/spans -d '[]'
```

## Collector config

```yaml
receivers:
  otlp:
    protocols:
      http:
        endpoint: 0.0.0.0:4318
processors:
  batch:
exporters:
  jaeger:
    endpoint: localhost:14250
    tls:
      insecure: true
service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [jaeger]
```

## Testing

```bash
curl -X POST localhost:4318/v1/traces -H 'Content-Type: application/json' -d '{"resourceSpans":[]}'
curl -s localhost:16686/api/services | jq '.data'
```

## Best practices

- Always add a batch processor before exporters
- Buffer to a local file or Kafka when backends are flaky
- Set sampling before the collector, not after

## Capabilities

### otel-pipeline
Run the OTel Collector and route traces to backends

**Parameters:**
- `config` (string): Collector config file path
- `backend` (string): jaeger or zipkin
- `endpoint` (string): OTLP endpoint, e.g. localhost:4318

**Commands:**
- `otelcol-contrib --config otel-collector.yaml`
- `curl -X POST localhost:4318/v1/traces -H 'Content-Type: application/json' -d '{"resourceSpans":[]}'`
- `docker run -d -p 16686:16686 jaegertracing/all-in-one`
- `docker run -d -p 9411:9411 openzipkin/zipkin`
- `curl -X POST -H 'Content-Type: application/json' localhost:9411/api/v2/spans -d '[]'`

**Examples:**
- otelcol-contrib --config otel-collector.yaml
- docker run -d -p 16686:16686 jaegertracing/all-in-one
- curl -X POST localhost:4318/v1/traces -H 'Content-Type: application/json' -d '{"resourceSpans":[]}'

## References
- [OpenTelemetry Collector docs](https://opentelemetry.io/docs/collector/)
- [Jaeger docs](https://www.jaegertracing.io/docs/)