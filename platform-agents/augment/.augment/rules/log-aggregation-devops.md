---
type: agent_requested
description: "Aggregates logs across infrastructure with Loki, Elasticsearch, and Fluent Bit: collection pipelines, queries, and retention. Use when working with loki stack, elk pipeline, devops or when the user mentions loki stack, elk pipeline, devops."
---

Aggregates logs across infrastructure with Loki, Elasticsearch, and Fluent Bit: collection pipelines, queries, and retention.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `helm repo add grafana https://grafana.github.io/helm-charts`, `docker run -d -p 9200:9200 -e discovery.type=single-node doc`
- Check `knowledge` references and prerequisites before proceeding

### 2. Reason
Analyze and plan:
- Compare current state vs desired state (drift, checksums, policy)
- Evaluate trust, compatibility, and risk: use `kdesk trust` and `kdesk doctor` patterns
- Decide: which capabilities/tools are needed, which can be skipped

### 3. Act
Execute with guards:
- Run only `allowed-tools` (see frontmatter); use `safe_path` for writes
- Prefer `Bash` with explicit binaries (`curl`, `kubectl`, `kdesk`) over generic shell
- Record evidence: file paths, checksums, and tool outputs for verification

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

**Parameters:**
- `query` (string): LogQL stream selector and filter
- `limit` (integer): Max log entries to return

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

**Parameters:**
- `index` (string): Elasticsearch index pattern
- `config` (string): Beat/Logstash config path

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

## References
- [Loki Documentation](https://grafana.com/docs/loki/latest/)
- [Elasticsearch Reference](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
- [Fluent Bit](https://docs.fluentbit.io/manual/)