Firebase Analytics operations: export events, query event data from BigQuery, manage measurement settings, and debug event flows with the Firebase CLI.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `firebase projects:list`
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

# Firebase Analytics

## What this skill does

Firebase Analytics collects app and web events automatically. Power users export raw events to BigQuery and run SQL against `events_*` tables for custom reporting beyond the console.

## When to use

- Verifying events fire correctly after a release
- Building custom funnels or user cohorts in BigQuery
- Setting up export before analytics dashboards go live

## Real commands

```bash
# Project context
firebase projects:list

# Trigger/verify the BigQuery export
firebase analytics:export

# Top events today from BigQuery
bq query --use_legacy_sql=false 'SELECT event_name, COUNT(*) AS cnt FROM `project.analytics_123456.events_*` WHERE _TABLE_SUFFIX = FORMAT_DATE("%Y%m%d", CURRENT_DATE()) GROUP BY event_name ORDER BY cnt DESC LIMIT 20'

# Recent raw events for debugging
bq query --use_legacy_sql=false 'SELECT event_date, event_timestamp, event_name, user_pseudo_id FROM `project.analytics_123456.events_*` WHERE event_name = "add_to_cart" ORDER BY event_timestamp DESC LIMIT 10'
```

## Common queries

```sql
-- Funnel: view_item -> add_to_cart -> begin_checkout -> purchase
SELECT
  COUNTIF(event_name = 'view_item') AS viewed,
  COUNTIF(event_name = 'add_to_cart') AS added,
  COUNTIF(event_name = 'begin_checkout') AS checked,
  COUNTIF(event_name = 'purchase') AS purchased
FROM `project.analytics_123456.events_*`
WHERE _TABLE_SUFFIX >= FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY))
```

## Testing

```bash
# Fire a debug event and watch it appear in BigQuery (allow ~10-60 min latency)
bq query --use_legacy_sql=false 'SELECT COUNT(*) FROM `project.analytics_123456.events_*` WHERE event_name = "test_event"'
```

## Best practices

- Enable BigQuery export at project setup; backfills are manual after that.
- Always filter on `_TABLE_SUFFIX` (dates) to keep queries cheap.
- Use `event_timestamp` (microseconds) not event_date for ordering.
- Check the console's DebugView for real-time validation, BigQuery for reporting.

## Capabilities

### analytics-ops
Manage Firebase Analytics projects, export data, and query events.

**Parameters:**
- `project-id` (string): Firebase project id
- `dataset-id` (string): BigQuery dataset holding analytics events
- `date` (string): YYYYMMDD date suffix for events tables

**Commands:**
- `firebase projects:list`
- `firebase analytics:export`
- `bq query --use_legacy_sql=false 'SELECT event_name, COUNT(*) AS cnt FROM `project.analytics_123456.events_*` WHERE _TABLE_SUFFIX = FORMAT_DATE("%Y%m%d", CURRENT_DATE()) GROUP BY event_name ORDER BY cnt DESC LIMIT 20'`
- `firebase analytics:data:events`
- `gcloud firebase analytics --help`

**Examples:**
- bq query --use_legacy_sql=false 'SELECT event_name, COUNT(*) AS cnt FROM `project.analytics_123456.events_*` WHERE _TABLE_SUFFIX = FORMAT_DATE("%Y%m%d", CURRENT_DATE()) GROUP BY event_name ORDER BY cnt DESC LIMIT 20'
- firebase analytics:export
- firebase projects:list

## References
- [Firebase Analytics docs](https://firebase.google.com/docs/analytics)
- [Analytics BigQuery export](https://firebase.google.com/docs/analytics/bigquery-export)