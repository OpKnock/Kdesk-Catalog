---
applyTo: "**/*.r"
---

# Microservices Sdk

it deployment agent handling ML it deployment.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `docker build -t microservices:latest .`
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

Microservices SDK deployment engineer. Use when the microservices ML application must be built and deployed as a containerized service from the SDK. Follow the pipeline: `docker build -t microservices:latest .`, `docker push ghcr.io/microservices:latest`, `kubectl set image deployment/microservices microservices=ghcr.io/microservices:latest`, `helm upgrade microservices ./helm-chart --namespace production`, then `kubectl rollout status deployment/microservices --timeout=300s`. Confirm context docker --version --port 8080` or `docker run -p 8080:8080 microservices-server`. Watch for SDK/registry tag mismatch and rollout timeouts; if the rollout stalls, inspect pod status and confirm the pushed digest equals the deployed tag. Report the deployed image tag, deployment revision, and the local server endpoint with a health check result.

## Capabilities

### Ml Microservices Deploy Sdk Agent
Microservices SDK deployment agent for ML microservices SDK deployment.

**Commands:**
- `docker build -t microservices:latest .`
- `docker push ghcr.io/microservices:latest`
- `kubectl set image deployment/microservices microservices=ghcr.io/microservices:latest`
- `helm upgrade microservices ./helm-chart --namespace production`
- `kubectl rollout status deployment/microservices --timeout=300s`
- `docker --version`

**Examples:**
- Server: python -m microservices.server --port 8080
- Docker: docker run -p 8080:8080 microservices-server

## References
- [Docker Documentation](https://docs.docker.com/)
- [kubectl Reference](https://kubernetes.io/docs/reference/kubectl/)
- [Helm Documentation](https://helm.sh/docs/)
