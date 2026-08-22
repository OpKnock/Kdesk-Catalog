---
trigger: glob
description: "it deployment agent handling ML it deployment."
globs: ["**/*.py", "**/*.r"]
---

# Gke Sdk

it deployment agent handling ML it deployment.

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
