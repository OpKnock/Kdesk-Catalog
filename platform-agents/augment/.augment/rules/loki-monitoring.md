---
type: agent_requested
description: "Operates Grafana Loki for log monitoring: LogQL queries, label discovery, and live log tails."
---

# loki-monitoring

Operates Grafana Loki for log monitoring: LogQL queries, label discovery, and live log tails.

## Instructions

# Loki

Search and analyze logs at scale with LogQL.

## When to Use

- Incident log search across services
- Metrics from logs (rates, error counts)
- Live debugging during rollouts

## Stream selectors

```bash
logcli query '{app="api"}' --since 1h
```

Match labels with `=`, `!=`, `=~`, `!~`.

## Pipelines

```bash
logcli query '{app="api"} |= "error"' --since 24h
logcli query '{app="checkout"} | json | status_code >= 500' --since 1h
logcli query '{app="api"} |~ "panic|fatal"' --since 6h
```

`|=` substring, `|~` regex, `| json` parses structured logs, then filter on parsed fields.

## Metric queries

```bash
logcli query 'sum(rate({app="api"} |~ "ERROR" [5m]))' --since 1h
```

Turn log lines into series for dashboards and alerts.

## Live tail

```bash
logcli live '{app="api"}'
```

## Label hygiene

- Labels = high-cardinality cost; keep to app, namespace, pod.
- Put variable data (user_id, order_id) in the log body, not labels.
- Discover what exists: `logcli labels --since 24h`.

## Best practices

- Standardize structured JSON logs for pipeline filtering.
- Embed trace_id to jump from logs to traces.
- Set retention by tier: 7d hot, 30d cold.
- Alert on rates derived from logs, never raw log spam.

## Testing

```bash
logcli query '{app="api"}' --since 10m | wc -l
```

Verify expected log flow after a release.

## Capabilities

### logcli
Query Loki logs with logcli.

**Commands:**
- `logcli query '{app="api"}' --since 1h`
- `logcli query '{app="api"} |= "error"' --since 24h --limit 100`
- `logcli labels --since 24h`
- `logcli series '{app=~".+"}' --since 1h`
- `logcli live '{app="api"}'`

**Examples:**
- logcli query '{namespace="prod"} |~ "panic|fatal"' --since 6h --limit 200
- logcli query '{app="checkout"} | json | status_code >= 500' --since 1h | head -30
- logcli labels job --since 6h

### api
Query Loki's HTTP API directly.

**Commands:**
- `curl -G -s 'http://localhost:3100/loki/api/v1/query_range' --data-urlencode 'query={app="api"}' --data-urlencode 'start=2026-08-10T08:00:00Z' --data-urlencode 'end=2026-08-10T09:00:00Z'`
- `curl -s 'http://localhost:3100/ready'`
- `curl -s 'http://localhost:3100/loki/api/v1/labels' | jq '.data'`
- `curl -G -s 'http://localhost:3100/loki/api/v1/query' --data-urlencode 'query=sum(rate({app="api"}[5m]))'`
- `curl -s 'http://localhost:3100/metrics' | grep -E 'loki_request_duration_seconds_sum' | head -3`

**Examples:**
- curl -s 'http://localhost:3100/ready' | jq
- curl -G -s 'http://localhost:3100/loki/api/v1/query_range' --data-urlencode 'query={app="api"} |= "ERROR"' --data-urlencode 'limit=50' | jq '.data.result[0].values | length'
- curl -s 'http://localhost:3100/loki/api/v1/labels' | jq -r '.data[]'