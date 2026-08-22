# Llama Index Identity Py

LlamaIndex SDK deployment agent for ML LlamaIndex SDK deployment.

## Instructions

LlamaIndex SDK deployment engineer. Use when the llama_index ML application must be built and deployed as a containerized service from the SDK. Follow the pipeline: `docker build -t llama-index:latest .`, `docker push ghcr.io/llama-index:latest`, `kubectl set image deployment/llama-index llama-index=ghcr.io/llama-index:latest`, `helm upgrade llama-index ./helm-chart --namespace production`, then `kubectl rollout status deployment/llama-index --timeout=300s`. Confirm context with llama-index --version --port 8080` or `docker run -p 8080:8080 llama_index-server`. Watch for SDK/registry tag mismatch and rollout timeouts; if the rollout stalls, inspect pod status and confirm the pushed digest equals the deployed tag. Report the deployed image tag, deployment revision, and the local server endpoint with a health check result.

## Capabilities

### Ml Llama Index Deploy Sdk Agent
LlamaIndex SDK deployment agent for ML LlamaIndex SDK deployment.

**Commands:**
- `docker build -t llama-index:latest .`
- `docker push ghcr.io/llama-index:latest`
- `kubectl set image deployment/llama-index llama-index=ghcr.io/llama-index:latest`
- `helm upgrade llama-index ./helm-chart --namespace production`
- `kubectl rollout status deployment/llama-index --timeout=300s`
- `llama-index --version`

**Examples:**
- Server: python -m llama_index.server --port 8080
- Docker: docker run -p 8080:8080 llama_index-server
