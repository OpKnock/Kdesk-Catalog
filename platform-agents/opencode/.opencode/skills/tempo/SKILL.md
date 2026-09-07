---
name: "tempo"
description: "Query traces with the it CLI. Search and query traces via the it HTTP API. and trace correlation.'. Use when working with tempo cli, http api or when the user mentions tempo cli, http api."
---

Query traces with the it CLI. Search and query traces via the it HTTP API. and trace correlation.'

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `tempo-cli query trace 00000000000000000000000000000000 --hos`, `curl -G -s 'http://localhost:3200/api/search' --data-urlenco`
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

# Tempo

Find slow and failed requests by their traces.

## When to Use

- Correlating logs to full request paths
- Root-causing latency regressions
- Auditing cross-service failures

## Search traces

```bash
tempo-cli search --host localhost:3200 '{resource.service.name="checkout"}' --limit 10
```

## Fetch a trace

```bash
tempo-cli query trace <trace-id> --host localhost:3200 | jq '.spans | length'
```

## Via HTTP API

```bash
curl -G -s 'http://localhost:3200/api/search' --data-urlencode 'tags=service.name=checkout' --data-urlencode 'limit=10'
curl -s 'http://localhost:3200/api/traces/<trace-id>'
```

## Correlate with logs

Logs carry `trace_id`; logs to traces via the same id in Grafana.

## Best practices

- Sample strategically: 100% for errors, lower for happy paths.
- Set a duration filter to skip noisy fast traces.
- Keep span names short and standardized.
- Instrument every outbound call (DB, HTTP, queue).

## Testing

```bash
curl -s 'http://localhost:3200/ready'
tempo-cli query blocks --host localhost:3200 --since 1h
```

Verify blocks are flushed and queryable after load.

## Capabilities

### tempo-cli
Query traces with the Tempo CLI.

**Parameters:**
- `trace-id` (string): 16 or 32 hex char trace id
- `host` (string): Tempo query-frontend address
- `limit` (number): Max results

**Commands:**
- `tempo-cli query trace 00000000000000000000000000000000 --host localhost:3200`
- `tempo-cli search --host localhost:3200 '{resource.service.name="checkout"}' --limit 10`
- `tempo-cli query blocks --host localhost:3200 --since 1h`
- `tempo-cli query trace 00000000000000000000000000000000 --host localhost:3200 --format json | jq '.spans | length'`
- `tempo-cli search --host localhost:3200 '{resource.service.name=~"api|checkout"} && duration > 1s' --limit 20`

**Examples:**
- tempo-cli query trace 5f3a1c9e0000000000000001 --host localhost:3200 | jq '.rootSpan'
- tempo-cli search --host localhost:3200 '{span.http.status_code >= 500}' --limit 50
- tempo-cli query blocks --host localhost:3200 --since 24h | head

### http-api
Search and query traces via the Tempo HTTP API.

**Parameters:**
- `tags` (string): Tag filters like service.name=x
- `minDuration` (string): Minimum span duration filter
- `trace-id` (string): Trace id to fetch

**Commands:**
- `curl -G -s 'http://localhost:3200/api/search' --data-urlencode 'tags=service.name=checkout' --data-urlencode 'limit=10'`
- `curl -s 'http://localhost:3200/api/traces/00000000000000000000000000000000' | jq '.traceID'`
- `curl -s 'http://localhost:3200/ready' | jq`
- `curl -G -s 'http://localhost:3200/api/search/tags' | jq '.tagNames'`
- `curl -G -s 'http://localhost:3200/api/search' --data-urlencode 'tags=error=true' --data-urlencode 'minDuration=500ms' | jq '.traces | length'`

**Examples:**
- curl -G -s 'http://localhost:3200/api/search' --data-urlencode 'tags=service.name=api' | jq '.traces[0].traceID'
- curl -s 'http://localhost:3200/api/traces/5f3a1c9e0000000000000001' | jq '.spans[0].name'
- curl -s 'http://localhost:3200/ready'

## References
- [Tempo Docs](https://grafana.com/docs/tempo/latest/)
- [tempo-cli](https://grafana.com/docs/tempo/latest/reference/tempo-cli/)
- [Tempo API](https://grafana.com/docs/tempo/latest/api_docs/)
