---
trigger: glob
description: "Observability inference server agent Manages Observability inference server. Use when working with Ml Observability Inference Server Agent V2 or when the user mentions Ml Observability Inference Server Agent V2."
globs: ["**/*.json", "**/*.py", "**/*.r"]
---

# Observability Inference

Observability inference server agent Manages Observability inference server.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `python observability.py --model model.pkl --data-stream data`
- Check `knowledge` references and prerequisites before proceeding

### 2. Reason
Analyze and plan:
- Compare current state vs desired state (drift, checksums, policy)
- Evaluate trust, compatibility, and risk: use `kdesk trust` and `kdesk doctor` patterns
- Decide: which capabilities/tools are needed, which can be skipped

### 3. Act
Execute with guards:
- Run only `allowed-tools` (see frontmatter); use `safe_path` for writes
- Prefer `Bash` with explicit binaries (`curl`, `kubectl`, `kdesk`) over generic shell
- Record evidence: file paths, checksums, and tool outputs for verification

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
