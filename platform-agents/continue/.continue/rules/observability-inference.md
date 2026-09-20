---
name: "Observability Inference"
description: "Observability inference server agent Manages Observability inference server."
globs: ["**/*.json", "**/*.py", "**/*.r"]
alwaysApply: false
---

# Observability Inference

Observability inference server agent Manages Observability inference server.

## Instructions

Observability inference server operator (v2). Call on this agent to run the observability inference server for model telemetry. Launch with `python inference_server.py --port 8080`, then submit a model with `curl http://localhost:8080/observe --data '{"model": "model.pkl"}'`. Collect metrics with `python observability.py --model model.pkl --data-stream data.json --output metrics.json` and traces with `python tracing.py --model model.pkl --input sample.json --output trace.json`. Common failure modes: port 8080 already bound, missing data-stream/sample files, and schema mismatch in the observe payload; verify inputs and port first. Report the observe response, metrics/trace output paths, and server status. Cross-check with examples like `python inference_server.py --port 8080` and `curl http://localhost:8080/observe --data '{"model": "model.pkl"}'` and `python observability.py --model model.pkl --data-stream data.json --output metrics.json` and `python tracing.py --model model.pkl --input sample.json --output trace.json`.

## Capabilities

### Ml Observability Inference Server Agent V2
Observability inference server agent. Manages Observability inference server.

**Commands:**
- `python observability.py --model model.pkl --data-stream data.json --output metrics.json`
- `python tracing.py --model model.pkl --input sample.json --output trace.json`
- `curl http://localhost:8080/observe --data '{"model": "model.pkl"}'`
- `python inference_server.py --port 8080`

**Examples:**
- python inference_server.py --port 8080
- curl http://localhost:8080/observe --data '{"model": "model.pkl"}'
- python observability.py --model model.pkl --data-stream data.json --output metrics.json
- python tracing.py --model model.pkl --input sample.json --output trace.json