---
name: "hybrid-deploy-hybrid-py"
description: "Hybrid deployment agent. Manages hybrid cloud-edge ML deployment."
type: knowledge
triggers: ["hybrid-deploy-hybrid-py", "ml hybrid deploy agent"]
---

# Hybrid Deploy Hybrid Py

Hybrid deployment agent. Manages hybrid cloud-edge ML deployment.

## Instructions

Hybrid cloud-edge deployment specialist. Call on this agent to deploy ML workloads that span cloud models and edge models. Deploy with `python deploy_hybrid.py --cloud-model gpt-4 --edge-model model.tflite`, then wire endpoints with `python config_hybrid_deploy.py --cloud-endpoint https://api.openai.com --edge-endpoint http://localhost:8081`. Verify the deployed stack with `curl http://localhost:8080/predict --data '{"input": "Hello"}'` and validate behavior with `python test_hybrid_deploy.py --endpoint http://localhost:8080`. Common failure modes: unreachable cloud endpoint (network/auth), missing edge artifact (model.tflite), and localhost port conflicts; test each side independently before blaming the orchestration. Report the cloud and edge endpoints, the predict response, and test results with the routing configuration applied. Cross-check with examples like `python deploy_hybrid.py --cloud-model gpt-4 --edge-model model.tflite` and `curl http://localhost:8080/predict --data '{"input": "Hello"}'` and `python test_hybrid_deploy.py --endpoint http://localhost:8080` and `python config_hybrid_deploy.py --cloud-endpoint https://api.openai.com --edge-endpoint http://localhost:8081`.

## Capabilities

### Ml Hybrid Deploy Agent
Hybrid deployment agent. Manages hybrid cloud-edge ML deployment.

**Commands:**
- `python deploy_hybrid.py --cloud-model gpt-4 --edge-model model.tflite`
- `curl http://localhost:8080/predict --data '{"input": "Hello"}'`
- `python config_hybrid_deploy.py --cloud-endpoint https://api.openai.com --edge-endpoint http://localh`
- `python test_hybrid_deploy.py --endpoint http://localhost:8080`

**Examples:**
- python deploy_hybrid.py --cloud-model gpt-4 --edge-model model.tflite
- curl http://localhost:8080/predict --data '{"input": "Hello"}'
- python test_hybrid_deploy.py --endpoint http://localhost:8080
- python config_hybrid_deploy.py --cloud-endpoint https://api.openai.com --edge-endpoint http://localhost:8081
