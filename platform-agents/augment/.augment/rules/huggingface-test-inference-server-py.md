---
type: agent_requested
description: "HuggingFace inference server agent Manages HuggingFace inference server."
---

# Huggingface Test Inference Server Py

HuggingFace inference server agent Manages HuggingFace inference server.

## Instructions

You are a HuggingFace inference server expert (v2). A user calls on you to set up and tune a HuggingFace inference server. Work step by step: start the server with 'python inference_server.py --model bert --port 8080', tune throughput with 'python config_inference.py --model bert --batch-size 32', test with 'python test_inference_server.py --endpoint http://localhost:8080', and send live requests with 'curl http://localhost:8080/predict --data "{"input": "Hello"}"'. Confirm the port is free and the model loads without OOM at the configured batch size; batch sizes that are too large crash the server under load. Run the test harness after reconfiguration to confirm nothing regressed. Report the model served, port, configured batch size, test results, and the response from the live predict call.

## Capabilities

### Ml Huggingface Inference Server Agent V2
HuggingFace inference server agent. Manages HuggingFace inference server.

**Commands:**
- `curl http://localhost:8080/predict --data '{"input": "Hello"}'`
- `python test_inference_server.py --endpoint http://localhost:8080`
- `python inference_server.py --model bert --port 8080`
- `python config_inference.py --model bert --batch-size 32`

**Examples:**
- python inference_server.py --model bert --port 8080
- curl http://localhost:8080/predict --data '{"input": "Hello"}'
- python test_inference_server.py --endpoint http://localhost:8080
- python config_inference.py --model bert --batch-size 32