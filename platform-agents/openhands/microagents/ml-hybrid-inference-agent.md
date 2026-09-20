---
name: "ml-hybrid-inference-agent"
description: "Hybrid inference agent. Manages hybrid cloud-edge ML inference."
type: knowledge
triggers: ["ml-hybrid-inference-agent", "ml hybrid inference agent"]
---

# Ml Hybrid Inference Agent

Hybrid inference agent. Manages hybrid cloud-edge ML inference.

## Instructions

Hybrid cloud-edge inference operator. Call on this agent to run inference across cloud and edge models in a hybrid setup. Configure routing with `python hybrid_config.py --cloud-endpoint https://api.openai.com --edge-endpoint http://localhost:8081`, deploy both sides with `python hybrid_deploy.py --cloud-model gpt-4 --edge-model model.tflite`, and serve with `python hybrid_server.py --port 8080`. Validate the setup with `python test_hybrid.py --endpoint http://localhost:8080`. Common failure modes: cloud quota/auth failures, edge model format errors, and fallback not triggering when the cloud is unreachable; verify the fallback path explicitly. Report routing config, per-side health, and inference test results. Cross-check with examples like `python hybrid_deploy.py --cloud-model gpt-4 --edge-model model.tflite` and `python hybrid_server.py --port 8080` and `python test_hybrid.py --endpoint http://localhost:8080` and `python hybrid_config.py --cloud-endpoint https://api.openai.com --edge-endpoint http://localhost:8081`.

## Capabilities

### Ml Hybrid Inference Agent
Hybrid inference agent. Manages hybrid cloud-edge ML inference.

**Commands:**
- `python hybrid_config.py --cloud-endpoint https://api.openai.com --edge-endpoint http://localhost:808`
- `python hybrid_deploy.py --cloud-model gpt-4 --edge-model model.tflite`
- `python test_hybrid.py --endpoint http://localhost:8080`
- `python hybrid_server.py --port 8080`

**Examples:**
- python hybrid_deploy.py --cloud-model gpt-4 --edge-model model.tflite
- python hybrid_server.py --port 8080
- python test_hybrid.py --endpoint http://localhost:8080
- python hybrid_config.py --cloud-endpoint https://api.openai.com --edge-endpoint http://localhost:8081
