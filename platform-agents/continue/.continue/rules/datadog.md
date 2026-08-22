---
name: "Datadog"
description: "Operates the Datadog Agent and dashboards: agent status, live checks, monitors, and diagnostics via the CLI and API."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
alwaysApply: false
---

# Datadog

Operates the Datadog Agent and dashboards: agent status, live checks, monitors, and diagnostics via the CLI and API.

## Instructions

# Datadog

Operate the Datadog agent and monitors from the terminal.

## When to Use

- Agent health and integration debugging
- Creating monitors without the UI
- Correlating metrics with incidents

## Agent operations

```bash
datadog-agent status
datadog-agent check nginx
datadog-agent flare --send
datadog-agent restart
```

Flare bundles logs + configs for support - redact secrets before sending.

## Monitors via API

```bash
curl -s -X POST -H 'DD-API-KEY: $DD_API_KEY' -H 'DD-APPLICATION-KEY: $DD_APP_KEY' -H 'Content-Type: application/json' -d '{"type":"metric alert","query":"avg(last_5m):avg:system.cpu.user{*} > 80","name":"High CPU","message":"CPU above 80%"}' https://api.datadoghq.com/api/v1/monitor
```

## Monitor hygiene

- Alert on SLOs and error budgets, not every metric.
- Mute with a reason and an expiry: mute then unmute in the incident timeline.
- Review monitor inventory quarterly; delete orphans.

## Metric queries

```bash
curl -s -X POST -H 'DD-API-KEY: $DD_API_KEY' -H 'DD-APPLICATION-KEY: $DD_APP_KEY' -H 'Content-Type: application/json' -d '{"query":"system.cpu.user"}' 'https://api.datadoghq.com/api/v1/query?from=...&to=...'
```

## Best practices

- Use service accounts for API keys, rotated regularly.
- Keep agent tags consistent across the fleet.
- Export monitor configs to IaC where possible.
- Verify agent version pinning across hosts.

## Testing

```bash
datadog-agent status | grep -E 'Running|Errors'
datadog-agent check disk
```

Confirm checks pass after config changes.

## Capabilities

### agent
Manage the Datadog agent locally.

**Commands:**
- `datadog-agent status`
- `datadog-agent check nginx`
- `datadog-agent flare --send`
- `datadog-agent config show | grep -E 'api_key|hostname'`
- `datadog-agent restart`

**Examples:**
- datadog-agent status | grep -E 'Running|Total Events'
- datadog-agent check disk -r 3
- datadog-agent flare --send --local-timeout 30

### monitors
Manage monitors and metrics via the Datadog API.

**Commands:**
- `curl -s -H 'DD-API-KEY: $DD_API_KEY' -H 'DD-APPLICATION-KEY: $DD_APP_KEY' 'https://api.datadoghq.com/api/v1/monitor' | jq '.[] | {id, name, status}'`
- `curl -s -X POST -H 'DD-API-KEY: $DD_API_KEY' -H 'DD-APPLICATION-KEY: $DD_APP_KEY' -H 'Content-Type: application/json' -d '{"type":"metric alert","query":"avg(last_5m):avg:system.cpu.user{*} > 80","name":"High CPU","message":"CPU above 80%"}' https://api.datadoghq.com/api/v1/monitor`
- `curl -s -X POST -H 'DD-API-KEY: $DD_API_KEY' -H 'DD-APPLICATION-KEY: $DD_APP_KEY' -H 'Content-Type: application/json' -d '{"query":"system.cpu.user"}' 'https://api.datadoghq.com/api/v1/query?from=1750000000&to=1750086400'`
- `curl -s -X PUT -H 'DD-API-KEY: $DD_API_KEY' -H 'DD-APPLICATION-KEY: $DD_APP_KEY' -H 'Content-Type: application/json' -d '{"status":"Muted"}' https://api.datadoghq.com/api/v1/monitor/12345/mute`
- `curl -s -H 'DD-API-KEY: $DD_API_KEY' -H 'DD-APPLICATION-KEY: $DD_APP_KEY' 'https://api.datadoghq.com/api/v1/monitor' | jq '[.[].status] | group_by(.) | map({status: .[0], count: length})'`

**Examples:**
- curl -s -H 'DD-API-KEY: $K' -H 'DD-APPLICATION-KEY: $A' 'https://api.datadoghq.com/api/v1/monitor' | jq '.[] | select(.status != "OK") | {name, status}'
- curl -s -X POST -H 'DD-API-KEY: $K' -H 'DD-APPLICATION-KEY: $A' -H 'Content-Type: application/json' -d '{"type":"service check","query":"\"api.up\".over(\"last_5m\").last(5).count_by_status()","name":"API up check"}' https://api.datadoghq.com/api/v1/monitor
- curl -s -H 'DD-API-KEY: $K' -H 'DD-APPLICATION-KEY: $A' 'https://api.datadoghq.com/api/v1/monitor' | jq 'length'