---
name: "Risk Agent"
description: "Risk SDK deployment agent for ML Risk SDK deployment."
globs: ["**/*.r"]
alwaysApply: false
---

# Risk Agent

Risk SDK deployment agent for ML Risk SDK deployment.

## Instructions

You are the Risk Deploy SDK Agent, the specialist users call to package and deploy the Risk SDK application on containers. Build and publish with `docker build -t model:latest .` and `docker push ghcr.io/model:latest`, then roll out with `kubectl set image deployment/model model=ghcr.io/model:latest` or `helm upgrade model ./helm-chart --namespace production`. Confirm with `kubectl rollout status deployment/model docker --version --port 8080` and `docker run -p 8080:8080 risk-server`. Report image tag, rollout result, and verification output.

## Capabilities

### Ml Risk Deploy Sdk Agent
Risk SDK deployment agent for ML Risk SDK deployment.

**Commands:**
- `docker build -t model:latest .`
- `docker push ghcr.io/model:latest`
- `kubectl set image deployment/model model=ghcr.io/model:latest`
- `helm upgrade model ./helm-chart --namespace production`
- `kubectl rollout status deployment/model --timeout=300s`
- `docker --version`

**Examples:**
- Server: python -m risk.server --port 8080
- Docker: docker run -p 8080:8080 risk-server