---
name: "fireworks-inference"
description: "Fireworks inference server agent. Manages Fireworks ML inference server."
type: knowledge
triggers: ["fireworks-inference", "ml fireworks inference server agent"]
---

# Fireworks Inference

Fireworks inference server agent. Manages Fireworks ML inference server.

## Instructions

Fireworks inference server expert. Call on this agent to set up and operate the Fireworks inference server. Verify with `curl -X POST http://localhost:8080/v1/predict -H 'Content-Type: application/json' -d '{"inputs": "hello"}'`, chat completions via `curl -X POST http://localhost:8080/v1/chat/completions -H 'Content-Type: application/json' -d '{"model": "fireworks", "messages": []}'`, list models with `curl -s http://localhost:8080/v1/models | jq -r '.data[].id'`, and probe liveness with `curl -s -o fireworks --version --agent fireworks-inference`. Failure modes: server down, model not loaded (empty model list), schema drift (400/422); check health, then models, then payload. Cross-check with tooling such as `fireworks login` and `fireworks serve --model accounts/fireworks/models/llama-v2-70b-chat` and `curl https://my-model.fireworks.ai/` and `fireworks models list`. Report the health code, model IDs, a sample prediction, and errors with fixes.

## Capabilities

### Ml Fireworks Inference Server Agent
Fireworks inference server agent. Manages Fireworks ML inference server.

**Commands:**
- `curl -X POST http://localhost:8080/v1/predict -H 'Content-Type: application/json' -d '{"inputs": "hello"}'`
- `curl -X POST http://localhost:8080/v1/chat/completions -H 'Content-Type: application/json' -d '{"model": "fireworks", "messages": []}'`
- `curl -s http://localhost:8080/v1/models | jq -r '.data[].id'`
- `curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/v1/health`
- `fireworks --version`

**Examples:**
- fireworks login
- fireworks serve --model accounts/fireworks/models/llama-v2-70b-chat
- curl https://my-model.fireworks.ai/
- fireworks models list
