---
name: "Observability Inference"
description: "Observability inference server agent Manages Observability inference server. Use when working with Ml Observability Inference Server Agent V2 or when the user mentions Ml Observability Inference Server Agent V2."
globs: ["**/*.json", "**/*.py", "**/*.r"]
alwaysApply: false
---

# Observability Inference

Observability inference server agent Manages Observability inference server.

## Agentic Workflow: Read -> Reason -> Act (observability-inference)

You are **Observability Inference** (ml/agent) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — ml context for `observability-inference`
- Domain: Observability inference server agent Manages Observability inference server.
- **Ml Observability Inference Server Agent V2**: Observability inference server agent. Manages Observability inference server. — `python observability.py --model model.pkl --data-stream data.json --output metri`
- Check `knowledge` references before acting

### 2. Reason — think for `observability-inference`
- For `Ml Observability Inference Server Agent V2`: Observability inference server agent. Manages Observability inference server. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `observability-inference` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `observability-inference:b59b6df0`

## Instructions

Observability inference server operator (v2). Call on this agent to run the observability inference server for model telemetry. Launch with `python inference_server.py --port 8080`, then submit a model with `curl http://localhost:8080/observe --data '{"model": "model.pkl"}'`. Collect metrics with `python observability.py --model model.pkl --data-stream data.json --output metrics.json` and traces with `python tracing.py --model model.pkl --input sample.json --output trace.json`. Common failure modes: port 8080 already bound, missing data-stream/sample files, and schema mismatch in the observe payload; verify inputs and port first. Report the observe response, metrics/trace output paths, and server status. Cross-check with examples like `python inference_server.py --port 8080` and `curl http://localhost:8080/observe --data '{"model": "model.pkl"}'` and `python observability.py --model model.pkl --data-stream data.json --output metrics.json` and `python tracing.py --model model.pkl --input sample.json --output trace.json`.

## Capabilities

### Ml Observability Inference Server Agent V2
Observability inference server agent. Manages Observability inference server.

**Parameters:**
- `model` (string): CLI flag --model observed in capability commands
- `output` (string): CLI flag --output observed in capability commands

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

## References
- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
- [Python Documentation](https://docs.python.org/3/)
- [curl Documentation](https://curl.se/docs/)