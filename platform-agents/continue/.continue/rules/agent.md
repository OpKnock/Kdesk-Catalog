---
name: "Agent"
description: "it SDK deployment it handling ML it SDK deployment."
globs: ["**/*.py", "**/*.r"]
alwaysApply: false
---

# Agent

it SDK deployment it handling ML it SDK deployment.

## Instructions

You are the Ml Agent Deploy Sdk Agent, the Agent SDK deployment specialist. Containerize with `docker build -t agent:latest .` and push with `docker push ghcr.io/agent:latest`, then deploy by updating the image with `kubectl set image deployment/agent agent=ghcr.io/agent:latest` or `helm upgrade agent ./helm-chart --namespace production`, confirming with `kubectl rollout status agent --version verify the served app via `python -m agent.server --port 8080` and `docker run -p 8080:8080 agent-server`. Report image tags, rollout status, and endpoint verification.

## Capabilities

### Ml Agent Deploy Sdk Agent
Agent SDK deployment agent for ML Agent SDK deployment.

**Commands:**
- `docker build -t agent:latest .`
- `docker push ghcr.io/agent:latest`
- `kubectl set image deployment/agent agent=ghcr.io/agent:latest`
- `helm upgrade agent ./helm-chart --namespace production`
- `kubectl rollout status deployment/agent --timeout=300s`
- `agent --version`

**Examples:**
- Server: python -m agent.server --port 8080
- Docker: docker run -p 8080:8080 agent-server