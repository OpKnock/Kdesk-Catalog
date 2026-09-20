---
name: "Api Analytics Privacy"
description: "Privacy-preserving API analytics - anonymize PII with Presidio, aggregate without raw data, and comply with GDPR data minimization. Use when working with privacy analytics or when the user mentions privacy analytics."
globs: ["**/*.json", "**/*.py", "**/*.r", "**/*.sh"]
alwaysApply: false
---

Privacy-preserving API analytics - anonymize PII with Presidio, aggregate without raw data, and comply with GDPR data minimization.

## Agentic Workflow: Read -> Reason -> Act (api-analytics-privacy)

You are **Api Analytics Privacy** (sre) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — sre context for `api-analytics-privacy`
- Domain: Privacy-preserving API analytics - anonymize PII with Presidio, aggregate without raw data, and comply with GDPR data minimization.
- **privacy-analytics**: Anonymize PII and run privacy-safe aggregations — `pip install presidio-analyzer presidio-anonymizer`
- Check `knowledge` and `prerequisites: prometheus, grafana, elasticsearch`

### 2. Reason — think for `api-analytics-privacy`
- For `privacy-analytics`: Anonymize PII and run privacy-safe aggregations — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-analytics-privacy` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Presidio-analyzer` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-analytics-privacy:ad1d8f6c`

# API Analytics (Privacy-preserving)

## What this skill does
Run analytics without exposing personal data: detect and anonymize PII with Presidio before analytics pipelines, aggregate on pseudonymous dimensions, and set retention policies.

## When to use
- Collecting analytics containing emails, phones, or credit cards
- GDPR / CCPA compliance for analytics
- Sharing datasets with partners

## Real commands
```bash
# Install
pip install presidio-analyzer presidio-anonymizer

# Detect PII in text
presidio-analyzer --text 'Call me at 555-1234 or email alice@example.com'

# Anonymize a stream
python anonymize.py --input events.jsonl \
  --output events_safe.jsonl \
  --entities EMAIL_ADDRESS,PHONE_NUMBER,CREDIT_CARD

# Redact instead of replace
python anonymize.py --input events.jsonl \
  --output events_safe.jsonl \
  --entities PERSON,EMAIL_ADDRESS --operator redact

# Aggregates only on safe dimensions
curl -s 'http://localhost:8080/api/analytics/aggregate?dimension=country' | jq '.rows | length'

# Check retention config
curl -s http://localhost:8080/api/analytics/privacy/retention | jq '.days'
```

## Anonymization strategies
- redact: remove the value
- replace: substitute a placeholder
- hash: SHA-256 pseudonymization (still linkable)
- encrypt: reversible for support use

## Best practices
- Anonymize before writing to analytics storage
- Keep raw data in a locked data lake with retention limits
- Never send PII to third-party analytics vendors
- Document the legal basis for each event property

## Testing
```bash
presidio-analyzer --text 'email alice@example.com' | jq '.recognized_entities'
curl -s http://localhost:8080/api/analytics/privacy/retention | jq '.days'
```

## Capabilities

### privacy-analytics
Anonymize PII and run privacy-safe aggregations

**Parameters:**
- `entities` (string): Comma-separated PII entity types to remove
- `operator` (string): redact, replace, or hash
- `input` (string): Input events file

**Commands:**
- `pip install presidio-analyzer presidio-anonymizer`
- `presidio-analyzer --text 'Call me at 555-1234 or email alice@localhost'`
- `presidio-anonymizer --analyzer_result /tmp/analysis.json --text 'alice@localhost called'`
- `python anonymize.py --input events.jsonl --output events_safe.jsonl --entities EMAIL_ADDRESS,PHONE_NUMBER,CREDIT_CARD`
- `curl -s http://localhost:8080/api/analytics/aggregate?dimension=country | jq '.rows | length'`

**Examples:**
- presidio-analyzer --text 'SSN 123-45-6789' --language en
- python anonymize.py --input events.jsonl --output events_safe.jsonl --entities PERSON,EMAIL_ADDRESS --operator redact
- curl -s http://localhost:8080/api/analytics/privacy/retention | jq '.days'

## References
- [Microsoft Presidio](https://microsoft.github.io/presidio/)
- [GDPR Data Minimization](https://gdpr-info.eu/art-5-gdpr/)