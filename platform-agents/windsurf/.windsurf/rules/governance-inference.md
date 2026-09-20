---
trigger: glob
description: "Governance inference server agent Manages Governance inference server."
globs: ["**/*.go", "**/*.json", "**/*.py", "**/*.r"]
---

# Governance Inference

Governance inference server agent Manages Governance inference server.

## Instructions

Governance inference server operator (v2). Call on this agent to run the Governance inference server for governed model scoring. Launch with `python inference_server.py --port 8080`, then submit a model for review with `curl http://localhost:8080/governance --data '{"model": "model.pkl"}'`. Run the compliance pass with `python compliance_check.py --model model.pkl --rules rules.json` and the audit pass with `python audit.py --model model.pkl --data train.csv --output audit.json`. Common failure modes: rules.json or train.csv missing, model.pkl unreadable, and the port already in use; validate file paths and port availability first. Report the governance endpoint response, compliance and audit results, and the server status. Cross-check with examples like `python inference_server.py --port 8080` and `curl http://localhost:8080/governance --data '{"model": "model.pkl"}'` and `python audit.py --model model.pkl --data train.csv --output audit.json` and `python compliance_check.py --model model.pkl --rules rules.json`.

## Capabilities

### Ml Governance Inference Server Agent V2
Governance inference server agent. Manages Governance inference server.

**Commands:**
- `curl http://localhost:8080/governance --data '{"model": "model.pkl"}'`
- `python compliance_check.py --model model.pkl --rules rules.json`
- `python audit.py --model model.pkl --data train.csv --output audit.json`
- `python inference_server.py --port 8080`

**Examples:**
- python inference_server.py --port 8080
- curl http://localhost:8080/governance --data '{"model": "model.pkl"}'
- python audit.py --model model.pkl --data train.csv --output audit.json
- python compliance_check.py --model model.pkl --rules rules.json
