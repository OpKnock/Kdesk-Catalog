---
name: "alertmanager"
description: "Query alerts and manage silences from the CLI. Validate it configuration and routing."
type: knowledge
triggers: ["alertmanager", "amtool", "config"]
---

# alertmanager

Query alerts and manage silences from the CLI. Validate it configuration and routing.

## Instructions

# Alertmanager

Manage alerts, silences, and routing without the UI.

## When to Use

- On-call triage of firing alerts
- Planned-maintenance silences
- Validating routing before deploy

## Query alerts

```bash
amtool alert query --alertmanager.url=http://localhost:9093 --state=active
```

## Silences with policy

```bash
amtool silence add --alertmanager.url=http://localhost:9093 'severity=~critical' --duration=2h --comment='scheduled maintenance'
```

Every silence needs a comment and an expiry - review active silences weekly.

## Config validation

```bash
amtool check-config /etc/alertmanager/alertmanager.yml
```

## Routing design

```yaml
route:
  group_by: [alertname]
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  routes:
    - matchers: [severity="critical"]
      receiver: pagerduty-critical
    - matchers: [severity=~"warning|info"]
      receiver: slack
```

Group similar alerts to prevent notification storms; set repeat_interval to avoid alert fatigue.

## Test alert delivery

```bash
curl -s -X POST -H 'Content-Type: application/json' -d '{"status":"firing","labels":{"alertname":"ApiDown","severity":"critical"}}' http://localhost:9093/api/v2/alerts
```

## Best practices

- Route by severity + team, not per alert.
- Use matchers with regex sparingly - they're hard to audit.
- Export alert state to dashboards for review.
- Never silence for longer than the maintenance window.

## Testing

```bash
amtool check-config alertmanager.yml
curl -s http://localhost:9093/api/v2/alerts | jq length
```

Post a test firing alert and verify the route/receiver chain.

## Capabilities

### amtool
Query alerts and manage silences from the CLI.

**Commands:**
- `amtool alert query --alertmanager.url=http://localhost:9093`
- `amtool alert query --alertmanager.url=http://localhost:9093 --state=active`
- `amtool silence add --alertmanager.url=http://localhost:9093 'severity=~critical' --duration=2h --comment='scheduled maintenance'`
- `amtool silence expire --alertmanager.url=http://localhost:9093 SILENCE_ID`
- `amtool silence query --alertmanager.url=http://localhost:9093 --pending`

**Examples:**
- amtool alert query --alertmanager.url=http://localhost:9093 -q
- amtool silence add --alertmanager.url=http://localhost:9093 'job="api"' --duration=1h --author=alice --comment='incident triage'
- amtool silence query --alertmanager.url=http://localhost:9093 --state=active --output=json

### config
Validate Alertmanager configuration and routing.

**Commands:**
- `amtool check-config alertmanager.yml`
- `amtool config routes --alertmanager.url=http://localhost:9093`
- `amtool config show --alertmanager.url=http://localhost:9093`
- `curl -s -X POST -H 'Content-Type: application/json' -d '{"status":"firing","labels":{"alertname":"ApiDown","severity":"critical"}}' http://localhost:9093/api/v2/alerts`
- `curl -s http://localhost:9093/api/v2/alerts | jq '.[] | {name: .labels.alertname, status: .status.state}'`

**Examples:**
- amtool check-config /etc/alertmanager/alertmanager.yml
- amtool config routes --alertmanager.url=http://localhost:9093
- curl -s http://localhost:9093/api/v2/alerts | jq length
