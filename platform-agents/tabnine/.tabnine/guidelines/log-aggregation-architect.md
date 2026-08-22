# log-aggregation-architect

Architects log pipelines with Loki, logcli, and Elasticsearch: collection, querying, retention, and cost-effective storage.

## Instructions

# Log Aggregation

Centralize logs so incidents are searchable in seconds.

## When to Use

- Consolidating logs from many services
- Building the search-first debugging workflow
- Right-sizing retention vs cost

## Loki + logcli

```bash
logcli query '{app="api"}' --since 1h
logcli query '{app="api"} |= "error"' --since 24h --limit 500
logcli query '{service="checkout"} | json | level="ERROR"' --since 6h
```

LogQL pipelines: `|=` substring, `|~` regex, `| json`, `| line_format`.

## Live tail

```bash
logcli live '{app="api"}'
```

## Collection

Promtail agents label streams with k8s metadata: `{app=...}`, `{namespace=...}`, `{pod=...}`. Cardinally label with app/service/namespace only.

## Elasticsearch path

```bash
curl -s 'http://localhost:9200/_cat/indices?v&h=index,docs.count,store.size'
curl -s -X POST 'http://localhost:9200/logs-2026.08.10/_search' -H 'Content-Type: application/json' -d '{"query":{"match":{"level":"ERROR"}},"size":10}'
```

## Retention design

- Hot: 7 days at full cardinality.
- Warm: 30 days at reduced verbosity.
- Cold: 90+ days sampled or in object storage.

## Best practices

- Structured logs (JSON) beat grep-able prose.
- Correlate logs with traces via trace_id field.
- Alert on error-rate metrics, not raw log volume.
- Sample debug logs; keep error logs complete.

## Testing

```bash
logcli query '{app="api"}' --since 10m | wc -l
```

Verify pipelines after every deploy.

## Capabilities

### loki
Query and operate Grafana Loki with logcli.

**Commands:**
- `logcli query '{app="api"}' --since 1h`
- `logcli query '{app="api"} |= "error"' --since 24h --limit 500`
- `logcli labels --since 1h`
- `logcli series '{app=~".+"}' --since 6h`
- `logcli live '{app="api"}'`

**Examples:**
- logcli query '{service="checkout", level="error"}' --since 1h | head -50
- logcli query '{app="api"} | json | level="ERROR"' --since 6h
- logcli query '{app="api"} |= "panic" | line_format "{{.ts}} {{.message}}"' --since 24h

### elasticsearch
Search and manage Elasticsearch indices.

**Commands:**
- `curl -s 'http://localhost:9200/_cat/indices?v' | head -20`
- `curl -s -X POST 'http://localhost:9200/logs-2026.08.10/_search' -H 'Content-Type: application/json' -d '{"query":{"match":{"level":"ERROR"}},"size":10}'`
- `curl -s 'http://localhost:9200/_cat/indices?v&h=index,docs.count,store.size' | sort -k3 -rn | head`
- `curl -s -X PUT 'http://localhost:9200/logs-2026.08.10/_settings' -H 'Content-Type: application/json' -d '{"index":{"number_of_replicas":0}}'`
- `curl -s -X POST 'http://localhost:9200/logs-*/_delete_by_query' -H 'Content-Type: application/json' -d '{"query":{"range":{"@timestamp":{"lte":"2025-01-01"}}}}'`

**Examples:**
- curl -s 'http://localhost:9200/_cat/indices?v&h=index,docs.count' | grep logs-
- curl -s -X POST 'http://localhost:9200/logs-*/_search' -H 'Content-Type: application/json' -d '{"query":{"match_phrase":{"message":"out of memory"}},"size":20}'
- curl -s 'http://localhost:9200/_cluster/health' | jq