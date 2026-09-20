---
name: "api-error-reproduction"
description: "Troubleshoots API error issues: reproduce failures, trace error flows, correlate with releases, and fix root causes."
---

# Api Error Reproduction

Troubleshoots API error issues: reproduce failures, trace error flows, correlate with releases, and fix root causes.

## Instructions

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
