---
applyTo: "**/*.py **/*.r **/*.sh"
---

# Tracing Sdk Instrumentation

Auto-instrument Python and Node.js applications with OpenTelemetry SDKs without code changes. Installs the Python distro with all default instrumentations, bootstraps Node with HTTP and Express instrumentations, and configures exporters and service names via environment variables for consistent fleet-wide tracing.

## Instructions

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
