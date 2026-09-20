# Opentelemetry

Runs the OpenTelemetry Collector with configured receivers, processors, and exporters. Validates OTLP ingestion over HTTP/gRPC and verifies collector self-metrics.

## Instructions

# OpenTelemetry

OpenTelemetry standardizes how traces, metrics and logs are produced and shipped.

## What this skill does

- Runs the OTel Collector with a config pipeline
- Exports telemetry over OTLP
- Verifies data reaches the collector

## When to use

- Adopting observability across services
- Replacing vendor-specific SDKs

## Real commands

```bash
# Run collector
otelcol --config config.yaml
otelcol-contrib --config config.yaml

# OTLP/HTTP ingest test
curl -X POST http://localhost:4318/v1/traces -H "Content-Type: application/json" -d @trace.json
curl -X POST http://localhost:4318/v1/metrics -H "Content-Type: application/json" -d @metric.json

# Collector self-metrics
curl -s http://localhost:8888/metrics | grep otelcol
```

## config.yaml

```yaml
receivers:
  otlp:
    protocols:
      grpc:
      http:
processors:
  batch:
exporters:
  otlp:
    endpoint: jaeger:4317
    tls:
      insecure: true
service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [otlp]
```

## SDK setup (Node)

```js
const { NodeSDK } = require('@opentelemetry/sdk-node');
const sdk = new NodeSDK();
sdk.start();
```

## Best practices

- Start with traces, then metrics, then logs
- Batch processor in every pipeline
- Export to a backend before scaling collection

## Capabilities

### otel-pipelines
Run the OTel Collector, configure receivers/exporters, and verify OTLP ingestion.

**Commands:**
- `otelcol --config config.yaml`
- `otelcol-contrib --config config.yaml`
- `curl -X POST http://localhost:4318/v1/traces -H "Content-Type: application/json" -d @trace.json`
- `curl -X POST http://localhost:4318/v1/metrics -H "Content-Type: application/json" -d @metric.json`
- `curl -s http://localhost:8888/metrics | grep otelcol`

**Examples:**
- docker run -p 4317:4317 -p 4318:4318 otel/opentelemetry-collector-contrib
- curl -X POST http://localhost:4318/v1/traces -H "Content-Type: application/json" -d @trace.json
- curl -s http://localhost:8888/metrics | grep otelcol_receiver
