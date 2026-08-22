---
name: "tracing"
description: "Run the OTel Collector and route traces to backends."
type: knowledge
triggers: ["tracing", "otel-pipeline"]
---

# Tracing

Run the OTel Collector and route traces to backends.

## Instructions

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
