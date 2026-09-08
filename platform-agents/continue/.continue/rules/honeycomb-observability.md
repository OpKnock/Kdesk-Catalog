---
name: "Honeycomb Observability"
description: "Manage Honeycomb datasets, execute ad-hoc queries, and ship events via the CLI. Covers OTLP exporter wiring, dataset operations, and query workflows for production observability. Use when working with honeycomb ops, api or when the user mentions honeycomb ops, api."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
alwaysApply: false
---

Manage Honeycomb datasets, execute ad-hoc queries, and ship events via the CLI. Covers OTLP exporter wiring, dataset operations, and query workflows for production observability.

## Agentic Workflow: Read -> Reason -> Act (honeycomb-observability)

You are **Honeycomb Observability** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `honeycomb-observability`
- Domain: Manage Honeycomb datasets, execute ad-hoc queries, and ship events via the CLI. Covers OTLP exporter wiring, dataset operations, and query workflows for production observability.
- **honeycomb-ops**: Manage datasets, run queries, and send events with the Honeycomb CLI. — `honeycomb auth login`
- Check `knowledge` and `prerequisites: honeycomb`

### 2. Reason — think for `honeycomb-observability`
- For `honeycomb-ops`: Manage datasets, run queries, and send events with the Honeycomb CLI. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `honeycomb-observability` tools
- Tools: `Glob`, `Grep`, `Read`, `Honeycomb` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `honeycomb-observability:533647a0`

# Honeycomb Observability

Query and instrument with Honeycomb from the CLI.

## What this skill does

- Logs into Honeycomb from the CLI and lists datasets.
- Runs ad-hoc queries against live data (time ranges, breakdowns, calculations).
- Posts raw events for testing ingestion.
- Wires OpenTelemetry exporters to Honeycomb.

## When to use

- Investigating a latency spike with a quick query.
- Verifying a service is sending telemetry to the right dataset.
- Bootstrapping OTLP config for new services.

## Real commands

```bash
# Authenticate
honeycomb auth login

# List datasets
honeycomb dataset list

# Run a query: count of events per app.name in the last hour
honeycomb query run --dataset myservice '{
  "time_range": 3600,
  "breakdowns": ["app.name"],
  "calculations": [{"op": "COUNT"}]
}'

# Post a test event
honeycomb events post --dataset myservice --json '{"name":"GET /api","duration_ms":42}'
```

## OTLP wiring

```bash
export OTEL_EXPORTER_OTLP_ENDPOINT=https://api.honeycomb.io
export OTEL_EXPORTER_OTLP_HEADERS="x-honeycomb-team=$HONEYCOMB_API_KEY"
export OTEL_SERVICE_NAME=myservice
```

## Testing

```bash
honeycomb events post --dataset myservice --json '{"check":"pipeline"}' \
  && honeycomb query run --dataset myservice '{"time_range": 300, "calculations": [{"op": "COUNT"}]}'
```

## Best practices

- Set a meaningful service name for every service so breakdowns work.
- Keep dataset names consistent with service names.
- Use derived columns for slow queries instead of heavy breakdowns.
- Store the API key in the honeycomb CLI keyring, not in code.

## Example exchange

```
User: Which app version is generating 500s right now?
Agent: honeycomb query run --dataset myservice '{"time_range": 900, "breakdowns": ["app.version"], "calculations": [{"op":"COUNT","field":"*"}]}'
```

## Capabilities

### honeycomb-ops
Manage datasets, run queries, and send events with the Honeycomb CLI.

**Parameters:**
- `dataset` (string): Honeycomb dataset name.
- `time_range` (integer): Query window in seconds.
- `api_key` (string): Honeycomb API key (or OTEL header).

**Commands:**
- `honeycomb auth login`
- `honeycomb dataset list`
- `honeycomb query run --dataset myservice '{"time_range": 3600, "breakdowns": ["app.name"], "calculations": [{"op": "COUNT"}]}'`
- `honeycomb events post --dataset myservice --json '{"name":"GET /api","duration_ms":42}'`
- `honeycomb --version`

**Examples:**
- honeycomb query run --dataset myservice '{"time_range": 900, "order": [{"op": "COUNT"}]}'
- honeycomb dataset create frontend
- export OTEL_EXPORTER_OTLP_ENDPOINT=https://api.honeycomb.io

## References
- [Honeycomb Docs](https://docs.honeycomb.io/)
- [Honeycomb CLI](https://docs.honeycomb.io/working-with-your-data/honeycomb-cli/)