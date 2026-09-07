Processes JSON in the shell with jq: filtering, transformations, aggregation, and scripting against APIs and log streams.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `cat data.json | jq '.users[].name'`, `jq '{count: (.items | length), names: [.items[].name]}' data`
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

**Parameters:**
- `filter` (string): jq filter expression
- `file` (string): JSON file path

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

**Parameters:**
- `raw` (boolean): Output raw strings without quotes (-r)
- `compact` (boolean): Compact single-line output (-c)

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

## References
- [jq Manual](https://jqlang.github.io/jq/manual/)
- [jq Playground](https://jqplay.org/)