---
name: "observability-stack-engineer"
description: "Deploys the OpenTelemetry stack: collector pipelines, trace generation, and metrics/logs/traces correlation. Use when working with collector, tracegen or when the user mentions collector, tracegen."
---

Deploys the OpenTelemetry stack: collector pipelines, trace generation, and metrics/logs/traces correlation.

## Agentic Workflow: Read -> Reason -> Act (observability-stack-engineer)

You are **observability-stack-engineer** (infrastructure) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — infrastructure context for `observability-stack-engineer`
- Domain: Deploys the OpenTelemetry stack: collector pipelines, trace generation, and metrics/logs/traces correlation.
- **collector**: Run and validate OpenTelemetry collectors. — `otelcol --config otel.yaml`
- **tracegen**: Generate load and verify the pipeline. — `tracegen -service checkout -trace 100 -duration 30s -otlp-endpoint localhost:431`
- Check `knowledge` and `prerequisites: prometheus, grafana, opentelemetry-collector, jaeger`

### 2. Reason — think for `observability-stack-engineer`
- For `collector`: Run and validate OpenTelemetry collectors. — decide which checks to run
- For `tracegen`: Generate load and verify the pipeline. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `observability-stack-engineer` tools
- Tools: `Glob`, `Grep`, `Read`, `Otelcol`, `Otelcol-contrib` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `observability-stack-engineer:dc8d3984`

# Observability Stack

Build one pipeline for metrics, logs, and traces.

## When to Use

- Standing up the telemetry backbone
- Migrating agents to OTLP
- Correlating logs, metrics, and traces

## Collector config

```yaml
receivers:
  otlp:
    protocols: { grpc: { endpoint: 0.0.0.0:4317 }, http: { endpoint: 0.0.0.0:4318 } }
processors:
  batch: {}
exporters:
  otlphttp/prometheus:
    endpoint: http://prometheus:9090/api/v1/otlp
  otlp/loki:
    endpoint: http://loki:3100/otlp
  otlp/tempo:
    endpoint: http://tempo:4317
    tls: { insecure: true }
service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [otlp/tempo]
    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [otlphttp/prometheus]
    logs:
      receivers: [otlp]
      processors: [batch]
      exporters: [otlp/loki]
```

## Validate and run

```bash
otelcol --config otel.yaml --validate
otelcol --config otel.yaml
curl -s http://localhost:13133/health
```

## Verify with load

```bash
tracegen -service checkout -trace 100 -duration 30s
otel-cli exec --service demo -- curl -s http://localhost:8080/healthz
```

## Golden signals

- Traces: latency per operation, error spans.
- Metrics: RED/USE dashboards.
- Logs: correlation via trace_id.

## Best practices

- Instrument with SDKs; collectors are for transport, not magic.
- Batch and queue exporters to avoid data loss.
- Set sampling policy centrally (head/tail).
- Validate configs in CI before rollout.

## Testing

```bash
otelcol --config otel.yaml --validate
tracegen -service checkout -trace 50 -duration 15s
curl -G -s 'http://localhost:3200/api/search' --data-urlencode 'tags=service.name=checkout'
```

Traces must appear in Tempo within seconds.

## Capabilities

### collector
Run and validate OpenTelemetry collectors.

**Parameters:**
- `config` (string): Collector config file
- `validate` (string): Validate config and exit
- `metrics-port` (number): Collector self-metrics port

**Commands:**
- `otelcol --config otel.yaml`
- `otelcol --config otel.yaml --validate`
- `otelcol-contrib --config otel.yaml`
- `curl -s http://localhost:13133/health | jq`
- `docker run -v $(pwd)/otel.yaml:/otel.yaml otel/opentelemetry-collector-contrib --config /otel.yaml`

**Examples:**
- otelcol --config otel.yaml --validate --feature-gates=exporter.otlp.retry.enabled
- curl -s http://localhost:8888/metrics | head -20
- docker run --rm -p 4317:4317 -p 13133:13133 otel/opentelemetry-collector --config otel.yaml

### tracegen
Generate load and verify the pipeline.

**Parameters:**
- `service` (string): Service name for generated traces
- `trace` (number): Traces per second
- `duration` (string): Generation duration

**Commands:**
- `tracegen -service checkout -trace 100 -duration 30s -otlp-endpoint localhost:4317`
- `tracegen -service checkout -trace 100 -duration 30s`
- `otel-cli exec --service demo -- curl -s http://localhost:8080/healthz`
- `curl -s -X POST -H 'Content-Type: application/json' -d '{"resourceSpans":[{"resource":{}}]}' http://localhost:4318/v1/traces`
- `curl -G -s 'http://localhost:3200/api/search' --data-urlencode 'tags=service.name=checkout' | jq '.traces | length'`

**Examples:**
- tracegen -service checkout -trace 50 -duration 15s -otlp-attributes service.version=3.2.0
- otel-cli exec --service demo -- sleep 1
- curl -G -s 'http://localhost:3200/api/search' --data-urlencode 'tags=service.name=demo' --data-urlencode 'limit=5' | jq '.traces | length'

## References
- [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/)
- [otel-cli](https://github.com/equinix-labs/otel-cli)
- [tracegen](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/cmd/tracegen)
