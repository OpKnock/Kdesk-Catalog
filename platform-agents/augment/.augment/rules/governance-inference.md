---
type: agent_requested
description: "Governance inference server agent Manages Governance inference server. Use when working with Ml Governance Inference Server Agent V2 or when the user mentions Ml Governance Inference Server Agent V2."
---

# Governance Inference

Governance inference server agent Manages Governance inference server.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl http://localhost:8080/governance --data '{"model": "mod`
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

## Instructions

Governance inference server operator (v2). Call on this agent to run the Governance inference server for governed model scoring. Launch with `python inference_server.py --port 8080`, then submit a model for review with `curl http://localhost:8080/governance --data '{"model": "model.pkl"}'`. Run the compliance pass with `python compliance_check.py --model model.pkl --rules rules.json` and the audit pass with `python audit.py --model model.pkl --data train.csv --output audit.json`. Common failure modes: rules.json or train.csv missing, model.pkl unreadable, and the port already in use; validate file paths and port availability first. Report the governance endpoint response, compliance and audit results, and the server status. Cross-check with examples like `python inference_server.py --port 8080` and `curl http://localhost:8080/governance --data '{"model": "model.pkl"}'` and `python audit.py --model model.pkl --data train.csv --output audit.json` and `python compliance_check.py --model model.pkl --rules rules.json`.

## Capabilities

### Ml Governance Inference Server Agent V2
Governance inference server agent. Manages Governance inference server.

**Parameters:**
- `data` (string): CLI flag --data observed in capability commands
- `model` (string): CLI flag --model observed in capability commands

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

## References
- [MLflow Model Registry](https://mlflow.org/docs/latest/model-registry.html)
- [curl Documentation](https://curl.se/docs/)
- [Python Documentation](https://docs.python.org/3/)