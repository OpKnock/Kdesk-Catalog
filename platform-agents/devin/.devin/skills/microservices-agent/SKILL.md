---
name: "microservices-agent"
description: "Microservices server agent. Manages microservices ML server. Use when working with Ml Microservices Server Agent or when the user mentions Ml Microservices Server Agent."
license: "MIT"
compatibility: "Requires network access."
metadata: {"author": "Kdesk", "version": "1.0.0", "category": "ml"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(python:*) Bash(supervisorctl:*) Bash(systemctl:*)"
---

# Microservices Agent

Microservices server agent. Manages microservices ML server.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `python -m microservices.server --port 8000 --workers 4`
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

microservices server operator. Call on this agent to launch, verify, and keep alive the microservices serving process. Start the service with `python -m microservices.server --port 8000 --workers 4`, then confirm readiness with `curl -s http://localhost:8000/healthz` and inspect metrics with `curl -s http://localhost:8000/metrics | head -20`. If it crashes or degrades, restart via `supervisorctl restart microservices` and confirm the unit with `systemctl status microservices.service`. Common failure modes: port already bound, worker pool exhaustion (scale `--workers`), rising error counts. For model-facing work use examples like `kubectl apply -f deployment.yaml` and `kubectl get pods` and `kubectl logs -f <pod>` and `curl http://my-service:8080/predict`. Report the healthz code, a metrics summary, the supervisor/systemd status after any restart, and next steps.

## Capabilities

### Ml Microservices Server Agent
Microservices server agent. Manages microservices ML server.

**Commands:**
- `python -m microservices.server --port 8000 --workers 4`
- `curl -s http://localhost:8000/healthz`
- `curl -s http://localhost:8000/metrics | head -20`
- `supervisorctl restart microservices`
- `systemctl status microservices.service`

**Examples:**
- kubectl apply -f deployment.yaml
- kubectl get pods
- kubectl logs -f <pod>
- curl http://my-service:8080/predict

## References
- [Python Documentation](https://docs.python.org/3/)
- [curl Documentation](https://curl.se/docs/)
