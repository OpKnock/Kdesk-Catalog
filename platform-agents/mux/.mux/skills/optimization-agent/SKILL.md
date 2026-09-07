---
name: "optimization-agent"
description: "Optimization SDK deployment agent for ML Optimization SDK deployment. Use when working with Ml Optimization Deploy Sdk Agent or when the user mentions Ml Optimization Deploy Sdk Agent."
license: "MIT"
compatibility: "Requires network access."
metadata: {"author": "Kdesk", "version": "1.0.0", "category": "ml"}
allowed-tools: "Glob Grep Read Bash(docker:*) Bash(helm:*) Bash(kubectl:*) Bash(optimization:*)"
---

# Optimization Agent

Optimization SDK deployment agent for ML Optimization SDK deployment.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `docker build -t optimization:latest .`
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

Optimization SDK deployment engineer. Use when the optimization ML application must be built and deployed as a containerized service from the SDK. Follow the pipeline: `docker build -t optimization:latest .`, `docker push ghcr.io/optimization:latest`, `kubectl set image deployment/optimization optimization=ghcr.io/optimization:latest`, `helm upgrade optimization ./helm-chart --namespace production`, then `kubectl rollout status deployment/optimization --timeout=300s`. Confirm context with optimization --version --port 8080` or `docker run -p 8080:8080 optimization-server`. Watch for SDK/registry tag mismatch and rollout timeouts; if the rollout stalls, inspect pod status and confirm the pushed digest equals the deployed tag. Report the deployed image tag, deployment revision, and the local server endpoint with a health check result.

## Capabilities

### Ml Optimization Deploy Sdk Agent
Optimization SDK deployment agent for ML Optimization SDK deployment.

**Commands:**
- `docker build -t optimization:latest .`
- `docker push ghcr.io/optimization:latest`
- `kubectl set image deployment/optimization optimization=ghcr.io/optimization:latest`
- `helm upgrade optimization ./helm-chart --namespace production`
- `kubectl rollout status deployment/optimization --timeout=300s`
- `optimization --version`

**Examples:**
- Server: python -m optimization.server --port 8080
- Docker: docker run -p 8080:8080 optimization-server

## References
- [Optuna Documentation](https://optuna.org/)
- [Docker Documentation](https://docs.docker.com/)
- [kubectl Reference](https://kubernetes.io/docs/reference/kubectl/)
