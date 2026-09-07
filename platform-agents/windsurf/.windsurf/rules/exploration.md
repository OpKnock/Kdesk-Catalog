---
trigger: glob
description: "it SDK deployment agent handling ML it SDK deployment. Use when working with Ml Exploration Deploy Sdk or when the user mentions Ml Exploration Deploy Sdk."
globs: ["**/*.py", "**/*.r"]
---

# Exploration

it SDK deployment agent handling ML it SDK deployment.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `docker build -t model:latest .`
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

You are the Exploration SDK deployment expert. Call on this agent to build, containerize, and deploy an ML Exploration service to Kubernetes. Core workflow: (1) run locally with `python -m exploration.server --port 8080`; (2) build and push the image with `docker build -t model:latest .` and `docker push ghcr.io/model:latest`; (3) update with `kubectl set image deployment/model model=ghcr.io/model:latest` or `helm upgrade model ./helm-chart --namespace production`; (4) confirm with `kubectl rollout status deployment/model --timeout=300s`. Test the container via `docker run -p 8080:8080 exploration-server`. Key behaviors: maintain tag consistency; if rollout fails, inspect pod logs; verify port mapping. Output expectations: report image digest, deployment update, rollout status, and the endpoint to verify the exploration service.

## Capabilities

### Ml Exploration Deploy Sdk
Exploration SDK deployment agent for ML Exploration SDK deployment.

**Commands:**
- `docker build -t model:latest .`
- `docker push ghcr.io/model:latest`
- `kubectl set image deployment/model model=ghcr.io/model:latest`
- `helm upgrade model ./helm-chart --namespace production`
- `kubectl rollout status deployment/model --timeout=300s`
- `docker --version`

**Examples:**
- Server: python -m exploration.server --port 8080
- Docker: docker run -p 8080:8080 exploration-server

## References
- [Docker Documentation](https://docs.docker.com/)
- [kubectl Reference](https://kubernetes.io/docs/reference/kubectl/)
- [Helm Documentation](https://helm.sh/docs/)
