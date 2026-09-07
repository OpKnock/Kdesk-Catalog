---
type: agent_requested
description: "Operates New Relic APM agents, runs NRQL queries against telemetry, searches entities, and manages dashboards and alert conditions via the New Relic CLI. Use when working with newrelic apm operations, api or when the user mentions newrelic apm operations, api."
---

Operates New Relic APM agents, runs NRQL queries against telemetry, searches entities, and manages dashboards and alert conditions via the New Relic CLI.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `newrelic entity search --name "my-app"`
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

# New Relic Monitoring

Instrument apps with New Relic APM and drive it from the CLI for instant answers.

## What this skill does

- Installs and configures APM agents
- Runs NRQL queries against telemetry
- Manages entities and dashboards

## When to use

- Debugging slow transactions
- Verifying agent health after deployment

## Real commands

```bash
# Entity search
newrelic entity search --name "my-app"
newrelic entity search --domain APM --type APPLICATION

# NRQL queries
newrelic nrql "SELECT count(*) FROM Transaction SINCE 1 hour ago"
newrelic nrql "SELECT average(duration) FROM Transaction WHERE appName = 'my-app' SINCE 1 day ago"

# GraphQL access
newrelic nerdgraph query --apiKey $NR_API_KEY \
  --query '{ actor { account(id: 1) { name } } }'

# Agent diagnostics
newrelic diagnostics run
```

## APM agent config (Node example)

```env
NEW_RELIC_LICENSE_KEY=xxxx
NEW_RELIC_APP_NAME=my-app
NEW_RELIC_LOG_LEVEL=info
```

```js
require('newrelic');
```

## Best practices

- Use the same app name across all instances
- Query with explicit SINCE windows to bound cost
- Alert on NRQL conditions, not static thresholds

## Capabilities

### newrelic-apm-operations
Install APM agents, query telemetry with NRQL, and inspect entities via the New Relic CLI.

**Parameters:**
- `nrql` (string): NRQL query string
- `app_name` (string): APM application name
- `api_key` (string): New Relic API key

**Commands:**
- `newrelic entity search --name "my-app"`
- `newrelic nrql "SELECT count(*) FROM Transaction SINCE 1 hour ago"`
- `newrelic nerdgraph query --apiKey $NR_API_KEY --query '{ actor { account(id: 1) { name } } }'`
- `newrelic diagnostics run`
- `curl -s 'https://api.newrelic.com/v2/applications.json' -H 'Api-Key: $NR_API_KEY'`

**Examples:**
- newrelic nrql "SELECT average(duration) FROM Transaction WHERE appName = 'my-app' SINCE 1 day ago"
- newrelic entity search --domain APM --type APPLICATION
- newrelic diagnostics run

## References
- [New Relic Documentation](https://docs.newrelic.com/)
- [New Relic CLI GitHub](https://github.com/newrelic/newrelic-cli)