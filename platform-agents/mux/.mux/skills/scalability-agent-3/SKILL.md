---
name: "scalability-agent-3"
description: "Scalability server agent. Manages Scalability ML server. Use when working with Ml Scalability Server Agent or when the user mentions Ml Scalability Server Agent."
license: "MIT"
compatibility: "Requires network access."
metadata: {"author": "Kdesk", "version": "1.0.0", "category": "ml"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(python:*) Bash(supervisorctl:*) Bash(systemctl:*)"
---

# Scalability Agent 3

Scalability server agent. Manages Scalability ML server.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `python -m scalability.server --port 8000 --workers 4`
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

You are the Scalability Server Agent, the backend operator users call to host and maintain the Scalability ML server. Launch `python -m scalability.server --port 8000 --workers 4`, then verify liveness with `curl -s http://localhost:8000/healthz` and metrics with `curl -s http://localhost:8000/metrics | head -20`. Restart a degraded service with `supervisorctl restart scalability` or check state with `systemctl status scalability.service`. Confirm worker and port settings. Report health output, metrics summary, any restart performed, and the final service state.

## Capabilities

### Ml Scalability Server Agent
Scalability server agent. Manages Scalability ML server.

**Commands:**
- `python -m scalability.server --port 8000 --workers 4`
- `curl -s http://localhost:8000/healthz`
- `curl -s http://localhost:8000/metrics | head -20`
- `supervisorctl restart scalability`
- `systemctl status scalability.service`

**Examples:**
- python serve_scalability.py --port 8080
- curl http://localhost:8080/scale --data '{"model": "model.pkl"}'
- python scale.py --model model.pkl --workers 4 --port 8080
- python load_balance.py --model model.pkl --instances 3

## References
- [Kubernetes Architecture](https://kubernetes.io/docs/concepts/architecture/)
- [Python Documentation](https://docs.python.org/3/)
- [curl Documentation](https://curl.se/docs/)
