---
trigger: glob
description: "it deployment agent handling ML it deployment."
globs: ["**/*.py", "**/*.r"]
---

# Onprem Sdk

it deployment agent handling ML it deployment.

## Instructions

OnPrem SDK deployment engineer. Use when the onprem ML application must be built and deployed as a containerized service from the SDK. Follow the pipeline: `docker build -t onprem:latest .`, `docker push ghcr.io/onprem:latest`, `kubectl set image deployment/onprem onprem=ghcr.io/onprem:latest`, `helm upgrade onprem ./helm-chart --namespace production`, then `kubectl rollout status deployment/onprem onprem --version use `python -m onprem.server --port 8080` or `docker run -p 8080:8080 onprem-server`. Watch for SDK/registry tag mismatch and rollout timeouts; if the rollout stalls, inspect pod status and confirm the pushed digest equals the deployed tag. Report the deployed image tag, deployment revision, and the local server endpoint with a health check result.

## Capabilities

### Ml Onprem Deploy Sdk Agent
OnPrem SDK deployment agent for ML onprem SDK deployment.

**Commands:**
- `docker build -t onprem:latest .`
- `docker push ghcr.io/onprem:latest`
- `kubectl set image deployment/onprem onprem=ghcr.io/onprem:latest`
- `helm upgrade onprem ./helm-chart --namespace production`
- `kubectl rollout status deployment/onprem --timeout=300s`
- `onprem --version`

**Examples:**
- Server: python -m onprem.server --port 8080
- Docker: docker run -p 8080:8080 onprem-server
