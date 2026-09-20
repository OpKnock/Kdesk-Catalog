---
name: "hybrid-inference"
description: "Hybrid inference server agent. Manages hybrid cloud-edge ML inference server."
type: knowledge
triggers: ["hybrid-inference", "ml hybrid inference server agent"]
---

# Hybrid Inference

Hybrid inference server agent. Manages hybrid cloud-edge ML inference server.

## Instructions

Hybrid inference server expert. Call on this agent to set up and operate the Hybrid inference server. Verify with `curl -X POST http://localhost:8080/v1/predict -H 'Content-Type: application/json' -d '{"inputs": "hello"}'`, chat completions via `curl -X POST http://localhost:8080/v1/chat/completions -H 'Content-Type: application/json' -d '{"model": "hybrid", "messages": []}'`, list models with `curl -s http://localhost:8080/v1/models | jq -r '.data[].id'`, and probe liveness with `curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/v1/health`. Failure modes: server down, model not loaded (empty model list), schema drift (400/422); check health, then models, then payload. Cross-check with tooling such as `python hybrid_server.py --port 8080` and `curl http://localhost:8080/predict --data '{"input": "Hello"}'` and `python test_hybrid_server.py --endpoint http://localhost:8080` and `python config_hybrid.py --cloud-model gpt-4 --edge-model model.tflite`. Report the health code, model IDs, a sample prediction, and errors with fixes.

## Capabilities

### Ml Hybrid Inference Server Agent
Hybrid inference server agent. Manages hybrid cloud-edge ML inference server.

**Commands:**
- `curl -X POST http://localhost:8080/v1/predict -H 'Content-Type: application/json' -d '{"inputs": "hello"}'`
- `curl -X POST http://localhost:8080/v1/chat/completions -H 'Content-Type: application/json' -d '{"model": "hybrid", "messages": []}'`
- `curl -s http://localhost:8080/v1/models | jq -r '.data[].id'`
- `curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/v1/health`

**Examples:**
- python hybrid_server.py --port 8080
- curl http://localhost:8080/predict --data '{"input": "Hello"}'
- python test_hybrid_server.py --endpoint http://localhost:8080
- python config_hybrid.py --cloud-model gpt-4 --edge-model model.tflite
