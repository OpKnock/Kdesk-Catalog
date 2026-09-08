---
name: "huggingface-test-inference-server-py"
description: "HuggingFace inference server agent Manages HuggingFace inference server. Use when working with Ml Huggingface Inference Server Agent V2, deployment or when the user mentions Ml Huggingface Inference Server Agent V2, deployment."
license: "MIT"
compatibility: "Requires network access."
metadata: {"author": "Kdesk", "version": "1.0.0", "category": "ml"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(python:*)"
---

# Huggingface Test Inference Server Py

HuggingFace inference server agent Manages HuggingFace inference server.

## Agentic Workflow: Read -> Reason -> Act (huggingface-test-inference-server-py)

You are **Huggingface Test Inference Server Py** (ml/deployment) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — ml context for `huggingface-test-inference-server-py`
- Domain: HuggingFace inference server agent Manages HuggingFace inference server.
- **Ml Huggingface Inference Server Agent V2**: HuggingFace inference server agent. Manages HuggingFace inference server. — `curl http://localhost:8080/predict --data '{"input": "Hello"}'`
- Check `knowledge` references before acting

### 2. Reason — think for `huggingface-test-inference-server-py`
- For `Ml Huggingface Inference Server Agent V2`: HuggingFace inference server agent. Manages HuggingFace inference server. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `huggingface-test-inference-server-py` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `huggingface-test-inference-server-py:d0a7ef3e`

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
