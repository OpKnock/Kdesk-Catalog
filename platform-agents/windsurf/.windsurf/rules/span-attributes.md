---
trigger: glob
description: "Creates OpenTelemetry spans with semantic convention attributes using otel-cli. Attaches HTTP attributes (method, status_code, route), database attributes (system, statement), wraps arbitrary commands with exec, and exports via OTLP to collectors."
globs: ["**/*.py", "**/*.r", "**/*.sh", "**/*.sql"]
---

# Span Attributes

Creates OpenTelemetry spans with semantic convention attributes using otel-cli. Attaches HTTP attributes (method, status_code, route), database attributes (system, statement), wraps arbitrary commands with exec, and exports via OTLP to collectors.

## Instructions

# Span Attributes

Hand-crafted skill for attaching semantic attributes to traces with otel-cli.

## What this skill does

- Creates spans from the CLI with otel-cli span
- Attaches semantic-convention attributes for http and db spans
- Wraps arbitrary commands with otel-cli exec

## When to use

- Instrumenting shell scripts and cron jobs without code changes
- Verifying attribute names follow semantic conventions
- Building trace samples for dashboards

## Real commands

```bash
# A span with HTTP semantic attributes
otel-cli span --name 'http.request' --attrs 'http.method=GET,http.status_code=200,http.route=/v1/users'

# Database span
otel-cli span --name 'db.query' --kind client --attrs 'db.system=postgresql,db.statement=SELECT 1'

# Wrap any command; span duration equals the command
otel-cli exec --service my-svc --name 'deploy job' -- curl -s https://example.com

# Manual start/end pair for a longer operation
otel-cli span --name 'operation' --start
sleep 5
otel-cli span --name 'operation' --end

# Export via OTLP to the local collector
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318
otel-cli span --name 'boot' --attrs "host.name=$(hostname)"
```

## Attribute conventions

- http.method, http.status_code, http.route, http.url
- db.system, db.statement, db.name, cache.hit
- Custom attributes: any key=value pair is valid

## Testing

```bash
otel-cli span --name 'test' --attrs 'http.method=GET,http.status_code=200' --traceparent-file t.txt
cat t.txt
```

## Best practices

- Follow semantic conventions so tools and dashboards understand spans
- Keep attribute cardinality low: never put user IDs or URLs in span names
- Use --traceparent-file to stitch child spans into a parent trace

## Capabilities

### otel-span-attrs
Creates OpenTelemetry spans with semantic convention attributes using otel-cli. Attaches HTTP attributes (method, status_code, route), database attributes (system, statement), wraps arbitrary commands with exec, and exports via OTLP to collectors.

**Commands:**
- `otel-cli span --name "http.request" --endpoint http://localhost:4318 --attrs "http.method=GET,http.route=/api/users,http.status_code=200"`
- `otel-cli span --name "db.query" --endpoint http://localhost:4318 --attrs "db.system=postgresql,db.statement=SELECT * FROM users"`
- `otel-cli exec --name "batch.job" --endpoint http://localhost:4318 -- python etl.py`

**Examples:**
- otel-cli span --name "http.request" --endpoint http://localhost:4318 --attrs "http.method=GET,http.route=/api/users,http.status_code=200"
- otel-cli span --name "db.query" --endpoint http://localhost:4318 --attrs "db.system=postgresql,db.statement=SELECT * FROM users"
- otel-cli exec --name "batch.job" --endpoint http://localhost:4318 -- python etl.py
