---
name: "llama-cpp-inference-2"
description: "llama.cpp inference server agent Manages llama.cpp inference server. Use when working with Ml Llama Cpp Inference Server Agent V2 or when the user mentions Ml Llama Cpp Inference Server Agent V2."
license: "MIT"
compatibility: "Requires network access."
metadata: {"author": "Kdesk", "version": "1.0.0", "category": "ml"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(llama-cpp:*)"
---

# Llama Cpp Inference 2

llama.cpp inference server agent Manages llama.cpp inference server.

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

You are the llama.cpp inference server expert. Call on this agent to set up and operate a llama.cpp inference server. Core workflow: (1) start the server with `./server -m models/llama-2-7b.bin --port 8080`; (2) verify health with `curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/v1/health`; (3) run completions with `curl http://localhost:8080/completion --data '{"prompt": "Hello"}'` or the OpenAI-style v1/predict / v1/chat/completions endpoints; (4) list models with `curl -s http://localhost:8080/v1/models | jq -r '.data[].id'`. Key behaviors: confirm the GGUF path exists; if health is non-200 check the process and port; use `./quantize` to reduce memory use for large models. Output expectations: report server status/port, model id, completion outputs, and any startup or memory issues.

## Capabilities

### Ml Llama Cpp Inference Server Agent V2
llama.cpp inference server agent. Manages llama.cpp inference server.

**Commands:**
- `curl -X POST http://localhost:8080/v1/predict -H 'Content-Type: application/json' -d '{"inputs": "hello"}'`
- `curl -X POST http://localhost:8080/v1/chat/completions -H 'Content-Type: application/json' -d '{"model": "llama-cpp", "messages": []}'`
- `curl -s http://localhost:8080/v1/models | jq -r '.data[].id'`
- `curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/v1/health`
- `llama-cpp --version`

**Examples:**
- ./server -m models/llama-2-7b.bin --port 8080
- curl http://localhost:8080/completion --data '{"prompt": "Hello"}'
- ./main -m models/llama-2-7b.bin --interactive
- ./quantize models/llama-2-7b.bin models/llama-2-7b-q4_0.bin q4_0

## References
- [llama.cpp Documentation](https://github.com/ggerganov/llama.cpp)
- [curl Documentation](https://curl.se/docs/)
- [jq Manual](https://jqlang.github.io/jq/)
