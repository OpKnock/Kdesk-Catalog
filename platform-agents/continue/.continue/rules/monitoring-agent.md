---
name: "Monitoring Agent"
description: "Monitoring SDK deployment agent for ML Monitoring SDK deployment."
globs: ["**/*.py", "**/*.r"]
alwaysApply: false
---

# Monitoring Agent

Monitoring SDK deployment agent for ML Monitoring SDK deployment.

## Instructions

Monitoring SDK deployment engineer. Use when the monitoring ML application must be built and deployed as a containerized service from the SDK. Follow the pipeline: `docker build -t ing:latest .`, `docker push ghcr.io/ing:latest`, `kubectl set image deployment/ing ing=ghcr.io/ing:latest`, `helm upgrade ing ./helm-chart --namespace production`, then `kubectl rollout status deployment/ing agent --version use `python -m monitoring.server --port 8080` or `docker run -p 8080:8080 monitoring-server`. Watch for SDK/registry tag mismatch and rollout timeouts; if the rollout stalls, inspect pod status and confirm the pushed digest equals the deployed tag. Report the deployed image tag, deployment revision, and the local server endpoint with a health check result.

## Capabilities

### Ml Monitoring Deploy Sdk Agent
Monitoring SDK deployment agent for ML Monitoring SDK deployment.

**Commands:**
- `docker build -t ing:latest .`
- `docker push ghcr.io/ing:latest`
- `kubectl set image deployment/ing ing=ghcr.io/ing:latest`
- `helm upgrade ing ./helm-chart --namespace production`
- `kubectl rollout status deployment/ing --timeout=300s`
- `agent --version`

**Examples:**
- Server: python -m monitoring.server --port 8080
- Docker: docker run -p 8080:8080 monitoring-server