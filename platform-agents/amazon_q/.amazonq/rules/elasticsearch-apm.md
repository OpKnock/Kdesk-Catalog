Application performance monitoring with the Elastic APM stack: configure APM Server, instrument Node.js apps, and query traces from the CLI.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `apm-server -e -c apm-server.yml`
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

**Parameters:**
- `apm-server-config` (string): Path to apm-server.yml
- `service-name` (string): APM agent service name for instrumentation
- `index-pattern` (string): Index pattern for APM data, e.g. apm-*

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

## References
- [APM Server Reference](https://www.elastic.co/guide/en/apm/server/current/index.html)
- [Elastic APM Node.js Agent](https://www.elastic.co/guide/en/apm/agent/nodejs/current/index.html)