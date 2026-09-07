---
name: "api-error-reproduction"
description: "Troubleshoots API error issues: reproduce failures, trace error flows, correlate with releases, and fix root causes. Use when working with error reproduction, log analysis or when the user mentions error reproduction, log analysis."
license: "MIT"
compatibility: "Requires node.js, python, openapi, postman. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "backend"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(kubectl:*) Bash(node:*)"
---

Troubleshoots API error issues: reproduce failures, trace error flows, correlate with releases, and fix root causes.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -s -X POST http://localhost:3000/api/users -H 'Content-`, `node -e "console.log('trace_id=abc123 err=DB_TIMEOUT op=user`
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

# API Error (Troubleshooting)

Diagnoses and fixes error-handling problems in running APIs.

## When to Use
- Unexplained 5xx spikes
- Inconsistent error bodies in production
- Errors only appear after deploys

## Real Commands

```bash
# Reproduce
curl -s -X POST http://localhost:3000/api/users -H 'Content-Type: application/json' -d '{"email":"bad"}' -w '\n%{http_code}'
curl -s http://localhost:3000/api/users/999999 -w '\n%{http_code}'

# Logs
kubectl logs -l app=api --tail=200 | grep -iE 'error|exception' | tail -20

# Metrics
curl -s http://localhost:3000/metrics | grep -E 'http_errors|http_error_total' | head

# Health
curl -s http://localhost:3000/health -w '\n%{http_code}'
```

## Root Cause Checklist
- Is the error body consistent? (format issue)
- When did the spike start? (release correlation)
- Is a dependency failing? (timeouts/upstream)

## Testing
Turn each reproduction into an automated regression test.

## Best Practices
- Add trace IDs to every error response
- Alert on rate deltas, not raw counts

## Capabilities

### error-reproduction
Reproduce error conditions with curl and scenario payloads

**Parameters:**
- `url` (string): Endpoint to probe
- `method` (string): HTTP method

**Commands:**
- `curl -s -X POST http://localhost:3000/api/users -H 'Content-Type: application/json' -d '{"email":"bad"}' -w '\n%{http_code}'`
- `curl -s http://localhost:3000/api/users/999999 -w '\n%{http_code}'`
- `curl -s -X PUT http://localhost:3000/api/users/1 -H 'Content-Type: application/json' -d '{"email":"x@y.z"}' -w '\n%{http_code}'`
- `curl -s -X DELETE http://localhost:3000/api/users/1 -w '\n%{http_code}'`
- `curl -s -H 'Authorization: Bearer invalid' http://localhost:3000/api/me -w '\n%{http_code}'`

**Examples:**
- curl -s -X POST http://localhost:3000/api/users -H 'Content-Type: application/json' -d '{"email":"bad"}' -w '\n%{http_code}'
- curl -s http://localhost:3000/api/users/999999 -w '\n%{http_code}'
- curl -s -H 'Authorization: Bearer invalid' http://localhost:3000/api/me -w '\n%{http_code}'

### log-analysis
Correlate errors in logs and metrics to find root causes

**Parameters:**
- `pattern` (string): Log filter pattern
- `lines` (string): Number of log lines

**Commands:**
- `node -e "console.log('trace_id=abc123 err=DB_TIMEOUT op=users.list')"`
- `curl -s http://localhost:3000/metrics | grep -E 'http_errors|http_error_total' | head`
- `kubectl logs -l app=api --tail=200 | grep -iE 'error|exception' | tail -20`
- `node -e "const r=require('os');console.log('pid',process.pid,'load',r.loadavg()[0])"`
- `curl -s http://localhost:3000/health -w '\n%{http_code}'`

**Examples:**
- kubectl logs -l app=api --tail=200 | grep -iE 'error|exception' | tail -20
- curl -s http://localhost:3000/metrics | grep -E 'http_errors|http_error_total' | head
- curl -s http://localhost:3000/health -w '\n%{http_code}'

## References
- [kubectl Logs](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_logs/)
- [Prometheus Metrics](https://prometheus.io/docs/instrumenting/writing_exporters/)
