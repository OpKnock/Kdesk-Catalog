---
type: agent_requested
description: "Anonymizes and masks test data for safe environments: Presidio PII redaction, jq field masking, and synthetic data generation for compliance. Use when working with presidio redaction, field masking or when the user mentions presidio redaction, field masking."
---

Anonymizes and masks test data for safe environments: Presidio PII redaction, jq field masking, and synthetic data generation for compliance.

## Agentic Workflow: Read -> Reason -> Act (api-test-data-presidio-redaction)

You are **Api Test Data Presidio Redaction** (testing) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — testing context for `api-test-data-presidio-redaction`
- Domain: Anonymizes and masks test data for safe environments: Presidio PII redaction, jq field masking, and synthetic data generation for compliance.
- **presidio-redaction**: Redact PII with Microsoft Presidio — `pip install presidio-analyzer presidio-anonymizer`
- **field-masking**: Mask fields with jq transformations — `curl -s http://localhost:3000/api/users | jq 'map(.email |= sub("(?<=.{3}).*(?=@`
- Check `knowledge` and `prerequisites: faker, node.js, python`

### 2. Reason — think for `api-test-data-presidio-redaction`
- For `presidio-redaction`: Redact PII with Microsoft Presidio — decide which checks to run
- For `field-masking`: Mask fields with jq transformations — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-test-data-presidio-redaction` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Presidio-anonymizer` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-test-data-presidio-redaction:d656856b`

# API Test Data v4 - Masking

PII masking and anonymization.

## What This Skill Does
- Detects PII with Presidio
- Anonymizes data for non-prod environments
- Masks fields with jq

## When to Use
- Copying prod data to staging
- Compliance with GDPR/HIPAA
- Safe shareable datasets

## Real Commands

```bash
pip install presidio-analyzer presidio-anonymizer
presidio-anonymizer --text "Contact alice@example.com or 555-1234" --language en
curl -s http://localhost:3000/api/users | jq 'map(.email |= sub("(?<=.{3}).*(?=@)"; "***"))'
```

## Masking Strategy
- Detect entities: email, phone, SSN, credit card
- Anonymize with placeholder operators
- Mask with regex sub in jq pipelines

## Testing
- Verify no original PII survives
- Confirm formats remain valid
- Test locale-specific entities


## Best Practices
- Mask before writing to disk
- Keep mapping tables encrypted
- Log anonymization transformations

## Capabilities

### presidio-redaction
Redact PII with Microsoft Presidio

**Parameters:**
- `text` (string): Input text to process
- `language` (string): Language of the input
- `entities` (array): PII entity types to detect

**Commands:**
- `pip install presidio-analyzer presidio-anonymizer`
- `presidio-anonymizer --text "Contact alice@localhost or 555-1234" --language en`
- `python -c "from presidio_anonymizer import AnonymizerEngine; from presidio_analyzer import AnalyzerEngine; a=AnalyzerEngine(); res=a.analyze(text='email: a@b.co', language='en'); print([str(r) for r in res])"`
- `python -c "from presidio_anonymizer import AnonymizerEngine; e=AnonymizerEngine(); print(e.anonymize(text='call 555-1234', analyzer_results=[]))"`

**Examples:**
- presidio-anonymizer redacts emails and phones
- AnalyzerEngine detects PII entities
- AnonymizerEngine replaces entities with placeholders

### field-masking
Mask fields with jq transformations

**Commands:**
- `curl -s http://localhost:3000/api/users | jq 'map(.email |= sub("(?<=.{3}).*(?=@)"; "***"))'`
- `curl -s http://localhost:3000/api/users | jq 'map(.phone = "***-***-0000")'`
- `curl -s http://localhost:3000/api/users | jq 'del(.[].ssn)'`

**Examples:**
- -cli --help
- -api --help

## References
- [Presidio Docs](https://microsoft.github.io/presidio/)
- [jq Manual](https://jqlang.github.io/jq/manual/)