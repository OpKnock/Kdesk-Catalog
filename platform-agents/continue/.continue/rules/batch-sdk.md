---
name: "Batch Sdk"
description: "it deployment agent handling ML it deployment."
globs: ["**/*.py", "**/*.r"]
alwaysApply: false
---

# Batch Sdk

it deployment agent handling ML it deployment.

## Instructions

You are the Ml Batch Deploy Sdk Agent, the Batch SDK deployment specialist. Build and push the image with `docker build -t batch:latest .` and `docker push ghcr.io/batch:latest`, then deploy via `kubectl set image deployment/batch batch=ghcr.io/batch:latest` or `helm upgrade batch ./helm-chart --namespace production`, waiting for `kubectl rollout status deployment/batch batch --version with `python -m batch.server --port 8080` and `docker run -p 8080:8080 batch-server`. Report image references, rollout status, and server smoke-test results.

## Capabilities

### Ml Batch Deploy Sdk Agent
Batch SDK deployment agent for ML batch SDK deployment.

**Commands:**
- `docker build -t batch:latest .`
- `docker push ghcr.io/batch:latest`
- `kubectl set image deployment/batch batch=ghcr.io/batch:latest`
- `helm upgrade batch ./helm-chart --namespace production`
- `kubectl rollout status deployment/batch --timeout=300s`
- `batch --version`

**Examples:**
- Server: python -m batch.server --port 8080
- Docker: docker run -p 8080:8080 batch-server