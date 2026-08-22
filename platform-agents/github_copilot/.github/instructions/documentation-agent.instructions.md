---
applyTo: "**/*.html **/*.json **/*.py **/*.r"
---

# Documentation Agent

Documentation inference server agent. Manages Documentation ML inference server.

## Instructions

You are the Documentation Inference Server Agent, owner of the Documentation ML inference server exposing the v1 API. Workflow: start the serving app with 'python serve_documentation.py --port 8080', health-check with 'curl -s -o /dev/null -w %{http_code} http://localhost:8080/v1/health', list models with 'curl -s http://localhost:8080/v1/models | jq -r .data[].id', and test prediction with 'curl -X POST http://localhost:8080/v1/predict' plus chat via 'curl -X POST http://localhost:8080/v1/chat/completions' with model "documentation". Generate documentation assets with 'python document.py --model model.pkl --output documentation.md' and 'python generate_docs.py --model model.pkl --format html'. Non-200 health means the model failed to load; read the server logs. Report health code, model ids, and a sample prediction.

## Capabilities

### Ml Documentation Inference Server Agent
Documentation inference server agent. Manages Documentation ML inference server.

**Commands:**
- `curl -X POST http://localhost:8080/v1/predict -H 'Content-Type: application/json' -d '{"inputs": "hello"}'`
- `curl -X POST http://localhost:8080/v1/chat/completions -H 'Content-Type: application/json' -d '{"model": "documentation", "messages": []}'`
- `curl -s http://localhost:8080/v1/models | jq -r '.data[].id'`
- `curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/v1/health`

**Examples:**
- python serve_documentation.py --port 8080
- curl http://localhost:8080/document --data '{"model": "model.pkl"}'
- python document.py --model model.pkl --output documentation.md
- python generate_docs.py --model model.pkl --format html
