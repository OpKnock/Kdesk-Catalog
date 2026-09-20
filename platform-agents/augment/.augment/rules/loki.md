---
type: agent_requested
description: "Run and query Grafana Loki: single-binary server, LogQL queries with logcli, promtail shipping, and label-based filtering."
---

# Loki

Run and query Grafana Loki: single-binary server, LogQL queries with logcli, promtail shipping, and label-based filtering.

## Instructions

# Grafana Loki

Query and operate Grafana Loki, the log aggregation system.

## What this skill does

- Starts a local Loki instance (single binary / Docker).
- Ships logs with promtail and queries with logcli.
- Runs LogQL stream and metric queries.

## When to use

- Cheap log search without full-text indexing overhead.
- Alerting on log rates (error rate, panic count).
- Consolidating logs from Kubernetes clusters.

## Real commands

```bash
# Start Loki
docker run -d --name loki -p 3100:3100 grafana/loki:3.0.0

# Readiness
curl -s http://localhost:3100/ready

# Ship logs with promtail
docker run -d --name promtail -v /var/log:/var/log:ro \
  -v $PWD/promtail-config.yml:/etc/promtail/config.yml \
  grafana/promtail:3.0.0 -config.file=/etc/promtail/config.yml

# logcli: recent lines for a label set
logcli query '{app="checkout"}' --limit 50

# logcli: filter for 500s in the last hour
logcli query '{app="nginx"} |= "500"' --from="1h ago" --limit 20

# logcli: rate query (lines/sec)
logcli query rate('{app="checkout"}[5m]') --from="1h ago"

# logcli: list label values
logcli labels app

# HTTP query API
curl -G -s http://localhost:3100/loki/api/v1/query_range \
  --data-urlencode 'query={app="checkout"}' --data-urlencode 'limit=10'
```

## promtail config example

```yaml
server:
  http_listen_port: 9080
clients:
  - url: http://localhost:3100/loki/api/v1/push
scrape_configs:
  - job_name: app
    static_configs:
      - targets: [localhost]
        labels:
          job: app
          __path__: /var/log/app/*.log
```

## Testing

```bash
logcli query '{job="app"}' --limit 5
```

## Best practices

- Design labels carefully; cardinality explodes storage and query cost.
- Use LogQL metric queries (rate/count_over_time) for alerting.
- Keep log lines parseable; combine with a parser for structured fields.

## Capabilities

### loki-server
Start a local Loki server and check readiness.

**Commands:**
- `docker run -d --name loki -p 3100:3100 grafana/loki:3.0.0`
- `curl -s http://localhost:3100/ready`
- `curl -s http://localhost:3100/metrics | grep loki_logs_ingested_bytes_total | head -3`
- `docker logs loki --tail=20`

**Examples:**
- docker run -d --name loki -p 3100:3100 grafana/loki:3.0.0
- curl -s http://localhost:3100/ready
- curl -s http://localhost:3100/metrics | grep loki_logs_ingested_bytes_total | head -3

### logcli-query
Query logs with logcli and the HTTP query API.

**Commands:**
- `logcli query '{app="checkout"}' --limit 50`
- `logcli query '{app="nginx"} |= "500"' --from="1h ago" --limit 20`
- `logcli query rate('{app="checkout"}[5m]') --from="1h ago"`
- `curl -G -s http://localhost:3100/loki/api/v1/query_range --data-urlencode 'query={app="checkout"}' --data-urlencode 'limit=10'`
- `logcli labels app`

**Examples:**
- logcli query '{app="nginx"} |= "500"' --from="1h ago" --limit 20
- logcli query rate('{app="checkout"}[5m]') --from="1h ago"
- curl -G -s http://localhost:3100/loki/api/v1/query_range --data-urlencode 'query={app="checkout"}' --data-urlencode 'limit=10'