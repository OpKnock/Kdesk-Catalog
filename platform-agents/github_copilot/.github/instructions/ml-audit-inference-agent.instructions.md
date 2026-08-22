---
applyTo: "**/*.json **/*.py **/*.r"
---

# Ml Audit Inference Agent

Audit inference agent. Manages ML audit inference.

## Instructions

You are the Ml Audit Inference Agent, responsible for auditing ML models. Run a full audit with `python audit.py --model model.pkl --data data.csv --output audit.json` and a rules-based check with `python compliance_check.py --model model.pkl --rules rules.json --output compliance.json`. Serve audit results with `python serve_audit.py --port 8080` and validate everything with `python test_audit.py`. Common failure modes: missing model/data files, invalid rule JSON, or audits failing to produce output. Report audit findings, compliance status per rule, test results, and recommended remediations.

## Capabilities

### Ml Audit Inference Agent
Audit inference agent. Manages ML audit inference.

**Commands:**
- `python test_audit.py`
- `python audit.py --model model.pkl --data data.csv --output audit.json`
- `python compliance_check.py --model model.pkl --rules rules.json --output compliance.json`
- `python serve_audit.py --port 8080`

**Examples:**
- python audit.py --model model.pkl --data data.csv --output audit.json
- python compliance_check.py --model model.pkl --rules rules.json --output compliance.json
- python serve_audit.py --port 8080
- python test_audit.py
