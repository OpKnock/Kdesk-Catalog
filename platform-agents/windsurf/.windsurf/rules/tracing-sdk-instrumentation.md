---
trigger: glob
description: "Auto-instrument Python and Node.js applications with OpenTelemetry SDKs without code changes. Installs the Python distro with all default instrumentations, bootstraps Node with HTTP and Express instrumentations, and configures exporters and service names via environment variables for consistent fleet-wide tracing. Use when working with sdk instrumentation, api or when the user mentions sdk instrumentation, api."
globs: ["**/*.py", "**/*.r", "**/*.sh"]
---

Auto-instrument Python and Node.js applications with OpenTelemetry SDKs without code changes. Installs the Python distro with all default instrumentations, bootstraps Node with HTTP and Express instrumentations, and configures exporters and service names via environment variables for consistent fleet-wide tracing.

## Agentic Workflow: Read -> Reason -> Act (tracing-sdk-instrumentation)

You are **Tracing Sdk Instrumentation** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `tracing-sdk-instrumentation`
- Domain: Auto-instrument Python and Node.js applications with OpenTelemetry SDKs without code changes. Installs the Python distro with all default instrumentations, bootstraps Node with HTTP and Express instru
- **sdk-instrumentation**: Instrument apps with OTel SDKs and auto-instrumentation — `pip install opentelemetry-distro opentelemetry-instrumentation`
- Check `knowledge` and `prerequisites: export, npm, opentelemetry-bootstrap, opentelemetry-instrument`

### 2. Reason — think for `tracing-sdk-instrumentation`
- For `sdk-instrumentation`: Instrument apps with OTel SDKs and auto-instrumentation — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `tracing-sdk-instrumentation` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Opentelemetry-bootstrap` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `tracing-sdk-instrumentation:d794ba15`

# OTel SDK Instrumentation

Hand-crafted skill for auto-instrumenting apps with OpenTelemetry SDKs.

## What this skill does

- Installs Python distro + instrumentations in one step
- Bootstraps Node SDK with http/express instrumentations
- Configures exporters and service names via env vars

## When to use

- Adding tracing to existing apps with zero code changes
- Standardizing service names and endpoints across a fleet
- Upgrading an SDK-instrumented app

## Real commands

```bash
# Python: distro + all default instrumentations
pip install opentelemetry-distro opentelemetry-instrumentation
opentelemetry-bootstrap -a install

# Run the app under instrumentation
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318
export OTEL_SERVICE_NAME=checkout
opentelemetry-instrument python app.py

# Node
npm i @opentelemetry/sdk-node @opentelemetry/instrumentation-http @opentelemetry/instrumentation-express
node -r @opentelemetry/auto-instrumentations-node/register app.js

# Inspect options
opentelemetry-instrument --help
```

## Env config

- OTEL_SERVICE_NAME: service identity in the trace
- OTEL_EXPORTER_OTLP_ENDPOINT: collector or backend
- OTEL_TRACES_SAMPLER: sampling strategy

## Testing

```bash
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318 OTEL_SERVICE_NAME=test
opentelemetry-instrument python -c 'print("traced")'
# then look for the span in Jaeger/Collector
```

## Best practices

- Set OTEL_SERVICE_NAME on every deploy; never default
- Pin distro versions for reproducible instrumentation
- Enable exporter batching via env when volume grows

## Capabilities

### sdk-instrumentation
Instrument apps with OTel SDKs and auto-instrumentation

**Parameters:**
- `service_name` (string): OTEL_SERVICE_NAME value
- `endpoint` (string): OTLP exporter endpoint
- `instrumentation` (string): Language: python or node

**Commands:**
- `pip install opentelemetry-distro opentelemetry-instrumentation`
- `opentelemetry-bootstrap -a install`
- `export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318 && export OTEL_SERVICE_NAME=checkout && opentelemetry-instrument python app.py`
- `npm i @opentelemetry/sdk-node @opentelemetry/instrumentation-http @opentelemetry/instrumentation-express`
- `opentelemetry-instrument --help`

**Examples:**
- export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318 && opentelemetry-instrument python app.py
- opentelemetry-bootstrap -a install
- node -r @opentelemetry/auto-instrumentations-node/register app.js

## References
- [Python auto-instrumentation](https://opentelemetry.io/docs/languages/python/automatic/)
- [Node SDK docs](https://opentelemetry.io/docs/languages/js/getting-started/nodejs/)
