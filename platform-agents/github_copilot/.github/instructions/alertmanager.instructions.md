---
applyTo: "**/*.json **/*.r **/*.sh **/*.{yaml,yml}"
---

Query alerts and manage silences from the CLI. Validate it configuration and routing.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `amtool alert query --alertmanager.url=http://localhost:9093`, `amtool check-config alertmanager.yml`
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

**Parameters:**
- `alertmanager.url` (string): Alertmanager API URL
- `duration` (string): Silence duration like 2h
- `comment` (string): Silence rationale (required by policy)

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

**Parameters:**
- `config` (string): alertmanager.yml path
- `payload` (string): Alert JSON to post
- `url` (string): Alertmanager base URL

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

## References
- [Alertmanager Docs](https://prometheus.io/docs/alerting/latest/alertmanager/)
- [amtool](https://prometheus.io/docs/alerting/latest/amtool/)
- [Alertmanager HTTP API](https://prometheus.io/docs/alerting/latest/clients/)
