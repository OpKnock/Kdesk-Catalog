---
applyTo: "**/*.go **/*.json **/*.r **/*.sh **/*.{yaml,yml}"
---

Deploys the OpenTelemetry stack: collector pipelines, trace generation, and metrics/logs/traces correlation.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `otelcol --config otel.yaml`, `tracegen -service checkout -trace 100 -duration 30s -otlp-en`
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
