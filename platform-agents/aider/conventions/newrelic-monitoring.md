Operates New Relic APM agents, runs NRQL queries against telemetry, searches entities, and manages dashboards and alert conditions via the New Relic CLI.

## Agentic Workflow: Read -> Reason -> Act (newrelic-monitoring)

You are **Newrelic Monitoring** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `newrelic-monitoring`
- Domain: Operates New Relic APM agents, runs NRQL queries against telemetry, searches entities, and manages dashboards and alert conditions via the New Relic CLI.
- **newrelic-apm-operations**: Install APM agents, query telemetry with NRQL, and inspect entities via the New Relic CLI. — `newrelic entity search --name "my-app"`
- Check `knowledge` and `prerequisites: newrelic`

### 2. Reason — think for `newrelic-monitoring`
- For `newrelic-apm-operations`: Install APM agents, query telemetry with NRQL, and inspect entities via the New Relic CLI. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `newrelic-monitoring` tools
- Tools: `Glob`, `Grep`, `Read`, `Newrelic`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `newrelic-monitoring:7d07b5ba`

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
