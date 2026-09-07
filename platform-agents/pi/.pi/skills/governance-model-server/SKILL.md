---
name: "governance-model-server"
description: "Governance server agent. Manages Governance ML server. Use when working with Ml Governance Server Agent or when the user mentions Ml Governance Server Agent."
license: "MIT"
compatibility: "Requires network access."
metadata: {"author": "Kdesk", "version": "1.0.0", "category": "ml"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(governance:*) Bash(python:*) Bash(supervisorctl:*) Bash(systemctl:*)"
---

# Governance Model Server

Governance server agent. Manages Governance ML server.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `python -m model.server --port 8000 --workers 4`
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

Governance server operator. Call on this agent to launch, verify, and keep alive the Governance serving process. Start the service with `python -m model.server --port 8000 --workers 4`, then confirm readiness with `curl -s http://localhost:8000/healthz` and inspect metrics with `curl -s http://localhost:8000/metrics | head -20`. If it crashes or degrades, restart via `supervisorctl restart model` and confirm the unit governance --version governance-model-server` before touching the service. Common failure modes: port already bound, worker pool exhaustion (scale `--workers`), rising error counts. For model-facing work use examples like `python serve_governance.py --port 8080` and `curl http://localhost:8080/governance --data '{"model": "model.pkl"}'` and `python audit.py --model model.pkl --data train.csv --output audit.json` and `python compliance_check.py --model model.pkl --rules rules.json`. Report the healthz code, a metrics summary, the supervisor/systemd status after any restart, and next steps.

## Capabilities

### Ml Governance Server Agent
Governance server agent. Manages Governance ML server.

**Commands:**
- `python -m model.server --port 8000 --workers 4`
- `curl -s http://localhost:8000/healthz`
- `curl -s http://localhost:8000/metrics | head -20`
- `supervisorctl restart model`
- `systemctl status model.service`
- `governance --version`

**Examples:**
- python serve_governance.py --port 8080
- curl http://localhost:8080/governance --data '{"model": "model.pkl"}'
- python audit.py --model model.pkl --data train.csv --output audit.json
- python compliance_check.py --model model.pkl --rules rules.json

## References
- [MLflow Model Registry](https://mlflow.org/docs/latest/model-registry.html)
- [Python Documentation](https://docs.python.org/3/)
- [curl Documentation](https://curl.se/docs/)
