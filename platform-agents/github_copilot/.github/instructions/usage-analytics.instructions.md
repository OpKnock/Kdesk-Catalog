---
applyTo: "**/*.json **/*.py **/*.r **/*.sh"
---

# Usage Analytics

Tracks product usage events and queries analytics APIs. Sends custom events to Plausible and Mixpanel, retrieves aggregate statistics and time-series data for dashboards, and imports historical event data via API.

## Instructions

# Usage Analytics

Hand-crafted skill for product usage analytics.

## What this skill does

- Ingests custom events (signups, upgrades, clicks)
- Queries aggregates and time series over pageviews
- Loads historical events into Mixpanel-style services

## When to use

- Instrumenting a feature with custom events
- Answering "how many X in the last 30 days?"
- Wiring analytics into CI or dashboards

## Real commands

```bash
# Send a custom event to Plausible
curl -X POST https://plausible.io/api/event -H "Content-Type: application/json" -d "{\"domain\":\"app.your-app.test\",\"name\":\"signup\",\"url\":\"https://app.your-app.test/signup\",\"props\":{\"plan\":\"pro\"}}"

# Aggregate stats
curl -s "https://plausible.io/api/v1/stats/aggregate?site_id=app.your-app.test&period=30d&metrics=visitors,pageviews" -H "Authorization: Bearer YOUR_API_KEY" | jq

# Time series for charts
curl -s "https://plausible.io/api/v1/stats/timeseries?site_id=app.your-app.test&period=30d&metrics=pageviews" -H "Authorization: Bearer KEY" | jq

# Mixpanel import of historical events
curl -s "https://api.mixpanel.com/import?strict=1" -H "Authorization: Basic BASE64" -H "Content-Type: application/json" -d "[{\"event\":\"signup\",\"properties\":{\"token\":\"TOKEN\",\"distinct_id\":\"u1\",\"time\":1700000000}}]"
```

## Event schema

- name: action verb (signup, upgrade, invite_sent)
- url: canonical page for the event
- props: flat custom properties
- user_id/distinct_id: stable per user

## Testing

```bash
curl -X POST https://plausible.io/api/event -H "Content-Type: application/json" -d "{\"domain\":\"app.your-app.test\",\"name\":\"test_event\",\"url\":\"https://app.your-app.test/\"}"

# then confirm it in the stats API timeseries
```

## Best practices

- Keep event names a small controlled vocabulary
- Never send PII in props
- Use one canonical URL format to avoid dupes

## Capabilities

### analytics-events
Collect and query product usage events

**Commands:**
- `curl -X POST https://plausible.io/api/event -H "Content-Type: application/json" -d "{\"domain\":\"app.your-app.test\",\"name\":\"signup\",\"url\":\"https://app.your-app.test/signup\",\"props\":{\"plan\":\"pro\"}}"`
- `curl -s "https://plausible.io/api/v1/stats/aggregate?site_id=app.your-app.test&period=30d&metrics=visitors,pageviews" -H "Authorization: Bearer $PLAUSIBLE_API_KEY" | jq`
- `curl -s "https://api.mixpanel.com/import?strict=1" -H "Authorization: Basic base64" -H "Content-Type: application/json" -d "[{\"event\":\"signup\",\"properties\":{\"token\":\"$MIXPANEL_TOKEN\",\"distinct_id\":\"u1\",\"time\":1700000000}}]"`
- `python -c "import json,requests; print(json.dumps({\"ok\":True}))"`
- `curl -s "https://plausible.io/api/v1/stats/timeseries?site_id=app.your-app.test&period=30d&metrics=pageviews" -H "Authorization: Bearer KEY" | jq`

**Examples:**
- curl -X POST https://plausible.io/api/event -H "Content-Type: application/json" -d "{\"domain\":\"app.your-app.test\",\"name\":\"signup\",\"url\":\"https://app.your-app.test/signup\"}"
- curl -s "https://plausible.io/api/v1/stats/aggregate?site_id=app.your-app.test&period=30d&metrics=visitors,pageviews" -H "Authorization: Bearer KEY" | jq
- curl -s "https://plausible.io/api/v1/stats/timeseries?site_id=app.your-app.test&period=7d&metrics=pageviews" -H "Authorization: Bearer KEY" | jq
