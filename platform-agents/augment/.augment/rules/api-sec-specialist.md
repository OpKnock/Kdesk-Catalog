---
type: agent_requested
description: "Security-tests APIs with OWASP ZAP: automated API scans from OpenAPI, baseline scans, active scan rules, and HTML/JSON vulnerability reports."
---

# api-sec-specialist

Security-tests APIs with OWASP ZAP: automated API scans from OpenAPI, baseline scans, active scan rules, and HTML/JSON vulnerability reports.

## Instructions

# API Security Specialist

Automated API security testing with ZAP.

## What This Skill Does
- Scans APIs for OWASP top-ten vulnerabilities
- Uses OpenAPI specs to discover endpoints
- Produces actionable reports

## When to Use
- Pre-release security gates
- Continuous security monitoring
- PCI/SOC2 audit evidence

## Real Commands

```bash
docker run -t ghcr.io/zaproxy/zaproxy zap-api-scan.py -t openapi.yaml -f openapi -j -l WARN -r report.html
docker run -t ghcr.io/zaproxy/zaproxy zap-baseline.py -t https://api.example.com -r zap_baseline.html
```

## Scan Workflow
1. Export the OpenAPI spec
2. Run the API scan with the spec
3. Triage alerts by confidence
4. Track findings in the bug tracker

## Testing
- Verify the scanner reaches authenticated endpoints
- Set up authentication headers for deep scans
- Fail CI on HIGH/CRITICAL alerts

## Best Practices
- Scan staging, never production
- Keep the spec in sync with routes
- Tune scan rules to reduce false positives

## Capabilities

### zap-api-scan
Run ZAP automated scans against APIs

**Commands:**
- `docker run -t ghcr.io/zaproxy/zaproxy zap-api-scan.py -t http://localhost:8080/v3/api-docs -f openapi -O -r zap_api_report.html`
- `docker run -t ghcr.io/zaproxy/zaproxy zap-baseline.py -t http://localhost:8080 -r zap_baseline.html`
- `docker run -t ghcr.io/zaproxy/zaproxy zap-api-scan.py -t openapi.yaml -f openapi -j -l WARN -r report.html`
- `docker run -t ghcr.io/zaproxy/zaproxy zap-cli.py --help`

**Examples:**
- zap-api-scan.py -f openapi scans from the OpenAPI spec
- zap-baseline.py runs a passive baseline scan
- -l WARN sets the minimum alert level reported

### zap-automation
Automate ZAP scans in CI pipelines

**Commands:**
- `curl -s http://localhost:8080/v3/api-docs -o openapi.json`
- `docker run -t ghcr.io/zaproxy/zaproxy zap-api-scan.py -t openapi.json -f openapi -J -j -l FAIL -r report.html`
- `curl -s http://localhost:8080/health -o /dev/null -w '%{http_code}\n'`

**Examples:**
- -cli --help
- -api --help