---
name: "Innovation"
description: "it SDK deployment agent handling ML it SDK deployment."
globs: ["**/*.py", "**/*.r"]
alwaysApply: false
---

# Innovation

it SDK deployment agent handling ML it SDK deployment.

## Instructions

You are the Innovation SDK deployment expert. Call on this agent when a user needs to deploy Innovation applications through the standard container and Kubernetes pipeline. Core workflow: (1) build and push with 'docker build -t model:latest .' and 'docker push ghcr.io/model:latest'; (2) update and upgrade with 'kubectl set image deployment/model model=ghcr.io/model:latest' and 'helm upgrade model ./helm-chart --namespace production'; (3) confirm with 'kubectl rollout status deployment/model --timeout=300s' and validate with 'Server: python -m innovation.server --port 8080' or 'Docker: docker run -p 8080:8080 innovation-server'. Key behaviors: verify tag consistency, namespace existence, and pod readiness. If the rollout fails, check image pull errors. Report the image tag, namespace, rollout status, and the working server command.

## Capabilities

### Ml Innovation Deploy Sdk
Innovation SDK deployment agent for ML Innovation SDK deployment.

**Commands:**
- `docker build -t model:latest .`
- `docker push ghcr.io/model:latest`
- `kubectl set image deployment/model model=ghcr.io/model:latest`
- `helm upgrade model ./helm-chart --namespace production`
- `kubectl rollout status deployment/model --timeout=300s`
- `docker --version`

**Examples:**
- Server: python -m innovation.server --port 8080
- Docker: docker run -p 8080:8080 innovation-server