---
trigger: glob
description: "Creates and manages Datadog monitors, dashboards, and synthetic API tests using the Datadog API and datadog-ci CLI for alerting on latency, error rates, and uptime. Use when working with monitors, synthetics, api or when the user mentions monitors, synthetics, api."
globs: ["**/*.json", "**/*.r", "**/*.sh", "**/*.tf"]
---

Creates and manages Datadog monitors, dashboards, and synthetic API tests using the Datadog API and datadog-ci CLI for alerting on latency, error rates, and uptime.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -X POST "https://api.datadoghq.com/api/v1/monitor" -H "`, `npx @datadog/datadog-ci synthetics run-tests --public-id abc`
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

# Datadog Monitoring

Monitor API health, latency, and uptime with Datadog monitors and synthetic tests.

## When to Use

- Alerting on API latency, error rates, and uptime
- Running synthetic API checks in CI and on a schedule
- Managing monitors as code

## Setup

```bash
export DD_API_KEY="your-api-key"
export DD_APP_KEY="your-application-key"
export DATADOG_SYNTHETICS_API_KEY="$DD_API_KEY"
export DATADOG_SYNTHETICS_APP_KEY="$DD_APP_KEY"
```

## Monitors

```bash
# Create a latency monitor
curl -X POST "https://api.datadoghq.com/api/v1/monitor" \
  -H "Content-Type: application/json" -H "DD-API-KEY: $DD_API_KEY" -H "DD-APPLICATION-KEY: $DD_APP_KEY" \
  -d '{"type":"metric alert","query":"avg(last_5m):avg:api.request.latency{*} > 500","name":"API latency high"}'

# List monitors
curl -X GET "https://api.datadoghq.com/api/v1/monitor" -H "DD-API-KEY: $DD_API_KEY" -H "DD-APPLICATION-KEY: $DD_APP_KEY" | jq '.[].name'

# Mute during maintenance
curl -X POST "https://api.datadoghq.com/api/v1/monitor/123456/mute" -H "DD-API-KEY: $DD_API_KEY" -H "DD-APPLICATION-KEY: $DD_APP_KEY"
```

## Synthetic Tests

```bash
npx @datadog/datadog-ci synthetics run-tests --public-id abc-123-def
npx @datadog/datadog-ci synthetics run-tests --files "./e2e/*.synthetics.json"
```

## Testing

```bash
# Trigger a monitor status check
curl -X GET "https://api.datadoghq.com/api/v1/monitor/123456" -H "DD-API-KEY: $DD_API_KEY" -H "DD-APPLICATION-KEY: $DD_APP_KEY" | jq '.overall_state'
```

## Best Practices

- Use terraform-provider-datadog for monitors as code
- Alert on SLOs, not just raw metrics
- Mute monitors for planned maintenance windows
- Add tags such as team:payments to monitors
- Run synthetics from CI on every deploy

## Capabilities

### monitors
Create, update, mute, and query Datadog monitors via the API

**Parameters:**
- `monitor_id` (string): Numeric Datadog monitor ID
- `query` (string): Monitor query such as avg(last_5m):avg:api.request.latency{*} > 500

**Commands:**
- `curl -X POST "https://api.datadoghq.com/api/v1/monitor" -H "Content-Type: application/json" -H "DD-API-KEY: $DD_API_KEY" -H "DD-APPLICATION-KEY: $DD_APP_KEY" -d @monitor.json`
- `curl -X GET "https://api.datadoghq.com/api/v1/monitor" -H "DD-API-KEY: $DD_API_KEY" -H "DD-APPLICATION-KEY: $DD_APP_KEY"`
- `curl -X POST "https://api.datadoghq.com/api/v1/monitor/MONITOR_ID/mute" -H "DD-API-KEY: $DD_API_KEY" -H "DD-APPLICATION-KEY: $DD_APP_KEY"`
- `curl -X PUT "https://api.datadoghq.com/api/v1/monitor/MONITOR_ID" -H "Content-Type: application/json" -H "DD-API-KEY: $DD_API_KEY" -H "DD-APPLICATION-KEY: $DD_APP_KEY" -d @monitor.json`

**Examples:**
- curl -X POST "https://api.datadoghq.com/api/v1/monitor" -H "Content-Type: application/json" -H "DD-API-KEY: $DD_API_KEY" -H "DD-APPLICATION-KEY: $DD_APP_KEY" -d '{"type":"metric alert","query":"avg(last_5m):avg:api.request.latency{*} > 500","name":"API latency high"}'
- curl -X GET "https://api.datadoghq.com/api/v1/monitor" -H "DD-API-KEY: $DD_API_KEY" -H "DD-APPLICATION-KEY: $DD_APP_KEY" | jq '.[] | select(.name | contains("API"))'
- curl -X POST "https://api.datadoghq.com/api/v1/monitor/123456/mute" -H "DD-API-KEY: $DD_API_KEY" -H "DD-APPLICATION-KEY: $DD_APP_KEY"

### synthetics
Run synthetic API tests from datadog-ci and check results

**Parameters:**
- `public_id` (string): Synthetic test public ID
- `files_glob` (string): Glob pattern for synthetic test definition files

**Commands:**
- `npx @datadog/datadog-ci synthetics run-tests --public-id abc-123-def`
- `npx @datadog/datadog-ci synthetics run-tests --config synthetics.global.json --files ./e2e/*.synthetics.json`
- `curl -X GET "https://api.datadoghq.com/api/v1/synthetics/tests" -H "DD-API-KEY: $DD_API_KEY" -H "DD-APPLICATION-KEY: $DD_APP_KEY"`
- `npx @datadog/datadog-ci synthetics run-tests --public-id abc-123-def --junit-report junit.xml`

**Examples:**
- npx @datadog/datadog-ci synthetics run-tests --public-id abc-123-def
- npx @datadog/datadog-ci synthetics run-tests --files "./e2e/*.synthetics.json"
- curl -s "https://api.datadoghq.com/api/v1/synthetics/tests" -H "DD-API-KEY: $DD_API_KEY" -H "DD-APPLICATION-KEY: $DD_APP_KEY" | jq '.synthetics[].name'

## References
- [Datadog Monitors API](https://docs.datadoghq.com/api/latest/monitors/)
- [datadog-ci Synthetics](https://docs.datadoghq.com/synthetics/cicd_integrations/)
