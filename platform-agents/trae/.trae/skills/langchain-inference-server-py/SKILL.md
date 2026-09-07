---
name: "langchain-inference-server-py"
description: "LangChain inference server agent Manages LangChain inference server. Use when working with Ml Langchain Inference Server Agent V2 or when the user mentions Ml Langchain Inference Server Agent V2."
license: "MIT"
compatibility: "Requires network access."
metadata: {"author": "Kdesk", "version": "1.0.0", "category": "ml"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(python:*)"
---

# Langchain Inference Server Py

LangChain inference server agent Manages LangChain inference server.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `python inference_server.py --chain qa --port 8080`
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

You are the LangChain inference server expert. Call on this agent to set up and operate a LangChain inference server. Core workflow: (1) configure the server with `python config_inference.py --chain qa --model gpt-4`; (2) start it with `python inference_server.py --chain qa --port 8080`; (3) test with `curl http://localhost:8080/query --data '{"query": "What is AI?"}'`; (4) run `python test_inference_server.py --endpoint http://localhost:8080` to verify. Key behaviors: configure before starting so the right chain/model loads; if /query returns errors, validate the JSON payload and chain name; if tests fail, check the endpoint URL and server logs. Output expectations: report the configured chain/model, server status and port, query responses, and test_inference_server pass/fail results.

## Capabilities

### Ml Langchain Inference Server Agent V2
LangChain inference server agent. Manages LangChain inference server.

**Parameters:**
- `chain` (string): CLI flag --chain observed in capability commands

**Commands:**
- `python inference_server.py --chain qa --port 8080`
- `python test_inference_server.py --endpoint http://localhost:8080`
- `curl http://localhost:8080/query --data '{"query": "What is AI?"}'`
- `python config_inference.py --chain qa --model gpt-4`

**Examples:**
- python inference_server.py --chain qa --port 8080
- curl http://localhost:8080/query --data '{"query": "What is AI?"}'
- python test_inference_server.py --endpoint http://localhost:8080
- python config_inference.py --chain qa --model gpt-4

## References
- [LangChain Documentation](https://python.langchain.com/docs/)
- [Python Documentation](https://docs.python.org/3/)
- [curl Documentation](https://curl.se/docs/)
