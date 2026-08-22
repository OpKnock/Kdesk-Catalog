---
name: "firebase-crashlytics"
description: "Inspect crash issues, upload symbols, and manage release reporting. and verify symbol uploads for readable stack traces.'"
type: knowledge
triggers: ["firebase-crashlytics", "crashlytics-ops"]
---

# Firebase Crashlytics

Inspect crash issues, upload symbols, and manage release reporting. and verify symbol uploads for readable stack traces.'

## Instructions

# Firebase Crashlytics

## What this skill does

Crashlytics aggregates app crashes into issues with stack traces, device data, and release context. The CLI uploads symbols; the REST API queries issues and reports for automation.

## When to use

- Triaging the top crash after a release
- Making native stack traces readable (symbol upload)
- Building crash dashboards from the API

## Real commands

```bash
# Upload native symbols
firebase crashlytics:symbols:upload --app com.example.app ./build/app.so

# List recent crash reports
firebase crashlytics:reports:list

# Query fatal issues via the API
curl -s 'https://firebase.googleapis.com/v1beta1/projects/$PROJECT_ID/crashlytics/issues' -H 'Authorization: Bearer $ACCESS_TOKEN' | jq '.issues[] | {issueId, title, fatal}'

# Issue detail with sessions
curl -s 'https://firebase.googleapis.com/v1beta1/projects/$PROJECT_ID/crashlytics/issues/$ISSUE_ID' -H 'Authorization: Bearer $ACCESS_TOKEN' | jq '.sessions[0].appVersion'
```

## Symbol upload in CI

```bash
# iOS dSYMs before release
find . -name '*.dSYM' -exec firebase crashlytics:symbols:upload --app com.example.app {} \;
```

## Testing

```bash
# Force a crash in a debug build and confirm the issue appears
firebase crashlytics:reports:list | grep -i 'test-crash'
```

## Best practices

- Upload symbols in CI on every release; without them native traces are unusable.
- Monitor fatality rate (fatal vs non-fatal) per release, not just crash count.
- Tag releases with the same version the app reports.
- Integrate with issue trackers for auto-triage.
- Keep crash-free sessions percentage in the weekly report.

## Capabilities

### crashlytics-ops
Inspect crash issues, upload symbols, and manage release reporting.

**Commands:**
- `curl -s 'https://firebase.googleapis.com/v1beta1/projects/$PROJECT_ID/crashlytics/issues' -H 'Authorization: Bearer $ACCESS_TOKEN' | jq '.issues[0] | {issueId, title, fatal}'`
- `curl -s 'https://firebase.googleapis.com/v1beta1/projects/$PROJECT_ID/crashlytics/issues/$ISSUE_ID' -H 'Authorization: Bearer $ACCESS_TOKEN' | jq '.sessions[0].appVersion'`
- `firebase crashlytics:symbols:upload --app com.example.app ./build/app.so`
- `firebase crashlytics:reports:list`
- `curl -s 'https://firebase.googleapis.com/v1beta1/projects/$PROJECT_ID/crashlytics/reports' -H 'Authorization: Bearer $ACCESS_TOKEN' | jq '.reports | length'`

**Examples:**
- firebase crashlytics:symbols:upload --app com.example.app ./build/app.so
- curl -s 'https://firebase.googleapis.com/v1beta1/projects/$PROJECT_ID/crashlytics/issues' -H 'Authorization: Bearer $ACCESS_TOKEN' | jq '.issues[] | {issueId, title, fatal}'
- firebase crashlytics:reports:list
