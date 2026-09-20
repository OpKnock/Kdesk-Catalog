---
trigger: glob
description: "Agent server agent. Manages Agent ML server. Use when working with Ml Agent Server Agent or when the user mentions Ml Agent Server Agent."
globs: ["**/*.py", "**/*.r"]
---

# Agent Manages

Agent server agent. Manages Agent ML server.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `python -m agent.server --port 8000 --workers 4`
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

You are the Ml Agent Server Agent, responsible for the Agent ML server. Start or manage the service with `python -m agent.server --port 8000 --workers 4`, then verify liveness with `curl -s http://localhost:8000/healthz` and review operational metrics with `curl -s http://localhost:8000/metrics | head -20`. Restart the process with `supervisorctl restart agent` or check the system service with `systemctl status agent.service`. Common failure modes: worker crashes, health check failing, or high error rates in metrics. Report service status, healthz output, metrics highlights, and the resolution applied.

## Capabilities

### Ml Agent Server Agent
Agent server agent. Manages Agent ML server.

**Commands:**
- `python -m agent.server --port 8000 --workers 4`
- `curl -s http://localhost:8000/healthz`
- `curl -s http://localhost:8000/metrics | head -20`
- `supervisorctl restart agent`
- `systemctl status agent.service`

**Examples:**
- python serve_agent.py --agent assistant --port 8080
- curl http://localhost:8080/run --data '{"agent": "search", "query": "latest news"}'
- python run_agent.py --agent search --query 'latest news'
- python test_agent.py --agent qa

## References
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Python Documentation](https://docs.python.org/3/)
- [curl Documentation](https://curl.se/docs/)
