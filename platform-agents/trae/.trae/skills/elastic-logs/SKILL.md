---
name: "elastic-logs"
description: "Ship, index, and query application logs into Elasticsearch with Filebeat, and run Elasticsearch log queries from the CLI."
---

# Elastic Logs

Ship, index, and query application logs into Elasticsearch with Filebeat, and run Elasticsearch log queries from the CLI.

## Instructions

# Elastic Logs

## What this skill does

This skill covers shipping application and system logs into Elasticsearch with Filebeat and querying them with the Elasticsearch REST API. Filebeat tails files, applies processors, and sends events to Elasticsearch or Logstash.

## When to use

- Standing up centralized logging for services
- Adding error-rate dashboards over filebeat-* indices
- Troubleshooting why logs are not arriving in Kibana

## Real commands

```bash
# Validate config, then run
filebeat test config -c filebeat.yml
filebeat -e -c filebeat.yml

# Set up index templates and ILM
filebeat setup -e -c filebeat.yml --index-management

# Query the latest error lines
curl -s 'localhost:9200/filebeat-*/_search' -H 'Content-Type: application/json' -d '{"query":{"bool":{"filter":[{"term":{"log.level":"ERROR"}}]}},"size":10}' | jq '.hits.hits[]._source.message'

# List log indices
curl -s 'localhost:9200/_cat/indices/filebeat-*?v'
```

## filebeat.yml example

```yaml
filebeat.inputs:
  - type: filestream
    id: app-logs
    paths:
      - /var/log/app/*.log
    parsers:
      - ndjson:
          target: ""
processors:
  - add_host_metadata: {}
  - add_cloud_metadata: {}
output.elasticsearch:
  hosts: ['http://localhost:9200']
  username: filebeat_writer
  password: '${FILEBEAT_PASSWORD}'
```

## Testing

```bash
# Watch the beat's own output while tailing a file
filebeat -e -c filebeat.yml -d 'publish'
```

## Best practices

- Use ILM (index lifecycle management) with 7-day hot then warm phases.
- Tag and namespace logs with `fields.service` for multi-tenant filtering.
- Set `filebeat.inputs` to filestream (modern) not log (legacy).
- Monitor `monitoring` dashboards for dropped events and registry errors.
- Keep secrets in `${VAR}` env references, never in the config file.

## Capabilities

### log-shipping
Configure and run Filebeat, test pipelines, and query indexed logs via the Elasticsearch REST API.

**Commands:**
- `filebeat test config -c filebeat.yml`
- `filebeat setup -e -c filebeat.yml --index-management`
- `filebeat -e -c filebeat.yml`
- `curl -s 'localhost:9200/filebeat-*/_search' -H 'Content-Type: application/json' -d '{"query":{"match_all":{}},"size":5}' | jq '.hits.total'`
- `curl -s 'localhost:9200/filebeat-*/_mapping' | jq '.filebeat-2024.*'`

**Examples:**
- filebeat test config -c filebeat.yml && filebeat -e -c filebeat.yml
- curl -s 'localhost:9200/filebeat-*/_search' -H 'Content-Type: application/json' -d '{"query":{"bool":{"filter":[{"term":{"log.level":"ERROR"}}]}},"size":10}' | jq '.hits.hits[]._source.message'
- curl -s 'localhost:9200/_cat/indices/filebeat-*?v'
