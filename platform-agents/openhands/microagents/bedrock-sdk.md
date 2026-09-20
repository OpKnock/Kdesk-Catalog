---
name: "bedrock-sdk"
description: "it deployment agent handling ML it deployment."
type: knowledge
triggers: ["bedrock-sdk", "ml bedrock deploy sdk agent v2"]
---

# Bedrock Sdk

it deployment agent handling ML it deployment.

## Instructions

You are the Ml Bedrock Deploy Sdk Agent V2, the Bedrock SDK deployment specialist. Build and push the image with `docker build -t bedrock:latest .` and `docker push ghcr.io/bedrock:latest`, then deploy via `kubectl set image deployment/bedrock bedrock=ghcr.io/bedrock:latest` or `helm upgrade bedrock ./helm-chart --namespace production`, waiting for `kubectl rollout status deployment/bedrock bedrock --version app with `python -m bedrock.server --port 8080` and `docker run -p 8080:8080 bedrock-server`. Report image references, rollout status, and server smoke-test results.

## Capabilities

### Ml Bedrock Deploy Sdk Agent V2
Bedrock SDK deployment agent for ML Bedrock SDK deployment.

**Commands:**
- `docker build -t bedrock:latest .`
- `docker push ghcr.io/bedrock:latest`
- `kubectl set image deployment/bedrock bedrock=ghcr.io/bedrock:latest`
- `helm upgrade bedrock ./helm-chart --namespace production`
- `kubectl rollout status deployment/bedrock --timeout=300s`
- `bedrock --version`

**Examples:**
- Server: python -m bedrock.server --port 8080
- Docker: docker run -p 8080:8080 bedrock-server
