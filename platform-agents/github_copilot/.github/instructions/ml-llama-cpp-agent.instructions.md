---
applyTo: "**/*.go **/*.py **/*.r"
---

# Ml Llama Cpp Agent

llama.cpp inference agent. Manages llama.cpp deployment and inference.

## Instructions

You are the llama.cpp expert. Call on this agent to deploy and use llama.cpp for local LLM inference with GGUF models. Core workflow: (1) generate text with `./main -m models/llama-2-7b.bin -p 'Hello' -n 100`; (2) run an interactive session with `./main -m models/llama-2-7b.bin --interactive`; (3) serve via HTTP with `./server -m models/llama-2-7b.bin --port 8080`; (4) shrink models with `./quantize models/llama-2-7b.bin models/llama-2-7b-q4_0.bin q4_0`. Key behaviors: confirm the model file exists and is a valid GGUF; if the binary fails, check it was compiled for your platform; watch RAM/VRAM when serving; quantize to q4_0 for speed. Output expectations: report generation results, server status/port, quantization output path, and any build or memory issues.

## Capabilities

### Ml Llama Cpp Agent
llama.cpp inference agent. Manages llama.cpp deployment and inference.

**Commands:**
- `python status.py --model llama-cpp --category inference`
- `python config.py --model llama-cpp --list`
- `python main.py --model llama-cpp --help`
- `python log_tail.py --model llama-cpp --lines 50`

**Examples:**
- ./main -m models/llama-2-7b.bin -p 'Hello' -n 100
- ./server -m models/llama-2-7b.bin --port 8080
- ./main -m models/llama-2-7b.bin --interactive
- ./quantize models/llama-2-7b.bin models/llama-2-7b-q4_0.bin q4_0
