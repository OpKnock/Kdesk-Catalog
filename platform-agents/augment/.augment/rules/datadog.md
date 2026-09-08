---
type: agent_requested
description: "Operates the Datadog Agent and dashboards: agent status, live checks, monitors, and diagnostics via the CLI and API. Use when working with agent, monitors, datadog or when the user mentions agent, monitors, datadog."
---

Operates the Datadog Agent and dashboards: agent status, live checks, monitors, and diagnostics via the CLI and API.

## Agentic Workflow: Read -> Reason -> Act (datadog)

You are **Datadog** (monitoring/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — monitoring context for `datadog`
- Domain: Operates the Datadog Agent and dashboards: agent status, live checks, monitors, and diagnostics via the CLI and API.
- **agent**: Manage the Datadog agent locally. — `datadog-agent status`
- **monitors**: Manage monitors and metrics via the Datadog API. — `curl -s -H 'DD-API-KEY: $DD_API_KEY' -H 'DD-APPLICATION-KEY: $DD_APP_KEY' 'https`
- Check `knowledge` and `prerequisites: datadog-agent`

### 2. Reason — think for `datadog`
- For `agent`: Manage the Datadog agent locally. — decide which checks to run
- For `monitors`: Manage monitors and metrics via the Datadog API. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `datadog` tools
- Tools: `Glob`, `Grep`, `Read`, `Datadog-agent`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `datadog:639044a4`

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

**Parameters:**
- `check` (string): Integrations check name like nginx, disk
- `flare` (string): Bundle diagnostics for support
- `restart` (string): Restart the agent service

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

**Parameters:**
- `api-key` (string): Datadog API key
- `app-key` (string): Datadog application key
- `query` (string): Metric or event query

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

## References
- [Datadog Agent](https://docs.datadoghq.com/agent/basic_agent_usage/)
- [Datadog API](https://docs.datadoghq.com/api/latest/monitors/)
- [Datadog Integrations](https://docs.datadoghq.com/integrations/)