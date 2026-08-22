---
type: agent_requested
description: "Aggregates logs across infrastructure with Loki, Elasticsearch, and Fluent Bit: collection pipelines, queries, and retention."
---

# Log Aggregation

Aggregates logs across infrastructure with Loki, Elasticsearch, and Fluent Bit: collection pipelines, queries, and retention.

## Instructions

# Log Aggregation

Centralize logs from containers, nodes, and apps into searchable stores.

## What This Skill Does

- Deploys Loki + Promtail for label-based log storage
- Runs ELK stacks (Elasticsearch + Logstash/Filebeat) for full-text search
- Queries aggregated logs (LogQL, _search)
- Configures parsers, pipelines, and retention policies
- Routes Fluent Bit outputs between stores

## When to Use

- You need to search logs across many pods/hosts
- Correlating errors across microservices
- Building dashboards and alerting on log trends

## Real Commands

```bash
# Loki stack
helm repo add grafana https://grafana.github.io/helm-charts
helm upgrade --install loki grafana/loki-stack --namespace observability
kubectl get pods -n observability -l app=loki
logcli query '{app="web"} |= "ERROR" | json' --limit 50
logcli labels

# ELK
docker run -d -p 9200:9200 -e discovery.type=single-node   docker.elastic.co/elasticsearch/elasticsearch:8.13.0
filebeat -e -c filebeat.yml
curl -s localhost:9200/_cat/indices?v
curl -s 'localhost:9200/_search?q=level:error&size=10'

# Fluent Bit pipeline
fluent-bit -c fluent-bit.conf
```

## Best Practices

- Use labels sparingly in Loki (high-cardinality labels hurt performance)
- Ship logs over a sidecar or daemonset, never from inside app code paths
- Set retention per environment; log storage is expensive
- Normalize timestamps and levels in the pipeline (parsers)
- Alert on log volume anomalies before alerting on message content

## Capabilities

### loki-stack
Deploy Loki + Promtail and query aggregated logs with LogQL.

**Commands:**
- `helm repo add grafana https://grafana.github.io/helm-charts`
- `helm upgrade --install loki grafana/loki-stack --namespace observability --create-namespace`
- `kubectl get pods -n observability -l app=loki`
- `curl -s 'http://loki:3100/loki/api/v1/query_range?query={namespace="app"}'`
- `logcli query '{app="web"} |= "ERROR"' --limit 50`
- `logcli labels`

**Examples:**
- helm upgrade --install loki grafana/loki-stack
- logcli query '{app="web"} |= "ERROR"' --limit 50
- logcli labels

### elk-pipeline
Run Elasticsearch, Logstash, and Filebeat pipelines for index-based aggregation.

**Commands:**
- `docker run -d -p 9200:9200 -e discovery.type=single-node docker.elastic.co/elasticsearch/elasticsearch:8.13.0`
- `docker run -d -v logstash.conf:/usr/share/logstash/pipeline -p 5044:5044 docker.elastic.co/logstash/logstash:8.13.0`
- `filebeat modules list`
- `filebeat -e -c filebeat.yml`
- `curl -s localhost:9200/_cat/indices?v`
- `curl -s localhost:9200/_search?q=level:error`

**Examples:**
- docker run -d -p 9200:9200 elasticsearch:8.13.0
- filebeat -e -c filebeat.yml
- curl -s localhost:9200/_cat/indices?v