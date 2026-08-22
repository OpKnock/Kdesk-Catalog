---
applyTo: "**/*.json **/*.py **/*.r **/*.sh"
---

# api-error-specialist

Deep expertise in API error handling: full error taxonomy, monitoring and alerting, and developer-facing error catalogs.

## Instructions

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
