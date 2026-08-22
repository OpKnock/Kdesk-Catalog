# Owasp Zap

DAST security testing with OWASP ZAP: full scans, API scans, and automated findings reports.

## Instructions

# OWASP ZAP

Active web application security scanner (DAST). Automates spidering and
active scanning to find injection, XSS, and misconfiguration issues.

## When to Use

- Testing a web app before release
- Scanning an API defined in OpenAPI/SOAP/GraphQL
- Recurring scheduled scans against staging

## Real Commands

```bash
# Start in daemon mode
zap.sh -daemon -port 8080 -config api.key=changeme

# Full scan (spider + active)
zap-full-scan.py -t https://staging.example.com -r report.html

# API scan from an OpenAPI definition
zap-api-scan.py -t https://api.example.com/openapi.json -f openapi -r api-report.html

# Quick targeted scan with zap-cli
zap-cli quick-scan -s xss,sqli https://target.com

# Spider only
zap-cli spider https://target.com

# Active scan with context
zap-cli active-scan -r https://target.com --context=prod
```

## Report Formats

```bash
zap-full-scan.py -t https://app.example.com -J report.json   # JSON
zap-full-scan.py -t https://app.example.com -x report.xml    # XML
zap-full-scan.py -t https://app.example.com -z "-config report.generateConfidence=true"
```

## Best Practices

- Run against staging, never production, without explicit approval
- Set `-D` (delay) or low thread counts on fragile apps
- Authenticate via ZAP authentication scripts or an authenticated context file
- Triage by risk (High/Medium/Low), confirm false positives manually
- Keep the daemon's api.key secret

## Example Response

Summarizes alerts by risk level with URLs and descriptions; the agent maps each
finding to the CWE and suggests a fix.

## Capabilities

### zap-scans
Run ZAP daemon, full scans, API scans, and spidering against web targets

**Commands:**
- `zap.sh -daemon -port 8080 -config api.key=changeme`
- `zap-full-scan.py -t https://target.com -r report.html`
- `zap-api-scan.py -t http://localhost:8080/openapi.json -f openapi -r api-report.html`
- `zap-cli quick-scan -s xss,sqli https://target.com`
- `zap-cli active-scan -r https://target.com`

**Examples:**
- zap-full-scan.py -t http://localhost:8080 -J report.json
- zap-api-scan.py -t http://localhost:8080/swagger.json -f openapi -a
- zap-cli spider https://target.com