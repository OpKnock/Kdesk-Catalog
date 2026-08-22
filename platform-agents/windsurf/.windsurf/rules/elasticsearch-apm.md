---
trigger: glob
description: "Application performance monitoring with the Elastic APM stack: configure APM Server, instrument Node.js apps, and query traces from the CLI."
globs: ["**/*.java", "**/*.json", "**/*.r", "**/*.sh", "**/*.{js,ts,jsx,tsx}", "**/*.{yaml,yml}"]
---

# Elasticsearch Apm

Application performance monitoring with the Elastic APM stack: configure APM Server, instrument Node.js apps, and query traces from the CLI.

## Instructions

# Elasticsearch APM

## What this skill does

Elastic APM captures transactions, spans, and errors from instrumented services. APM Server (port 8200) receives data from agents and indexes into `apm-*` indices; Kibana visualizes the traces.

## When to use

- Finding slow endpoints and their bottleneck spans
- Instrumenting a new service with a minimum of code
- Verifying APM data flows end to end

## Real commands

```bash
# Validate config and start the server
apm-server test config -c apm-server.yml
apm-server -e -c apm-server.yml

# Health check
curl -s http://localhost:8200/ | jq '.version'

# Node.js agent
npm install elastic-apm-node
node -r elastic-apm-node/start app.js

# Verify transactions landed in Elasticsearch
curl -s 'localhost:9200/apm-*/_search' -H 'Content-Type: application/json' -d '{"query":{"term":{"processor.event":"transaction"}},"size":3}' | jq '.hits.total'
```

## apm-server.yml example

```yaml
apm-server:
  host: "0.0.0.0:8200"
  auth:
    secret_token: '${APM_SECRET_TOKEN}'
output.elasticsearch:
  hosts: ['https://es.example.com:9200']
  username: apm_server_writer
  password: '${APM_ES_PASSWORD}'
```

## Agent config example

```javascript
const apm = require('elastic-apm-node').start({
  serviceName: 'orders-api',
  serverUrl: 'http://apm.internal:8200',
  secretToken: process.env.APM_SECRET_TOKEN,
  environment: process.env.NODE_ENV,
  captureBody: 'errors'
})
```

## Testing

```bash
# Generate traffic and check for spans
curl -s http://localhost:8080/api/orders > /dev/null
curl -s 'localhost:9200/apm-*/_search' -H 'Content-Type: application/json' -d '{"query":{"term":{"service.name":"orders-api"}}}' | jq '.hits.total'
```

## Best practices

- Set a secret token and TLS for the APM intake endpoint.
- Sample at 10% in prod and use central config to adjust per service.
- Set `captureBody: 'errors'` to limit sensitive data.
- Correlate traces with logs by shipping the `trace.id` into log records.

## Capabilities

### apm-instrumentation
Configure and run the Elastic APM server and agents, and inspect traces and service status.

**Commands:**
- `apm-server -e -c apm-server.yml`
- `apm-server test config -c apm-server.yml`
- `curl -s http://localhost:8200/ | jq`
- `npm install elastic-apm-node`
- `curl -s 'localhost:9200/apm-*/_search' -H 'Content-Type: application/json' -d '{"query":{"term":{"processor.event":"transaction"}},"size":3}' | jq '.hits.total'`

**Examples:**
- apm-server test config -c apm-server.yml && apm-server -e -c apm-server.yml
- curl -s 'localhost:9200/apm-*/_search' -H 'Content-Type: application/json' -d '{"query":{"range":{"@timestamp":{"gte":"now-1h"}}}}' | jq '.hits.total'
- curl -s http://localhost:8200/ | jq '.version'
