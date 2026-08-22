---
trigger: glob
description: "Operates New Relic APM agents, runs NRQL queries against telemetry, searches entities, and manages dashboards and alert conditions via the New Relic CLI."
globs: ["**/*.go", "**/*.json", "**/*.r", "**/*.sh"]
---

# Newrelic Monitoring

Operates New Relic APM agents, runs NRQL queries against telemetry, searches entities, and manages dashboards and alert conditions via the New Relic CLI.

## Instructions

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
