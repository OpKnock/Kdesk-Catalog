---
name: "jq"
description: "Processes JSON in the shell with jq: filtering, transformations, aggregation, and scripting against APIs and log streams."
---

# jq

Processes JSON in the shell with jq: filtering, transformations, aggregation, and scripting against APIs and log streams.

## Instructions

# jq JSON Processing

Query, transform, and aggregate JSON from the command line.

## What This Skill Does

- Filters and extracts values from JSON documents
- Selects objects by conditions
- Builds new JSON objects and arrays
- Aggregates with group_by, length, add
- Formats output (raw, compact, colored)
- Powers API pipelines: curl | jq

## When to Use

- Inspecting API responses in the shell
- Parsing Kubernetes/cloud CLI JSON output
- Data wrangling in pipelines

## Real Commands

```bash
# Extract
cat data.json | jq '.users[].name'
jq '.items[] | select(.status == "open")' data.json
jq '.total' data.json

# Transform
jq '{count: (.items | length), names: [.items[].name]}' data.json
jq '[.items[] | {name, size}] | sort_by(.size) | reverse' data.json
jq 'map(.price) | add / length' data.json
jq -n '{hello: "world", arr: [1,2,3]}'

# Output modes
jq -r '.items[] | "\(.name)	\(.id)"' data.json
jq -c '.items[]' data.json
curl -s https://api.example.com/data | jq '.result'
```

## Best Practices

- Use -r for unquoted output (CSV, TSV, shell assignment)
- Use select() early in pipelines for performance
- Quote filters in single quotes to protect shell expansion
- Prefer jq for ad-hoc; SQL or duckdb for large data analysis
- Use --arg to inject shell variables: jq --arg name "$N" '.name=$name'

## Capabilities

### query-and-filter
Extract and filter values from JSON documents.

**Commands:**
- `cat data.json | jq '.users[].name'`
- `jq '.items[] | select(.status == "open")' data.json`
- `jq '.[] | {name, id}' data.json`
- `jq '.total' data.json`
- `jq 'has("errors")' data.json`
- `curl -s http://localhost:8080/data | jq '.result'`

**Examples:**
- jq '.users[].name' data.json
- jq '.items[] | select(.status == "open")' data.json
- curl -s http://localhost:8080/data | jq '.result'

### transform-and-aggregate
Build new JSON, group, count, and reshape data.

**Commands:**
- `jq '{count: (.items | length), names: [.items[].name]}' data.json`
- `jq 'group_by(.kind) | map({kind: .[0].kind, count: length})' data.json`
- `jq '[.items[] | {name, size}] | sort_by(.size) | reverse' data.json`
- `jq -r '.items[] | "\(.name)\t\(.id)"' data.json`
- `jq 'map(.price) | add / length' data.json`
- `jq -n '{hello: "world", arr: [1,2,3]}'`

**Examples:**
- jq 'group_by(.kind) | map({kind: .[0].kind, count: length})' data.json
- jq -r '.items[] | "\(.name)\t\(.id)"' data.json
- jq 'map(.price) | add / length' data.json
