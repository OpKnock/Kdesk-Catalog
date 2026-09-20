---
applyTo: "**/*.json **/*.r **/*.sh"
---

# Grafana Loki

Log aggregation with Grafana Loki: query logs with logcli, filter with LogQL, and manage labels and retention.

## Instructions

# Grafana Loki

## What this skill does

Loki is a log aggregation system that indexes labels, not content, making it cheap to store high-volume logs. logcli queries logs with LogQL: label selectors, line filters, and log-range metrics.

## When to use

- Centralized log search across services
- Error rate derivation from logs (count_over_time)
- Auditing label cardinality

## Real commands

```bash
# Simple search with line filter
logcli query '{job="orders"} |= "ERROR"' --limit=50 --since=1h

# All labels in use
logcli labels --since=24h

# Series for a selector
logcli series --since=24h --match='{job="orders"}'

# Log-rate metric: errors per minute by level
logcli query 'sum by (level) (count_over_time({job="orders"}[5m]))' --since=1h

# REST API
curl -s 'http://localhost:3100/loki/api/v1/labels' | jq '.data.values'
```

## LogQL patterns

```logql
# Line filters (fast, cheap)
{job="orders"} |~ "(5\d\d|panic)"
# Parsing JSON fields
{job="orders"} | json | level = "error"
# Rate of matched lines
sum(rate({job="orders"} |= "ERROR" [5m]))
```

## Testing

```bash
# Verify a known log line is queryable
logcli query '{job="orders", service="payments"}' --since=5m | grep 'order-123'
```

## Best practices

- Use label selectors for cost, line filters for precision.
- Keep label cardinality low: no per-user or per-request labels.
- Prefer `|= "string"` over regex where possible (faster).
- Derive error rates with count_over_time instead of shipping separate metrics.
- Set retention per tenant/stream; Loki grows with cardinality, not volume.

## Capabilities

### loki-queries
Query Loki logs via logcli and inspect label usage.

**Commands:**
- `logcli query '{job="orders"} |= "ERROR"' --limit=50 --since=1h`
- `logcli labels --since=24h`
- `logcli series --since=24h --match='{job="orders"}'`
- `logcli query 'sum by (level) (count_over_time({job="orders"}[5m]))' --since=1h`
- `curl -s 'http://localhost:3100/loki/api/v1/labels' | jq '.data.values'`

**Examples:**
- logcli query '{job="orders"} |= "ERROR"' --limit=50 --since=1h
- logcli labels --since=24h
- logcli query 'sum by (level) (count_over_time({job="orders"}[5m]))' --since=1h
