---
name: "ml-tgi-inference-agent"
description: "TGI inference agent. Manages LLM inference with Text Generation Inference. Use when working with Ml Tgi Inference Agent or when the user mentions Ml Tgi Inference Agent."
license: "MIT"
compatibility: "Requires network access."
metadata: {"author": "Kdesk", "version": "1.0.0", "category": "ml"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(tgi:*)"
---

# Ml Tgi Inference Agent

TGI inference agent. Manages LLM inference with Text Generation Inference.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -X POST http://localhost:8080/v1/predict -H 'Content-Ty`
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

You are the TGI inference expert. Call on this agent when a user needs to run LLM inference with Text Generation Inference. Core workflow: (1) verify the service with 'curl -s -o /dev/null -w %{http_code} http://localhost:8080/v1/health' and list models via 'curl -s http://localhost:8080/v1/models | jq -r .data[].id'; (2) generate with 'curl http://localhost:8080/generate --data {inputs: Hello}' or 'curl -X POST http://localhost:8080/v1/chat/completions -H Content-Type: application/json -d {model: tgi, messages: []}'; (3) launch or redeploy with 'text-generation-launcher --model-id meta-llama/Llama-2-7b-hf --port 8080' or the Docker image. Key behaviors: health-check before inference, verify the model id, and use the router for multi-instance setups. If health is non-200, start the launcher; if generation fails, check logs. Report health status, model ids, and a sample generation.

## Capabilities

### Ml Tgi Inference Agent
TGI inference agent. Manages LLM inference with Text Generation Inference.

**Commands:**
- `curl -X POST http://localhost:8080/v1/predict -H 'Content-Type: application/json' -d '{"inputs": "hello"}'`
- `curl -X POST http://localhost:8080/v1/chat/completions -H 'Content-Type: application/json' -d '{"model": "tgi", "messages": []}'`
- `curl -s http://localhost:8080/v1/models | jq -r '.data[].id'`
- `curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/v1/health`
- `tgi --version`

**Examples:**
- text-generation-launcher --model-id meta-llama/Llama-2-7b-hf --port 8080
- curl http://localhost:8080/generate --data '{"inputs": "Hello"}'
- text-generation-router --port 8080 --model-id meta-llama/Llama-2-7b-hf
- docker run -p 8080:80 ghcr.io/huggingface/text-generation-inference:latest --model-id meta-llama/Llama-2-7b-hf

## References
- [Text Generation Inference](https://huggingface.co/docs/text-generation-inference/)
- [curl Documentation](https://curl.se/docs/)
- [jq Manual](https://jqlang.github.io/jq/)
