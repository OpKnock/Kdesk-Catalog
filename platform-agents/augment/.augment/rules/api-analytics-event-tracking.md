---
type: agent_requested
description: "API analytics event tracking and funnels - capture custom events via Segment HTTP API, analyze conversion, and build retention views. Use when working with event tracking or when the user mentions event tracking."
---

API analytics event tracking and funnels - capture custom events via Segment HTTP API, analyze conversion, and build retention views.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -s -X POST https://api.segment.io/v1/track -u 'WRITE_KE`
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

# API Analytics (Event Tracking)

## What this skill does
Track custom product events around your API - signups, orders, feature use - via the Segment HTTP API, then analyze funnels and retention to understand conversion.

## When to use
- Measuring feature adoption
- Building conversion funnels
- Cohort retention analysis

## Real commands
```bash
# Track an event
curl -s -X POST https://api.segment.io/v1/track \
  -u 'WRITE_KEY:' -H 'Content-Type: application/json' \
  -d '{"userId":"u_123","event":"API Call","properties":{"endpoint":"/v1/orders"}}'

# Identify a user
curl -s -X POST https://api.segment.io/v1/identify \
  -u 'WRITE_KEY:' -H 'Content-Type: application/json' \
  -d '{"userId":"u_123","traits":{"plan":"enterprise"}}'

# Funnel analysis
curl -s 'http://localhost:8080/api/analytics/funnel?steps=visit,create_order,pay' | jq '.steps[].conversion'

# Retention
curl -s 'http://localhost:8080/api/analytics/retention?cohort=day' | jq '.cohorts[-1]'

# Event volume by name
curl -s http://localhost:8080/api/analytics/events -H 'X-API-Key: key' | jq '.events | group_by(.name) | map({name: .[0].name, count: length})'
```

## Event schema discipline
```json
{
  "userId": "u_123",
  "event": "Checkout Started",
  "properties": { "endpoint": "/v1/orders", "status": 201 }
}
```

## Best practices
- Use verb-past-tense event names (Order Completed)
- Keep a properties dictionary per event
- Send events from server-side, not the browser, for APIs
- Batch events and retry with backoff

## Testing
```bash
curl -s -X POST http://localhost:8080/api/analytics/test-event -H 'Content-Type: application/json' -d '{"name":"Test"}'
curl -s 'http://localhost:8080/api/analytics/events?event=Test' | jq '.total'
```

## Capabilities

### event-tracking
Track API events and analyze funnels

**Parameters:**
- `event` (string): Event name, e.g. API Call
- `steps` (string): Comma-separated funnel steps
- `cohort` (string): Cohort granularity: day, week, month

**Commands:**
- `curl -s -X POST https://api.segment.io/v1/track -u 'WRITE_KEY:' -H 'Content-Type: application/json' -d '{"userId":"u_123","event":"API Call","properties":{"endpoint":"/v1/orders"}}'`
- `curl -s -X POST https://api.segment.io/v1/identify -u 'WRITE_KEY:' -H 'Content-Type: application/json' -d '{"userId":"u_123","traits":{"plan":"enterprise"}}'`
- `curl -s 'http://localhost:8080/api/analytics/funnel?steps=visit,create_order,pay' | jq '.steps[].conversion'`
- `curl -s 'http://localhost:8080/api/analytics/retention?cohort=day' | jq '.cohorts[-1]'`
- `curl -s http://localhost:8080/api/analytics/events -H 'X-API-Key: key' | jq '.events | group_by(.name) | map({name: .[0].name, count: length})'`

**Examples:**
- curl -s -X POST https://api.segment.io/v1/track -u 'WRITE_KEY:' -d '{"userId":"u_123","event":"Checkout Started","properties":{"cart":{"total":99.9}}}'
- curl -s 'http://localhost:8080/api/analytics/funnel?steps=signup,activate,invite' | jq '.steps'
- curl -s 'http://localhost:8080/api/analytics/events?event=API%20Call&from=2024-06-01' | jq '.total'

## References
- [Segment HTTP Tracking API](https://segment.com/docs/connections/sources/catalog/libraries/server/http/)
- [Amplitude HTTP API](https://developers.amplitude.com/docs/http-api-v2)