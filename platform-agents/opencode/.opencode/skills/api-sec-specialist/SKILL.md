---
name: "api-sec-specialist"
description: "Security-tests APIs with OWASP ZAP: automated API scans from OpenAPI, baseline scans, active scan rules, and HTML/JSON vulnerability reports. Use when working with zap api scan, zap automation or when the user mentions zap api scan, zap automation."
---

Security-tests APIs with OWASP ZAP: automated API scans from OpenAPI, baseline scans, active scan rules, and HTML/JSON vulnerability reports.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `docker run -t ghcr.io/zaproxy/zaproxy zap-api-scan.py -t htt`, `curl -s http://localhost:8080/v3/api-docs -o openapi.json`
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

**Parameters:**
- `target` (string): API URL or spec file
- `format` (string): openapi, soap, graphql
- `level` (string): Alert threshold: WARN, FAIL, PASS

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

## References
- [ZAP API Scan Docs](https://www.zaproxy.org/docs/docker/api-scan/)
- [ZAP User Guide](https://www.zaproxy.org/docs/desktop/start/)
