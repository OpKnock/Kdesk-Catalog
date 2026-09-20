---
name: "api-error-specialist"
description: "Deep expertise in API error handling: full error taxonomy, monitoring and alerting, and developer-facing error catalogs. Use when working with error taxonomy, error monitoring or when the user mentions error taxonomy, error monitoring."
license: "MIT"
compatibility: "Requires node.js, python, openapi, postman. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "backend"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(node:*) Bash(python:*) Bash(sentry-cli:*)"
---

Deep expertise in API error handling: full error taxonomy, monitoring and alerting, and developer-facing error catalogs.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `node -e "const t=['AUTH','VALIDATION','RATE','NOT_FOUND','CO`, `sentry-cli send-event -m 'test' --release 1.2.3`
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

# API Error Specialist

Designs and operates a complete error program: taxonomy, monitoring, and developer experience.

## When to Use
- Designing error strategy org-wide
- Reducing mean-time-to-understand incidents
- Standardizing cross-team error codes

## Real Commands

```bash
# Draft taxonomy
node -e "const t=['AUTH','VALIDATION','RATE','NOT_FOUND','CONFLICT','UPSTREAM','TIMEOUT'];console.log(t.map(c=>c+'_XXXX').join('\n'))"

# Verify no duplicate codes
node -e "const codes=require('./errors.json').map(e=>e.code);console.log(new Set(codes).size===codes.length?'no dups':'dups')"

# Ship a test event
sentry-cli send-event -m 'manual test' --release 1.2.3

# Watch error metrics
curl -s http://localhost:3000/metrics | grep error_rate | head
```

## Taxonomy Rules
- Prefix by family: `VALIDATION_`, `UPSTREAM_`, `AUTH_`
- Numeric suffix within family
- One canonical meaning per code

## Monitoring
Alert on error-rate deltas vs. baseline, not absolute counts.

## Best Practices
- Every code has a doc entry and a remediation hint
- Deprecate codes, never reuse

## Capabilities

### error-taxonomy
Design a comprehensive error code taxonomy covering client, server, and integration failures

**Parameters:**
- `prefix` (string): Error family prefix
- `schema` (string): Error schema path

**Commands:**
- `node -e "const t=['AUTH','VALIDATION','RATE','NOT_FOUND','CONFLICT','UPSTREAM','TIMEOUT'];console.log(t.map(c=>c+'_XXXX').join('\n'))"`
- `python -c "import json;print(json.dumps({'prefix':'VALIDATION_','range':[1000,1999]}))"`
- `curl -s http://localhost:3000/api/errors/schema | python -m json.tool`
- `node -e "const codes=['VALIDATION_1001','VALIDATION_1002'];console.log(codes.length+' codes defined')"`
- `python -c "print(' '.join(['%04d'%i for i in range(1000,1005)]))"`

**Examples:**
- node -e "const t=['AUTH','VALIDATION','RATE','NOT_FOUND','CONFLICT','UPSTREAM','TIMEOUT'];console.log(t.map(c=>c+'_XXXX').join('\n'))"
- curl -s http://localhost:3000/api/errors/schema | python -m json.tool
- node -e "const codes=require('./errors.json').map(e=>e.code);console.log(new Set(codes).size===codes.length?'no dups':'dups found')"

### error-monitoring
Track error rates, correlate with deploys, and alert on regressions

**Parameters:**
- `release` (string): Release version
- `metric` (string): Metric to query

**Commands:**
- `sentry-cli send-event -m 'test' --release 1.2.3`
- `curl -s -X POST http://localhost:3000/api/monitor/errors -H 'Content-Type: application/json' -d '{"code":"TIMEOUT","count":42}'`
- `node -e "const r=require('os');console.log('uptime',r.uptime())"`
- `curl -s http://localhost:3000/metrics | grep -E 'http_errors_total|http_error_rate'`
- `sentry-cli releases list`

**Examples:**
- sentry-cli send-event -m 'manual test' --release 1.2.3
- curl -s http://localhost:3000/metrics | grep error_rate | head
- sentry-cli releases list | head -5

## References
- [Sentry CLI](https://docs.sentry.io/cli/)
- [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457)
- [OpenTelemetry Errors](https://opentelemetry.io/docs/specs/otel/)
