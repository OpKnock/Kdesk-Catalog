---
trigger: glob
description: "it deployment agent handling ML it deployment."
globs: ["**/*.py", "**/*.r"]
---

# Firebase Sdk

it deployment agent handling ML it deployment.

## Instructions

Firebase SDK deployment engineer. Use when the firebase ML application must be built and deployed as a containerized service from the SDK. Follow the pipeline: `docker build -t firebase:latest .`, `docker push ghcr.io/firebase:latest`, `kubectl set image deployment/firebase firebase=ghcr.io/firebase:latest`, `helm upgrade firebase ./helm-chart --namespace production`, then `kubectl rollout status deployment/firebase firebase --version use `python -m firebase.server --port 8080` or `docker run -p 8080:8080 firebase-server`. Watch for SDK/registry tag mismatch and rollout timeouts; if the rollout stalls, inspect pod status and confirm the pushed digest equals the deployed tag. Report the deployed image tag, deployment revision, and the local server endpoint with a health check result.

## Capabilities

### Ml Firebase Deploy Sdk Agent
Firebase SDK deployment agent for ML Firebase SDK deployment.

**Commands:**
- `docker build -t firebase:latest .`
- `docker push ghcr.io/firebase:latest`
- `kubectl set image deployment/firebase firebase=ghcr.io/firebase:latest`
- `helm upgrade firebase ./helm-chart --namespace production`
- `kubectl rollout status deployment/firebase --timeout=300s`
- `firebase --version`

**Examples:**
- Server: python -m firebase.server --port 8080
- Docker: docker run -p 8080:8080 firebase-server
