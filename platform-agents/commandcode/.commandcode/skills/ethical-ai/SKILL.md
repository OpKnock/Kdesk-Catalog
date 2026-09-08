---
name: "ethical-ai"
description: "Builds guardrails for AI systems: model vulnerability scanning with garak, supply-chain checks, PII detection, and bias assessment. Use when working with llm security scanning, data and supply chain or when the user mentions llm security scanning, data and supply chain."
license: "MIT"
compatibility: "Requires fairlearn, ai-fairness, shap, lime, tensorflow-model-analysis."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "ai"}
allowed-tools: "Glob Grep Read Bash(detect-secrets:*) Bash(garak:*) Bash(gitleaks:*) Bash(pip-audit:*) Bash(presidio-analyzer:*) Bash(python:*) Bash(scorecard:*)"
---

Builds guardrails for AI systems: model vulnerability scanning with garak, supply-chain checks, PII detection, and bias assessment.

## Agentic Workflow: Read -> Reason -> Act (ethical-ai)

You are **ethical-ai** (ai) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — ai context for `ethical-ai`
- Domain: Builds guardrails for AI systems: model vulnerability scanning with garak, supply-chain checks, PII detection, and bias assessment.
- **llm-security-scanning**: Probe LLMs for prompt injection, jailbreaks, and harmful output with garak. — `garak --model_type openai-chat --model_name gpt-4o-mini`
- **data-and-supply-chain**: Scan repos for secrets, PII, and supply-chain risks. — `gitleaks detect --source . --report-format json --report-path leak.json`
- Check `knowledge` and `prerequisites: fairlearn, ai-fairness, shap, lime`

### 2. Reason — think for `ethical-ai`
- For `llm-security-scanning`: Probe LLMs for prompt injection, jailbreaks, and harmful output with garak. — decide which checks to run
- For `data-and-supply-chain`: Scan repos for secrets, PII, and supply-chain risks. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `ethical-ai` tools
- Tools: `Glob`, `Grep`, `Read`, `Garak`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `ethical-ai:8115805e`

# Ethical AI Engineering

Build and ship AI systems with guardrails: security, privacy, and fairness.

## What This Skill Does

- Probes LLMs for injection/jailbreak vulnerabilities with garak
- Scans repos for secrets and PII
- Assesses supply-chain security with Scorecard
- Detects PII in text with Presidio
- Advises on bias testing and model documentation

## When to Use

- Releasing a new LLM-powered feature
- Auditing an AI system before deployment
- Responding to red-team findings

## Real Commands

```bash
# LLM scanning (garak)
garak --model_type openai-chat --model_name gpt-4o-mini
garak --probes dan,encoding --model_type openai-chat --model_name gpt-4o-mini
garak --report_type html -G /tmp/garak-report
python -m garak.scan --model_type claude --model_name claude-3-5-sonnet

# Secrets and PII
gitleaks detect --source . --report-format json --report-path leak.json
detect-secrets scan --baseline .secrets.baseline
presidio-analyzer --analyzer text 'Call me at 555-0100'

# Supply chain
scorecard --repo=github.com/org/app
pip-audit -r requirements.txt
```

## Guardrail Checklist

1. Prompt injection probes pass with mitigations in place
2. No secrets in training data or prompts (gitleaks baseline)
3. PII redaction before model input/output
4. Supply-chain scorecard >= 7
5. Bias evaluation documented for sensitive use cases

## Best Practices

- Run garak in CI on model updates, not just releases
- Establish a secrets baseline, then fail on new leaks
- Log model decisions for audit (human-in-the-loop where risky)
- Write model cards: data, limitations, mitigations
- Publish an AI ethics review checklist with the product

## Capabilities

### llm-security-scanning
Probe LLMs for prompt injection, jailbreaks, and harmful output with garak.

**Parameters:**
- `model_type` (string): Model interface: openai-chat, huggingface, claude
- `model_name` (string): Model identifier
- `probes` (string): Probe groups, e.g. dan, encoding

**Commands:**
- `garak --model_type openai-chat --model_name gpt-4o-mini`
- `garak --model_type huggingface --model_name org/model --probes dan,encoding`
- `garak --report_type html -G /tmp/garak-report`
- `garak --probes dan --model_type openai-chat --model_name gpt-4o-mini`
- `python -m garak.scan --model_type claude --model_name claude-3-5-sonnet`

**Examples:**
- garak --model_type openai-chat --model_name gpt-4o-mini
- garak --probes dan --model_type openai-chat --model_name gpt-4o-mini
- garak --report_type html -G /tmp/garak-report

### data-and-supply-chain
Scan repos for secrets, PII, and supply-chain risks.

**Parameters:**
- `source` (string): Path or repo to scan
- `report` (string): Report output path

**Commands:**
- `gitleaks detect --source . --report-format json --report-path leak.json`
- `detect-secrets scan --baseline .secrets.baseline`
- `scorecard --repo=github.com/org/app`
- `presidio-analyzer --analyzer text 'Call me at 555-0100'`
- `gitleaks detect --redact`
- `pip-audit -r requirements.txt`

**Examples:**
- gitleaks detect --source . --report-format json
- scorecard --repo=github.com/org/app
- presidio-analyzer --analyzer text 'Call me at 555-0100'

## References
- [garak LLM Vulnerability Scanner](https://docs.garak.ai/garak/)
- [OpenSSF Scorecard](https://scorecard.dev/)
- [Microsoft Presidio](https://microsoft.github.io/presidio/)
- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework)
