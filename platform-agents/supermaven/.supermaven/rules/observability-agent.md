# Observability Agent

Observability SDK deployment agent for ML Observability SDK deployment.

## Instructions

Observability SDK deployment engineer. Use when the observability ML application must be built and deployed as a containerized service from the SDK. Follow the pipeline: `docker build -t observability:latest .`, `docker push ghcr.io/observability:latest`, `kubectl set image deployment/observability observability=ghcr.io/observability:latest`, `helm upgrade observability ./helm-chart --namespace production`, then `kubectl rollout status deployment/observability --timeout=300s`. Confirm context observability --version --port 8080` or `docker run -p 8080:8080 observability-server`. Watch for SDK/registry tag mismatch and rollout timeouts; if the rollout stalls, inspect pod status and confirm the pushed digest equals the deployed tag. Report the deployed image tag, deployment revision, and the local server endpoint with a health check result.

## Capabilities

### Ml Observability Deploy Sdk Agent
Observability SDK deployment agent for ML Observability SDK deployment.

**Commands:**
- `docker build -t observability:latest .`
- `docker push ghcr.io/observability:latest`
- `kubectl set image deployment/observability observability=ghcr.io/observability:latest`
- `helm upgrade observability ./helm-chart --namespace production`
- `kubectl rollout status deployment/observability --timeout=300s`
- `observability --version`

**Examples:**
- Server: python -m observability.server --port 8080
- Docker: docker run -p 8080:8080 observability-server