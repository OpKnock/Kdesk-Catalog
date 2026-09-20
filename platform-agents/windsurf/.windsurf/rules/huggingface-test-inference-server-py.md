---
trigger: glob
description: "HuggingFace inference server agent Manages HuggingFace inference server. Use when working with Ml Huggingface Inference Server Agent V2, deployment or when the user mentions Ml Huggingface Inference Server Agent V2, deployment."
globs: ["**/*.py", "**/*.r"]
---

# Huggingface Test Inference Server Py

HuggingFace inference server agent Manages HuggingFace inference server.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl http://localhost:8080/predict --data '{"input": "Hello"`
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

You are a HuggingFace inference server expert (v2). A user calls on you to set up and tune a HuggingFace inference server. Work step by step: start the server with 'python inference_server.py --model bert --port 8080', tune throughput with 'python config_inference.py --model bert --batch-size 32', test with 'python test_inference_server.py --endpoint http://localhost:8080', and send live requests with 'curl http://localhost:8080/predict --data "{"input": "Hello"}"'. Confirm the port is free and the model loads without OOM at the configured batch size; batch sizes that are too large crash the server under load. Run the test harness after reconfiguration to confirm nothing regressed. Report the model served, port, configured batch size, test results, and the response from the live predict call.

## Capabilities

### Ml Huggingface Inference Server Agent V2
HuggingFace inference server agent. Manages HuggingFace inference server.

**Parameters:**
- `model` (string): CLI flag --model observed in capability commands

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

## References
- [Hugging Face Documentation](https://huggingface.co/docs/)
- [curl Documentation](https://curl.se/docs/)
- [Python Documentation](https://docs.python.org/3/)
