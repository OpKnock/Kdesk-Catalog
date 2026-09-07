---
applyTo: "**/*.r **/*.sh **/*.{yaml,yml}"
---

Send and query traces and metrics with Lightstep: OpenTelemetry collector configuration, OTLP ingestion, and Lightstep API queries.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `otelcol-contrib --config otelcol.yaml`, `curl -s -H "Authorization: Bearer $LS_TOKEN" https://api.lig`
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

# Lightstep Observability

Instrument services with OpenTelemetry and send telemetry to Lightstep.

## What this skill does

- Runs the OTel Collector exporting to Lightstep.
- Emits OTLP traces/metrics from apps and the CLI.
- Queries traces and snapshots via the public API.

## When to use

- Distributed tracing across microservices.
- SLO monitoring on trace-based latency.
- Onboarding new services to Lightstep.

## Real commands

```bash
# Run the collector
otelcol-contrib --config otelcol.yaml

# Docker collector with Lightstep export
docker run -p 4317:4317 -p 4318:4318 \
  -e OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318 \
  -e LS_ACCESS_TOKEN=$LS_TOKEN \
  otel/opentelemetry-collector-contrib:latest

# Emit a trace around a command
otel-cli exec --service checkout --name 'postgres.query' \
  -- curl -s http://localhost:8080/api

# Push protobuf OTLP directly
curl -s -X POST http://localhost:4318/v1/traces \
  -H 'Content-Type: application/x-protobuf' --data-binary @traces.pb

# Query snapshots (project SLOs)
curl -s -H "Authorization: Bearer $LS_TOKEN" \
  https://api.lightstep.com/public/v0.2/projects/{project}/snapshots

# Query traces for an operation
curl -s -H "Authorization: Bearer $LS_TOKEN" \
  "https://api.lightstep.com/public/v0.2/projects/{project}/traces?operation=checkout.checkout"
```

## otelcol.yaml example

```yaml
receivers:
  otlp:
    protocols:
      grpc:
      http:
exporters:
  otlp/lightstep:
    endpoint: ingest.lightstep.com:443
    headers:
      "lightstep-access-token": ${LS_ACCESS_TOKEN}
service:
  pipelines:
    traces:
      receivers: [otlp]
      exporters: [otlp/lightstep]
```

## Testing

```bash
curl -s http://localhost:4318/metrics   # collector is alive
```

## Best practices

- Send access tokens via env var, never hard-coded configs.
- Use the same service.name across hosts so traces join correctly.
- Configure tail sampling for high-volume services to control cost.

## Capabilities

### otel-ingest
Run the OpenTelemetry Collector and emit OTLP telemetry.

**Parameters:**
- `config` (string): OpenTelemetry Collector config file.
- `access_token` (string): Lightstep access token (LS_ACCESS_TOKEN).

**Commands:**
- `otelcol-contrib --config otelcol.yaml`
- `docker run -p 4317:4317 -p 4318:4318 -e OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318 -e LS_ACCESS_TOKEN=$LS_TOKEN otel/opentelemetry-collector-contrib:latest`
- `curl -s -X POST http://localhost:4318/v1/traces -H 'Content-Type: application/x-protobuf' --data-binary @traces.pb`
- `otel-cli exec --service checkout --name 'postgres.query' -- curl -s http://localhost:8080/api`

**Examples:**
- otelcol-contrib --config otelcol.yaml
- curl -s -X POST http://localhost:4318/v1/traces -H 'Content-Type: application/x-protobuf' --data-binary @traces.pb
- otel-cli exec --service checkout --name 'postgres.query' -- curl -s http://localhost:8080/api

### lightstep-api
Query Lightstep via the public API and the built-in CLI/curl.

**Parameters:**
- `project` (string): Lightstep project name.
- `operation` (string): Trace operation filter.

**Commands:**
- `curl -s -H "Authorization: Bearer $LS_TOKEN" https://api.lightstep.com/public/v0.2/projects/{project}/snapshots`
- `curl -s -H "Authorization: Bearer $LS_TOKEN" "https://api.lightstep.com/public/v0.2/projects/{project}/traces?operation=checkout.checkout"`
- `curl -s http://localhost:4318/metrics`
- `curl -s -X POST http://localhost:4318/v1/metrics -H 'Content-Type: application/x-protobuf' --data-binary @metrics.pb`

**Examples:**
- curl -s -H "Authorization: Bearer $LS_TOKEN" https://api.lightstep.com/public/v0.2/projects/{project}/snapshots
- curl -s http://localhost:4318/metrics
- curl -s -H "Authorization: Bearer $LS_TOKEN" "https://api.lightstep.com/public/v0.2/projects/{project}/traces?operation=checkout.checkout"

## References
- [Lightstep Docs](https://docs.lightstep.com/)
- [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/)
