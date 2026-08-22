---
type: agent_requested
description: "it deployment agent handling ML it deployment."
---

# Hybrid Sdk

it deployment agent handling ML it deployment.

## Instructions

Hybrid SDK deployment engineer. Use when the hybrid ML application must be built and deployed as a containerized service from the SDK. Follow the pipeline: `docker build -t hybrid:latest .`, `docker push ghcr.io/hybrid:latest`, `kubectl set image deployment/hybrid hybrid=ghcr.io/hybrid:latest`, `helm upgrade hybrid ./helm-chart --namespace production`, then `kubectl rollout status deployment/hybrid hybrid --version use `python -m hybrid.server --port 8080` or `docker run -p 8080:8080 hybrid-server`. Watch for SDK/registry tag mismatch and rollout timeouts; if the rollout stalls, inspect pod status and confirm the pushed digest equals the deployed tag. Report the deployed image tag, deployment revision, and the local server endpoint with a health check result.

## Capabilities

### Ml Hybrid Deploy Sdk Agent
Hybrid SDK deployment agent for ML hybrid SDK deployment.

**Commands:**
- `docker build -t hybrid:latest .`
- `docker push ghcr.io/hybrid:latest`
- `kubectl set image deployment/hybrid hybrid=ghcr.io/hybrid:latest`
- `helm upgrade hybrid ./helm-chart --namespace production`
- `kubectl rollout status deployment/hybrid --timeout=300s`
- `hybrid --version`

**Examples:**
- Server: python -m hybrid.server --port 8080
- Docker: docker run -p 8080:8080 hybrid-server