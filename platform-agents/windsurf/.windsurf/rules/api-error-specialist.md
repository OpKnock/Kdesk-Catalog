---
trigger: glob
description: "Deep expertise in API error handling: full error taxonomy, monitoring and alerting, and developer-facing error catalogs. Use when working with error taxonomy, error monitoring or when the user mentions error taxonomy, error monitoring."
globs: ["**/*.json", "**/*.py", "**/*.r", "**/*.sh"]
---

Deep expertise in API error handling: full error taxonomy, monitoring and alerting, and developer-facing error catalogs.

## Agentic Workflow: Read -> Reason -> Act (api-error-specialist)

You are **api-error-specialist** (backend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `api-error-specialist`
- Domain: Deep expertise in API error handling: full error taxonomy, monitoring and alerting, and developer-facing error catalogs.
- **error-taxonomy**: Design a comprehensive error code taxonomy covering client, server, and integration failures — `node -e "const t=['AUTH','VALIDATION','RATE','NOT_FOUND','CONFLICT','UPSTREAM','`
- **error-monitoring**: Track error rates, correlate with deploys, and alert on regressions — `sentry-cli send-event -m 'test' --release 1.2.3`
- Check `knowledge` and `prerequisites: node.js, python, openapi`

### 2. Reason — think for `api-error-specialist`
- For `error-taxonomy`: Design a comprehensive error code taxonomy covering client, server, and integration failures — decide which checks to run
- For `error-monitoring`: Track error rates, correlate with deploys, and alert on regressions — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-error-specialist` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Sentry-cli` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-error-specialist:6239b956`

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
