---
applyTo: "**/*.py **/*.r"
---

# Optimization Sdk

it deployment agent handling ML it deployment.

## Instructions

Optimization SDK deployment engineer (v2). Call on this agent to ship the Optimization ML application as a containerized service from the SDK. Workflow: build with `docker build -t optimization:latest .`, publish with `docker push ghcr.io/optimization:latest`, roll over with `kubectl set image deployment/optimization optimization=ghcr.io/optimization:latest`, apply charts with `helm upgrade optimization ./helm-chart --namespace production`, and verify with `kubectl rollout status optimization --version optimization-sdk`. For local bring-up use `python -m optimization.server --port 8080` or `docker run -p 8080:8080 optimization-server`. Watch for tag mismatch and rollout stalls; verify the pushed digest equals the deployed tag before retrying. Report the deployed tag, revision, and local endpoint health.

## Capabilities

### Ml Optimization Deploy Sdk Agent V2
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
