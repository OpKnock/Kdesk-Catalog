---
name: "Ml Observability Inference Agent"
description: "Observability inference agent. Manages ML observability inference."
globs: ["**/*.json", "**/*.py", "**/*.r"]
alwaysApply: false
---

# Ml Observability Inference Agent

Observability inference agent. Manages ML observability inference.

## Instructions

ML observability operator. Call on this agent to collect metrics and traces for ML models in production. Run the metrics pass with `python observability.py --model model.pkl --data-stream data.json --output metrics.json`, capture request traces with `python tracing.py --model model.pkl --input sample.json --output trace.json`, and serve the observability endpoint with `python serve_observability.py --port 8080`. Validate the pipeline with `python test_observability.py` before reporting. Common failure modes: missing data-stream or sample input files, incompatible model serialization, and port conflicts; verify inputs and port first. Report metrics.json and trace.json paths, test results, and endpoint status. Cross-check with examples like `python observability.py --model model.pkl --data-stream data.json --output metrics.json` and `python tracing.py --model model.pkl --input sample.json --output trace.json` and `python serve_observability.py --port 8080` and `python test_observability.py`.

## Capabilities

### Ml Observability Inference Agent
Observability inference agent. Manages ML observability inference.

**Commands:**
- `python observability.py --model model.pkl --data-stream data.json --output metrics.json`
- `python serve_observability.py --port 8080`
- `python tracing.py --model model.pkl --input sample.json --output trace.json`
- `python test_observability.py`

**Examples:**
- python observability.py --model model.pkl --data-stream data.json --output metrics.json
- python tracing.py --model model.pkl --input sample.json --output trace.json
- python serve_observability.py --port 8080
- python test_observability.py