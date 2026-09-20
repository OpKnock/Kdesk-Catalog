---
applyTo: "**/*.json **/*.r **/*.sh **/*.{yaml,yml}"
---

# Logging Elasticsearch Ops

Centralized logging with the ELK stack: Elasticsearch index setup, Filebeat shipping, Logstash pipelines, and querying logs with curl.

## Instructions

# Logging v2 (ELK Stack)

Centralized log analysis with Elasticsearch, Filebeat, and Logstash.

## What this skill does

- Creates Elasticsearch indices for log data.
- Ships files with Filebeat and processes with Logstash.
- Queries and aggregates logs via the ES REST API.

## When to use

- Organization-wide log search and retention.
- Auditing error rates by service and timeframe.
- Feeding logs into Kibana dashboards.

## Real commands

```bash
# Create the log index
curl -s -X PUT 'localhost:9200/app-logs?pretty' \
  -H 'Content-Type: application/json'

# Search errors
curl -s 'localhost:9200/app-logs/_search?q=level:ERROR&size=10' \
  | jq '.hits.hits[]._source'

# Index health
curl -s 'localhost:9200/_cat/indices?v' | grep app-logs

# Ingest a document directly
curl -s -X POST 'localhost:9200/app-logs/_doc' \
  -H 'Content-Type: application/json' \
  -d '{"level":"info","msg":"smoke test"}'

# Filebeat: validate config and output
filebeat test config -c filebeat.yml
filebeat test output -c filebeat.yml

# Filebeat: run
filebeat -e -c filebeat.yml

# Logstash: validate then run
logstash --config.test_and_exit -f logstash.conf
logstash -f logstash.conf
```

## filebeat.yml example

```yaml
filebeat.inputs:
  - type: filestream
    id: app-logs
    paths:
      - /var/log/app/*.log
output.elasticsearch:
  hosts: ["localhost:9200"]
  index: "app-logs"
```

## logstash.conf example

```
input { beats { port => 5044 } }
filter {
  if [message] =~ /^\{/ {
    json { source => "message" }
  }
}
output { elasticsearch { hosts => ["localhost:9200"] index => "app-logs" } }
```

## Testing

```bash
echo '{"level":"error","msg":"test"}' | nc localhost 5044
curl -s 'localhost:9200/app-logs/_count?q=level:error'
```

## Best practices

- Use index lifecycle management (ILM) for retention and rollover.
- Send everything to one pipeline; parse JSON as early as possible.
- Test configs with --config.test_and_exit / filebeat test before deploy.

## Capabilities

### elasticsearch-ops
Create indices and query log documents in Elasticsearch.

**Commands:**
- `curl -s -X PUT 'localhost:9200/app-logs?pretty' -H 'Content-Type: application/json'`
- `curl -s 'localhost:9200/app-logs/_search?q=level:ERROR&size=10' | jq '.hits.hits[]._source'`
- `curl -s 'localhost:9200/_cat/indices?v' | grep app-logs`
- `curl -s -X POST 'localhost:9200/app-logs/_doc' -H 'Content-Type: application/json' -d '{"level":"info","msg":"smoke test"}'`

**Examples:**
- curl -s -X PUT 'localhost:9200/app-logs?pretty' -H 'Content-Type: application/json'
- curl -s 'localhost:9200/app-logs/_search?q=level:ERROR&size=10' | jq '.hits.hits[]._source'
- curl -s 'localhost:9200/_cat/indices?v' | grep app-logs

### ship-process
Ship logs with Filebeat and process with Logstash pipelines.

**Commands:**
- `filebeat -e -c filebeat.yml`
- `filebeat test config -c filebeat.yml`
- `filebeat test output -c filebeat.yml`
- `logstash -f logstash.conf`
- `logstash --config.test_and_exit -f logstash.conf`

**Examples:**
- filebeat -e -c filebeat.yml
- filebeat test output -c filebeat.yml
- logstash --config.test_and_exit -f logstash.conf
