---
trigger: glob
description: "Tails and aggregates logs from multiple Kubernetes pods with regex matching using stern: multi-pod, multi-container, and namespace-wide views."
globs: ["**/*.go", "**/*.r", "**/*.sh"]
---

# stern

Tails and aggregates logs from multiple Kubernetes pods with regex matching using stern: multi-pod, multi-container, and namespace-wide views.

## Instructions

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
