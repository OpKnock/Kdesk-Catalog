---
type: agent_requested
description: "Error tracking and release monitoring with Sentry: upload source maps, query issues, manage releases, and analyze crash reports."
---

# Error Tracking

Error tracking and release monitoring with Sentry: upload source maps, query issues, manage releases, and analyze crash reports.

## Instructions

# Error Tracking

## What this skill does

Error tracking collects stack traces, groups them into issues, and ties them to releases. This skill covers Sentry operations: creating releases, uploading source maps, querying issues, and validating event ingestion.

## When to use

- Deploying a release and confirming source maps match
- Triaging the most frequent errors after a launch
- Automating release tracking in CI

## Real commands

```bash
# Create and finalize a release
sentry-cli releases new -p my-project 1.2.3
sentry-cli releases set-commits --auto 1.2.3
sentry-cli releases finalize 1.2.3

# Upload source maps so stack traces are readable
sentry-cli sourcemaps upload -p my-project --release 1.2.3 ./dist/assets

# List unresolved issues from the API
curl -s 'https://sentry.io/api/0/projects/org/project/issues/?query=is:unresolved&statsPeriod=24h' -H 'Authorization: Bearer $SENTRY_TOKEN' | jq '.[] | {id: .id, title: .title, count: .count}'

# Verify uploaded artifacts
sentry-cli debug-files list -p my-project --release 1.2.3
```

## CI release step example

```bash
sentry-cli releases new -p my-project "$CI_COMMIT_SHA"
sentry-cli releases set-commits --auto "$CI_COMMIT_SHA"
sentry-cli sourcemaps upload -p my-project --release "$CI_COMMIT_SHA" ./dist/assets
sentry-cli releases finalize "$CI_COMMIT_SHA"
```

## Testing

```bash
# Send a test event to verify ingestion
curl -s -X POST 'https://sentry.io/api/0/store/' -H 'Content-Type: application/json' -H "X-Sentry-Auth: sentry_key=$SENTRY_DSN_KEY" -d '{"message":"test event","event_id":"id1234567890abcdef"}' | jq
```

## Best practices

- Upload source maps with the exact release tag your SDK reports.
- Use `--auto` for set-commits so each release links to git history.
- Set up ownership rules to route issues to the right team.
- Mark resolved issues with a comment referencing the fixing release.
- Monitor unresolved issue count, not total volume, in dashboards.

## Capabilities

### sentry-ops
Manage Sentry releases, upload artifacts, query issues, and inspect events.

**Commands:**
- `sentry-cli releases new -p my-project 1.2.3`
- `sentry-cli releases set-commits --auto 1.2.3`
- `sentry-cli sourcemaps upload -p my-project --release 1.2.3 ./dist/assets`
- `curl -s 'https://sentry.io/api/0/projects/org/project/issues/?query=is:unresolved&statsPeriod=24h' -H 'Authorization: Bearer $SENTRY_TOKEN' | jq '.[] | {id: .id, title: .title, count: .count}'`
- `sentry-cli releases finalize 1.2.3`
- `sentry-cli debug-files list -p my-project --release 1.2.3`

**Examples:**
- sentry-cli releases new -p my-project 1.2.3 && sentry-cli releases set-commits --auto 1.2.3
- sentry-cli sourcemaps upload -p my-project --release 1.2.3 ./dist/assets
- curl -s 'https://sentry.io/api/0/projects/org/project/issues/?query=is:unresolved&statsPeriod=24h' -H 'Authorization: Bearer $SENTRY_TOKEN' | jq '.[] | {title: .title, count: .count}'