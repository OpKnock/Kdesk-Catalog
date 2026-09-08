Jaeger distributed tracing: running all-in-one, generating sample traces with tracegen, and querying the Jaeger API for services and traces.

## Agentic Workflow: Read -> Reason -> Act (jaeger-tracing)

You are **Jaeger Tracing** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `jaeger-tracing`
- Domain: Jaeger distributed tracing: running all-in-one, generating sample traces with tracegen, and querying the Jaeger API for services and traces.
- **jaeger-ops**: Run Jaeger locally and query traces through the API and UI. — `docker run -d --name jaeger -p 16686:16686 -p 4317:4317 -p 4318:4318 jaegertraci`
- Check `knowledge` and `prerequisites: docker`

### 2. Reason — think for `jaeger-tracing`
- For `jaeger-ops`: Run Jaeger locally and query traces through the API and UI. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `jaeger-tracing` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `jaeger-tracing:1c48a1e8`

# Jaeger Tracing

Run Jaeger and investigate distributed traces.

## What this skill does

- Starts the all-in-one Jaeger stack (collector + query UI).
- Generates sample traces with tracegen.
- Queries services and traces via the JSON API.
- Inspects span counts and durations from the CLI.

## When to use

- Verifying trace instrumentation is emitting data.
- Drilling into one slow request's span waterfall.
- Load-testing the trace pipeline itself.

## Real commands

```bash
# Run all-in-one (UI :16686, OTLP :4317/:4318)
docker run -d --name jaeger -p 16686:16686 -p 4317:4317 -p 4318:4318 \
  jaegertracing/all-in-one:1.57

# Generate sample traces
go install github.com/jaegertracing/jaeger/cmd/tracegen@latest
tracegen -service myservice -traces 50 -duration 2s

# List known services
curl 'http://localhost:16686/api/services' | jq '.data'

# Recent traces for a service
curl 'http://localhost:16686/api/traces?service=myservice&limit=10' | jq '.data[].traceID'

# Span count in the newest trace
curl 'http://localhost:16686/api/traces?service=myservice&limit=1' | jq '.data[0].spans | length'
```

## OTLP wiring for apps

```bash
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318
export OTEL_SERVICE_NAME=myservice
```

## Testing

```bash
tracegen -service myservice -traces 10 && \
  curl -s 'http://localhost:16686/api/traces?service=myservice&limit=1' | jq -e '.data[0]' > /dev/null && echo "traces flowing"
```

## Best practices

- Check sampling config before blaming missing traces (default head sampling).
- Use lookback windows matching the investigation window.
- Query by operation and tags: /api/traces?service=X&operation=Y&tags=...
- Match OTLP port choices (4317 gRPC, 4318 HTTP) to your exporter.

## Example exchange

```
User: Are traces arriving for the checkout service?
Agent: curl -s 'http://localhost:16686/api/traces?service=checkout&lookback=1h' | jq '.data | length'
```

## Capabilities

### jaeger-ops
Run Jaeger locally and query traces through the API and UI.

**Parameters:**
- `service` (string): Service name to query traces for.
- `lookback` (string): Time window, e.g. 1h, 24h.
- `limit` (integer): Max traces to return.

**Commands:**
- `docker run -d --name jaeger -p 16686:16686 -p 4317:4317 -p 4318:4318 jaegertracing/all-in-one:1.57`
- `curl 'http://localhost:16686/api/traces?service=myservice&limit=10' | jq '.data[0].traceID'`
- `curl 'http://localhost:16686/api/services' | jq '.data'`
- `go install github.com/jaegertracing/jaeger/cmd/tracegen@latest && tracegen -service myservice -traces 50`
- `curl -s 'http://localhost:16686/api/traces?service=myservice&lookback=1h' | jq '.data | length'`

**Examples:**
- tracegen -service myservice -traces 100 -duration 2s
- curl 'http://localhost:16686/api/traces?service=myservice&limit=1' | jq '.data[0].spans | length'
- docker logs jaeger | tail -20

## References
- [Jaeger Docs](https://www.jaegertracing.io/docs/latest/)
- [Jaeger API Reference](https://www.jaegertracing.io/docs/latest/apis/)
