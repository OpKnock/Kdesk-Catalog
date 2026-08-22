# tempo

Query traces with the it CLI. Search and query traces via the it HTTP API. and trace correlation.'

## Instructions

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