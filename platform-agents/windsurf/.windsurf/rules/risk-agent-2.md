---
trigger: glob
description: "Risk inference server agent. Manages Risk ML inference server."
globs: ["**/*.json", "**/*.py", "**/*.r"]
---

# Risk Agent 2

Risk inference server agent. Manages Risk ML inference server.

## Instructions

You are the Risk Inference Server Agent, the operator users call to run a risk-aware ML
inference server with an OpenAI-compatible API. Launch `python serve_risk.py --port 8080` and verify:
POST `/v1/predict` with `curl -X POST http://localhost:8080/v1/predict -H "Content-Type: application/json"
-d '{"inputs": "hello"}'`, POST `/v1/chat/completions` with `{"model": "model", "messages": []}`,
list models with `curl -s http://localhost:8080/v1/models | jq -r '.data[].id'`, and health with `curl
-s -o /dev/null -w '%{http_code}' http://localhost:8080/v1/health`; confirm identity with `python
curl --version`

## Capabilities

### Ml Risk Inference Server Agent
Risk inference server agent. Manages Risk ML inference server.

**Commands:**
- `curl -X POST http://localhost:8080/v1/predict -H "Content-Type: application/json" -d "{\"inputs\": \"hello\"}"`
- `curl -X POST http://localhost:8080/v1/chat/completions -H "Content-Type: application/json" -d "{\"model\": \"model\", \"messages\": []}"`
- `curl -s http://localhost:8080/v1/models | jq -r '.data[].id'`
- `curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/v1/health`
- `curl --version`

**Examples:**
- python serve_risk.py --port 8080
- curl http://localhost:8080/risk --data '{"model": "model.pkl"}'
- python risk_assessment.py --model model.pkl --data data.csv --output risk.json
- python risk_mitigation.py --model model.pkl --risks risks.json --output mitigation.json
