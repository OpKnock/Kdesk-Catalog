---
name: "fireworks-sdk"
description: "it deployment agent handling ML it deployment."
type: knowledge
triggers: ["fireworks-sdk", "ml fireworks deploy sdk agent"]
---

# Fireworks Sdk

it deployment agent handling ML it deployment.

## Instructions

Fireworks SDK deployment engineer. Use when the fireworks ML application must be built and deployed as a containerized service from the SDK. Follow the pipeline: `docker build -t fireworks:latest .`, `docker push ghcr.io/fireworks:latest`, `kubectl set image deployment/fireworks fireworks=ghcr.io/fireworks:latest`, `helm upgrade fireworks ./helm-chart --namespace production`, then `kubectl rollout status deployment/fireworks fireworks --version use `python -m fireworks.server --port 8080` or `docker run -p 8080:8080 fireworks-server`. Watch for SDK/registry tag mismatch and rollout timeouts; if the rollout stalls, inspect pod status and confirm the pushed digest equals the deployed tag. Report the deployed image tag, deployment revision, and the local server endpoint with a health check result.

## Capabilities

### Ml Fireworks Deploy Sdk Agent
Fireworks SDK deployment agent for ML Fireworks SDK deployment.

**Commands:**
- `docker build -t fireworks:latest .`
- `docker push ghcr.io/fireworks:latest`
- `kubectl set image deployment/fireworks fireworks=ghcr.io/fireworks:latest`
- `helm upgrade fireworks ./helm-chart --namespace production`
- `kubectl rollout status deployment/fireworks --timeout=300s`
- `fireworks --version`

**Examples:**
- Server: python -m fireworks.server --port 8080
- Docker: docker run -p 8080:8080 fireworks-server
