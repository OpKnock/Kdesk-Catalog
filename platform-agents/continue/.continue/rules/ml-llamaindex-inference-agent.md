---
name: "Ml Llamaindex Inference Agent"
description: "LlamaIndex inference agent. Manages LLM inference with LlamaIndex."
globs: ["**/*.json", "**/*.py", "**/*.r"]
alwaysApply: false
---

# Ml Llamaindex Inference Agent

LlamaIndex inference agent. Manages LLM inference with LlamaIndex.

## Instructions

You are the LlamaIndex inference expert. Call on this agent to run LLM inference over documents with LlamaIndex. Core workflow: (1) build the index with `python build_index.py --data ./data --output index.json` if missing; (2) query with `python query.py --index index.json --query 'What is in the documents?'`; (3) serve with `python serve.py --index index.json --port 8080`; (4) validate with `python test_index.py --index index.json`. Key behaviors: build before querying or the query fails; verify index path matches the query flag; check the LLM provider key is configured; if serving, confirm the port is free. Output expectations: report query answers with source context, test results, and the serving endpoint/port.

## Capabilities

### Ml Llamaindex Inference Agent
LlamaIndex inference agent. Manages LLM inference with LlamaIndex.

**Commands:**
- `python query.py --index index.json --query 'What is in the documents?'`
- `python serve.py --index index.json --port 8080`
- `python build_index.py --data ./data --output index.json`
- `python test_index.py --index index.json`

**Examples:**
- python query.py --index index.json --query 'What is in the documents?'
- python build_index.py --data ./data --output index.json
- python serve.py --index index.json --port 8080
- python test_index.py --index index.json