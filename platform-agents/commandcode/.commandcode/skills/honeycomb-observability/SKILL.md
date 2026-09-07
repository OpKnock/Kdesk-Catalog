---
name: "honeycomb-observability"
description: "Manage Honeycomb datasets, execute ad-hoc queries, and ship events via the CLI. Covers OTLP exporter wiring, dataset operations, and query workflows for production observability. Use when working with honeycomb ops, api or when the user mentions honeycomb ops, api."
license: "MIT"
compatibility: "Requires honeycomb."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(honeycomb:*)"
---

Manage Honeycomb datasets, execute ad-hoc queries, and ship events via the CLI. Covers OTLP exporter wiring, dataset operations, and query workflows for production observability.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `honeycomb auth login`
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
