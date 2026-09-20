# Logging Structured

Work with structured (JSON) logs: validate lines, filter by level/service with jq, and aggregate counts for dashboards.

## Instructions

# Structured Logging

Analyze and produce JSON-formatted logs with jq and Python.

## What this skill does

- Filters structured logs by level, service, and latency fields.
- Projects only the fields you need for analysis.
- Detects malformed (non-JSON) log lines.

## When to use

- Debugging slow requests from latency fields.
- Building dashboards from log aggregates.
- Enforcing structured logging in app output.

## Real commands

```bash
# Error lines with timestamp + message
jq -r 'select(.level=="error") | .ts + " " + .msg' checkout-service.log

# Project key fields
jq '. | {service, level, duration_ms}' checkout-service.log | head -20

# Slow requests as TSV
jq -r 'select(.duration_ms > 1000) | [.ts, .service, .msg] | @tsv' checkout-service.log

# Count by service
jq -s 'group_by(.service) | map({service: .[0].service, count: length})' checkout-service.log

# Error messages via grep + jq
grep '"level":"error"' checkout-service.log | jq -r '.msg'

# Validate the last line parses
tail -1 checkout-service.log | python3 -m json.tool

# Live streaming as TSV
tail -f checkout-service.log | jq -r '[.ts, .level, .msg] | @tsv'

# Find malformed lines
awk '!/^{/ {print "MALFORMED: " $0}' checkout-service.log | head
```

## Log line example

```json
{"ts":"2026-08-10T09:12:33Z","level":"error","service":"checkout","msg":"payment declined","duration_ms":450,"code":"CARD_DECLINED"}
```

## Testing

```bash
echo '{"level":"info","msg":"boot"}' | jq -e '.level=="info"' && echo valid
```

## Best practices

- Emit one JSON object per line; multiline JSON breaks pipelines.
- Always include ts, level, msg, and a correlation id field.
- Keep the schema stable; add fields, never rename existing ones.

## Capabilities

### jq-filter
Filter and project structured log fields with jq.

**Commands:**
- `jq -r 'select(.level=="error") | .ts + " " + .msg' checkout-service.log`
- `jq '. | {service, level, duration_ms}' checkout-service.log | head -20`
- `jq -r 'select(.duration_ms > 1000) | [.ts, .service, .msg] | @tsv' checkout-service.log`
- `jq -s 'group_by(.service) | map({service: .[0].service, count: length})' checkout-service.log`

**Examples:**
- jq -r 'select(.level=="error") | .ts + " " + .msg' checkout-service.log
- jq -r 'select(.duration_ms > 1000) | [.ts, .service, .msg] | @tsv' checkout-service.log
- jq -s 'group_by(.service) | map({service: .[0].service, count: length})' checkout-service.log

### validate-produce
Validate log lines parse and produce well-formed JSON logs.

**Commands:**
- `grep '"level":"error"' checkout-service.log | jq -r '.msg'`
- `tail -1 checkout-service.log | python3 -m json.tool`
- `tail -f checkout-service.log | jq -r '[.ts, .level, .msg] | @tsv'`
- `awk '!/^{/ {print "MALFORMED: " $0}' checkout-service.log | head`

**Examples:**
- grep '"level":"error"' checkout-service.log | jq -r '.msg'
- tail -1 checkout-service.log | python3 -m json.tool
- tail -f checkout-service.log | jq -r '[.ts, .level, .msg] | @tsv'