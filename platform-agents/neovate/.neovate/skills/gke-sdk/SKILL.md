---
name: "gke-sdk"
description: "it deployment agent handling ML it deployment. Use when working with Ml Gke Deploy Sdk Agent or when the user mentions Ml Gke Deploy Sdk Agent."
license: "MIT"
compatibility: "Requires network access."
metadata: {"author": "Kdesk", "version": "1.0.0", "category": "ml"}
allowed-tools: "Glob Grep Read Bash(docker:*) Bash(gke:*) Bash(helm:*) Bash(kubectl:*)"
---

# Gke Sdk

it deployment agent handling ML it deployment.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `docker build -t gke:latest .`
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

GKE SDK deployment engineer. Use when the gke ML application must be built and deployed as a containerized service from the SDK. Follow the pipeline: `docker build -t gke:latest .`, `docker push ghcr.io/gke:latest`, `kubectl set image deployment/gke gke=ghcr.io/gke:latest`, `helm upgrade gke ./helm-chart --namespace production`, then `kubectl rollout status deployment/gke gke --version `python -m gke.server --port 8080` or `docker run -p 8080:8080 gke-server`. Watch for SDK/registry tag mismatch and rollout timeouts; if the rollout stalls, inspect pod status and confirm the pushed digest equals the deployed tag. Report the deployed image tag, deployment revision, and the local server endpoint with a health check result.

## Capabilities

### Ml Gke Deploy Sdk Agent
GKE SDK deployment agent for ML GKE SDK deployment.

**Commands:**
- `docker build -t gke:latest .`
- `docker push ghcr.io/gke:latest`
- `kubectl set image deployment/gke gke=ghcr.io/gke:latest`
- `helm upgrade gke ./helm-chart --namespace production`
- `kubectl rollout status deployment/gke --timeout=300s`
- `gke --version`

**Examples:**
- Server: python -m gke.server --port 8080
- Docker: docker run -p 8080:8080 gke-server

## References
- [Google Kubernetes Engine Documentation](https://cloud.google.com/kubernetes-engine/docs)
- [Docker Documentation](https://docs.docker.com/)
- [kubectl Reference](https://kubernetes.io/docs/reference/kubectl/)
