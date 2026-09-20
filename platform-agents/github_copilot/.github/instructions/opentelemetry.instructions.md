---
applyTo: "**/*.json **/*.r **/*.sh **/*.{yaml,yml}"
---

Runs the OpenTelemetry Collector with configured receivers, processors, and exporters. Validates OTLP ingestion over HTTP/gRPC and verifies collector self-metrics.

## Agentic Workflow: Read -> Reason -> Act (opentelemetry)

You are **Opentelemetry** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `opentelemetry`
- Domain: Runs the OpenTelemetry Collector with configured receivers, processors, and exporters. Validates OTLP ingestion over HTTP/gRPC and verifies collector self-metrics.
- **otel-pipelines**: Run the OTel Collector, configure receivers/exporters, and verify OTLP ingestion. — `otelcol --config config.yaml`
- Check `knowledge` and `prerequisites: otelcol, otelcol-contrib`

### 2. Reason — think for `opentelemetry`
- For `otel-pipelines`: Run the OTel Collector, configure receivers/exporters, and verify OTLP ingestion. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `opentelemetry` tools
- Tools: `Glob`, `Grep`, `Read`, `Otelcol`, `Otelcol-contrib` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `opentelemetry:fa9c50d3`

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

**Parameters:**
- `config` (string): Collector config file path
- `protocol` (string): otlp/grpc (4317) or otlp/http (4318)
- `exporter` (string): Destination: otlp, prometheus, jaeger, loki

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

## References
- [OpenTelemetry Docs](https://opentelemetry.io/docs/)
- [Collector Configuration](https://opentelemetry.io/docs/collector/configuration/)
