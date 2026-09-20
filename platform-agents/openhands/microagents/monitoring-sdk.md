---
name: "monitoring-sdk"
description: "it deployment agent handling ML it deployment."
type: knowledge
triggers: ["monitoring-sdk", "ml monitoring deploy sdk agent v2"]
---

# Monitoring Sdk

it deployment agent handling ML it deployment.

## Instructions

Monitoring SDK deployment engineer (v2). Call on this agent to ship the Monitoring ML application as a containerized service from the SDK. Workflow: build with `docker build -t ing:latest .`, publish with `docker push ghcr.io/ing:latest`, roll over with `kubectl set image deployment/ing ing=ghcr.io/ing:latest`, apply charts with `helm upgrade ing ./helm-chart --namespace production`, and verify with `kubectl rollout status deployment/ing --timeout=300s`. Start by confirming context docker --version --port 8080` or `docker run -p 8080:8080 monitoring-server`. Watch for tag mismatch and rollout stalls; verify the pushed digest equals the deployed tag before retrying. Report the deployed tag, revision, and local endpoint health.

## Capabilities

### Ml Monitoring Deploy Sdk Agent V2
Monitoring SDK deployment agent for ML Monitoring SDK deployment.

**Commands:**
- `docker build -t ing:latest .`
- `docker push ghcr.io/ing:latest`
- `kubectl set image deployment/ing ing=ghcr.io/ing:latest`
- `helm upgrade ing ./helm-chart --namespace production`
- `kubectl rollout status deployment/ing --timeout=300s`
- `docker --version`

**Examples:**
- Server: python -m monitoring.server --port 8080
- Docker: docker run -p 8080:8080 monitoring-server
