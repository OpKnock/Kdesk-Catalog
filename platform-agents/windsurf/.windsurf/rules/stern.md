---
trigger: glob
description: "Tails and aggregates logs from multiple Kubernetes pods with regex matching using stern: multi-pod, multi-container, and namespace-wide views. Use when working with multi pod tailing, filtering and format, devops or when the user mentions multi pod tailing, filtering and format, devops."
globs: ["**/*.go", "**/*.r", "**/*.sh"]
---

Tails and aggregates logs from multiple Kubernetes pods with regex matching using stern: multi-pod, multi-container, and namespace-wide views.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `stern web-*`, `stern web -i 'GET /health'`
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

# stern Multi-Pod Logging

Tail logs across many pods at once with regex matching.

## What This Skill Does

- Matches multiple pods with a single regex
- Aggregates logs chronologically with pod prefixes
- Filters by include/exclude regexes
- Supports multi-container pods and all-namespace scans
- Customizes output with Go templates

## When to Use

- Debugging across a deployment's replicas
- Correlation across API + worker pods
- Live log monitoring during incidents

## Real Commands

```bash
# Basic tailing
stern web-*                      # all web pods
stern '^api-.*' -n app
stern web -A                     # all namespaces
stern web -c sidecar             # specific container
stern web --tail 200

# Filtering
stern web -i 'ERROR|WARN'        # include
stern web -e 'health-check'      # exclude
stern web --since 30m

# Format
stern web --timestamps
stern web --no-color
stern web --template '{{.PodName}} {{.Message}}'
stern web --max-log-requests 20
```

## Templates

- `{{.Namespace}} {{.PodName}} {{.ContainerName}} {{.Message}}`

## Best Practices

- Quote regexes containing special chars: `stern 'web-[0-9]+'`
- Use -e to drop noisy health-check lines during incidents
- Pin --max-log-requests to avoid API throttling on big deployments
- Pair with --since for bounded time windows
- Use --timestamps when correlating with metrics dashboards

## Capabilities

### multi-pod-tailing
Tail logs from pod groups matched by regex across namespaces.

**Parameters:**
- `pattern` (string): Pod name regex, e.g. web-*
- `namespace` (string): Namespace scope
- `exclude` (string): Regex to exclude lines

**Commands:**
- `stern web-*`
- `stern '^api-.*' -n app`
- `stern web --all-namespaces`
- `stern web -A -e 'ERROR'`
- `stern web -c sidecar`
- `stern web --tail 200`

**Examples:**
- stern web-*
- stern '^api-.*' -n app
- stern web -A -e 'ERROR'

### filtering-and-format
Filter lines, colorize, and control timestamps and output.

**Parameters:**
- `include` (string): Regex to include lines
- `since` (string): Look back window, e.g. 30m
- `template` (string): Go template for output

**Commands:**
- `stern web -i 'GET /health'`
- `stern web -n app --timestamps`
- `stern web --since 30m`
- `stern web --no-color`
- `stern web --template '{{.PodName}} {{.Message}}'`
- `stern web --max-log-requests 20`

**Examples:**
- stern web -i 'GET /health'
- stern web --since 30m
- stern web --template '{{.PodName}} {{.Message}}'

## References
- [stern GitHub](https://github.com/stern/stern)
- [stern Documentation](https://stern.io/)
