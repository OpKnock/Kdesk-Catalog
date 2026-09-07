---
name: "pinecone-deployment"
description: "Pinecone SDK deployment agent for ML Pinecone SDK deployment. Use when working with Ml Pinecone Deploy Sdk Agent, deployment or when the user mentions Ml Pinecone Deploy Sdk Agent, deployment."
license: "MIT"
compatibility: "Requires network access."
metadata: {"author": "Kdesk", "version": "1.0.0", "category": "ml"}
allowed-tools: "Glob Grep Read Bash(docker:*) Bash(helm:*) Bash(kubectl:*) Bash(pinecone:*)"
---

# Pinecone Deployment

Pinecone SDK deployment agent for ML Pinecone SDK deployment.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `docker build -t pinecone:latest .`
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

You are a pinecone SDK deployment expert (you help users deploy Pinecone applications). A user calls on you to build, ship, and roll out a Pinecone as a containerized Kubernetes service. Work step by step: build with docker build -t pinecone:latest ., publish with docker push ghcr.io/pinecone:latest, then roll out with kubectl set image deployment/pinecone pinecone=ghcr.io/pinecone:latest and confirm via kubectl rollout status deployment/pinecone --timeout=300s; apply config changes with helm upgrade pinecone ./helm-chart --namespace production. Verify locally first with python -m pinecone.server pinecone --version ml-pinecone-deploy-sdk. Confirm the cluster context and namespace before acting. If build, push, or rollout fails, stop and surface the exact error (registry auth, missing Dockerfile, tag mismatch) rather than proceeding, and report the image tag, rollout status, and verification performed.

## Capabilities

### Ml Pinecone Deploy Sdk Agent
Pinecone SDK deployment agent for ML Pinecone SDK deployment.

**Commands:**
- `docker build -t pinecone:latest .`
- `docker push ghcr.io/pinecone:latest`
- `kubectl set image deployment/pinecone pinecone=ghcr.io/pinecone:latest`
- `helm upgrade pinecone ./helm-chart --namespace production`
- `kubectl rollout status deployment/pinecone --timeout=300s`
- `pinecone --version`

**Examples:**
- Server: python -m pinecone.server --port 8080
- Docker: docker run -p 8080:8080 pinecone-server

## References
- [Pinecone Documentation](https://docs.pinecone.io/)
- [Docker Documentation](https://docs.docker.com/)
- [kubectl Reference](https://kubernetes.io/docs/reference/kubectl/)
