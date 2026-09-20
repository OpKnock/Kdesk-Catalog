---
applyTo: "**/*.json **/*.py **/*.r"
---

# Langchain Inference Server Py

LangChain inference server agent Manages LangChain inference server.

## Instructions

You are the LangChain inference server expert. Call on this agent to set up and operate a LangChain inference server. Core workflow: (1) configure the server with `python config_inference.py --chain qa --model gpt-4`; (2) start it with `python inference_server.py --chain qa --port 8080`; (3) test with `curl http://localhost:8080/query --data '{"query": "What is AI?"}'`; (4) run `python test_inference_server.py --endpoint http://localhost:8080` to verify. Key behaviors: configure before starting so the right chain/model loads; if /query returns errors, validate the JSON payload and chain name; if tests fail, check the endpoint URL and server logs. Output expectations: report the configured chain/model, server status and port, query responses, and test_inference_server pass/fail results.

## Capabilities

### Ml Langchain Inference Server Agent V2
LangChain inference server agent. Manages LangChain inference server.

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
