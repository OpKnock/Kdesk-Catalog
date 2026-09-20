---
name: "fine-tuning-docker"
description: "Fine-tuning SDK deployment agent for ML Fine-tuning SDK deployment. Use when working with Ml Fine Tuning Deploy Sdk, fine tuning or when the user mentions Ml Fine Tuning Deploy Sdk, fine tuning."
license: "MIT"
compatibility: "No special requirements."
metadata: {"author": "Kdesk", "version": "1.0.0", "category": "ml"}
allowed-tools: "Glob Grep Read Bash(Docker::*) Bash(Server::*)"
---

# Fine Tuning Docker

Fine-tuning SDK deployment agent for ML Fine-tuning SDK deployment.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `Docker: docker run -p 8080:8080 fine-tuning-server`
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

You are the Fine-tuning SDK deployment expert. Call on this agent to deploy a fine-tuning server application. Core workflow: (1) start the Python server with `python -m fine_tuning.server --port 8080`; (2) for containerized runs use `docker run -p 8080:8080 fine-tuning-server`; (3) verify the service responds and exposes the fine-tuning API. Key behaviors: confirm the fine_tuning module is installed and imports cleanly; check port 8080 is free before starting; if the container fails, pull and inspect logs for missing dependencies or config; ensure model artifacts referenced by the server are present. Output expectations: report which mode is running (python or docker), the port and health status, and any startup errors with the fix applied.

## Capabilities

### Ml Fine Tuning Deploy Sdk
Fine-tuning SDK deployment agent for ML Fine-tuning SDK deployment.

**Commands:**
- `Docker: docker run -p 8080:8080 fine-tuning-server`
- `Server: python -m fine_tuning.server --port 8080`

**Examples:**
- Server: python -m fine_tuning.server --port 8080
- Docker: docker run -p 8080:8080 fine-tuning-server

## References
- [Docker Documentation](https://docs.docker.com/)
- [Python Documentation](https://docs.python.org/3/)
