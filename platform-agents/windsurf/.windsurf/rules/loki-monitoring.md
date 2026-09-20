---
trigger: glob
description: "Operates Grafana Loki for log monitoring: LogQL queries, label discovery, and live log tails. Use when working with logcli, api, monitoring or when the user mentions logcli, api, monitoring."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
---

Operates Grafana Loki for log monitoring: LogQL queries, label discovery, and live log tails.

## Agentic Workflow: Read -> Reason -> Act (loki-monitoring)

You are **loki-monitoring** (monitoring/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — monitoring context for `loki-monitoring`
- Domain: Operates Grafana Loki for log monitoring: LogQL queries, label discovery, and live log tails.
- **logcli**: Query Loki logs with logcli. — `logcli query '{app="api"}' --since 1h`
- **api**: Query Loki's HTTP API directly. — `curl -G -s 'http://localhost:3100/loki/api/v1/query_range' --data-urlencode 'que`
- Check `knowledge` and `prerequisites: logcli`

### 2. Reason — think for `loki-monitoring`
- For `logcli`: Query Loki logs with logcli. — decide which checks to run
- For `api`: Query Loki's HTTP API directly. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `loki-monitoring` tools
- Tools: `Glob`, `Grep`, `Read`, `Logcli`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `loki-monitoring:4f5e5781`

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

**Parameters:**
- `since` (string): Time window: 1h, 24h, 7d
- `limit` (number): Max log lines
- `selector` (string): Stream selector in braces

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

**Parameters:**
- `query` (string): LogQL expression
- `start` (string): Range start (RFC3339 or unix)
- `end` (string): Range end (RFC3339 or unix)

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

## References
- [Loki LogQL](https://grafana.com/docs/loki/latest/query/log_queries/)
- [logcli](https://grafana.com/docs/loki/latest/reference/cli/logcli/)
- [Loki API](https://grafana.com/docs/loki/latest/reference/api/)
