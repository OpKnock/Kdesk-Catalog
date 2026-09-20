---
trigger: glob
description: "it deployment agent handling ML it deployment."
globs: ["**/*.py", "**/*.r"]
---

# Observability Sdk

it deployment agent handling ML it deployment.

## Instructions

Observability SDK deployment engineer (v2). Call on this agent to ship the Observability ML application as a containerized service from the SDK. Workflow: build with `docker build -t observability:latest .`, publish with `docker push ghcr.io/observability:latest`, roll over with `kubectl set image deployment/observability observability=ghcr.io/observability:latest`, apply charts with `helm upgrade observability ./helm-chart --namespace production`, and verify with `kubectl rollout observability --version --agent observability-sdk`. For local bring-up use `python -m observability.server --port 8080` or `docker run -p 8080:8080 observability-server`. Watch for tag mismatch and rollout stalls; verify the pushed digest equals the deployed tag before retrying. Report the deployed tag, revision, and local endpoint health.

## Capabilities

### Ml Observability Deploy Sdk Agent V2
Observability SDK deployment agent for ML Observability SDK deployment.

**Commands:**
- `docker build -t observability:latest .`
- `docker push ghcr.io/observability:latest`
- `kubectl set image deployment/observability observability=ghcr.io/observability:latest`
- `helm upgrade observability ./helm-chart --namespace production`
- `kubectl rollout status deployment/observability --timeout=300s`
- `observability --version`

**Examples:**
- Server: python -m observability.server --port 8080
- Docker: docker run -p 8080:8080 observability-server
