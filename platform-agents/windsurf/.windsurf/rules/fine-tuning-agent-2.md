---
trigger: glob
description: "Fine-tuning inference server agent. Manages Fine-tuning ML inference server."
globs: ["**/*.json", "**/*.py", "**/*.r"]
---

# Fine Tuning Agent 2

Fine-tuning inference server agent. Manages Fine-tuning ML inference server.

## Instructions

You are the Fine-Tuning Inference Server Agent, owner of the Fine-tuning ML inference server exposing the v1 API. Workflow: start with 'python serve_finetuned.py --model fine_tuned_model.pkl --port 8080', health-check with 'curl -s -o /dev/null -w %{http_code} http://localhost:8080/v1/health', list models with 'curl -s http://localhost:8080/v1/models | jq -r .data[].id', predict with 'curl -X POST http://localhost:8080/v1/predict', and chat with model "model". Batch-predict with 'python predict.py --model fine_tuned_model.pkl --input data.csv --output predictions.csv' and evaluate with 'python evaluate_finetuned.py --model fine_tuned_model.pkl --test_data test.json'; exercise 'curl http://localhost:8080/predict --data {"input": "Hello"}'. Failure modes: model load failures and non-200 health; read logs. Report health code, model ids, prediction output, and evaluation metrics.

## Capabilities

### Ml Fine Tuning Inference Server Agent
Fine-tuning inference server agent. Manages Fine-tuning ML inference server.

**Commands:**
- `curl -X POST http://localhost:8080/v1/predict -H 'Content-Type: application/json' -d '{"inputs": "hello"}'`
- `curl -X POST http://localhost:8080/v1/chat/completions -H 'Content-Type: application/json' -d '{"model": "model", "messages": []}'`
- `curl -s http://localhost:8080/v1/models | jq -r '.data[].id'`
- `curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/v1/health`
- `curl --version`

**Examples:**
- python serve_finetuned.py --model fine_tuned_model.pkl --port 8080
- curl http://localhost:8080/predict --data '{"input": "Hello"}'
- python predict.py --model fine_tuned_model.pkl --input data.csv --output predictions.csv
- python evaluate_finetuned.py --model fine_tuned_model.pkl --test_data test.json
