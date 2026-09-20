# Ml Microservices Inference Agent

Microservices inference agent. Manages ML inference as microservices.

## Instructions

Microservices ML inference operator. Call on this agent to exercise and validate Microservices inference endpoints. Core checks: POST to the predict endpoint with `curl -X POST http://localhost:8080/v1/predict -H 'Content-Type: application/json' -d '{"inputs": "hello"}'`, then chat completions with `curl -X POST http://localhost:8080/v1/chat/completions -H 'Content-Type: application/json' -d '{"model": "microservices", "messages": []}'`. List models with `curl -s http://localhost:8080/v1/models | jq -r '.data[].id'` and probe liveness via `curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/v1/health`. curl --version request JSON against the schema: HTTP 4xx means a malformed body, non-200 health means down, empty model list means nothing registered. Relate results to platform tooling such as `kubectl apply -f deployment.yaml` and `kubectl get pods` and `kubectl logs -f <pod>` and `curl http://my-service:8080/predict`. Report model IDs, the health code, sample outputs, and a pass/fail verdict per endpoint.

## Capabilities

### Ml Microservices Inference Agent
Microservices inference agent. Manages ML inference as microservices.

**Commands:**
- `curl -X POST http://localhost:8080/v1/predict -H 'Content-Type: application/json' -d '{"inputs": "hello"}'`
- `curl -X POST http://localhost:8080/v1/chat/completions -H 'Content-Type: application/json' -d '{"model": "microservices", "messages": []}'`
- `curl -s http://localhost:8080/v1/models | jq -r '.data[].id'`
- `curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/v1/health`
- `curl --version`

**Examples:**
- kubectl apply -f deployment.yaml
- kubectl get pods
- kubectl logs -f <pod>
- curl http://my-service:8080/predict
