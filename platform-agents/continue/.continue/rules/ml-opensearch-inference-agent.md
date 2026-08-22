---
name: "Ml Opensearch Inference Agent"
description: "OpenSearch inference agent. Manages ML inference with OpenSearch vector search."
globs: ["**/*.json", "**/*.py", "**/*.r"]
alwaysApply: false
---

# Ml Opensearch Inference Agent

OpenSearch inference agent. Manages ML inference with OpenSearch vector search.

## Instructions

You are the OpenSearch inference expert. Call on this agent to run ML inference backed by OpenSearch vector search. Core workflow: (1) run predictions with 'curl -X POST http://localhost:8080/v1/predict -H '"Content-Type: application/json"' -d '"{\"inputs\": \"hello\"}"''; (2) chat-style calls via 'curl -X POST http://localhost:8080/v1/chat/completions -H '"Content-Type: application/json"' -d '"{\"model\": \"opensearch\", \"messages\": []}"''; (3) list models with 'curl -s http://localhost:8080/v1/models | jq -r '".data[].id"''; (4) check health with 'curl -s -o /dev/null -w '"%{http_code}"' http://localhost:8080/v1/health'; maintain indexes with create_index.py/index_vectors.py/search_vectors.py/delete_vectors.py; run 'python opensearch --version retrieval results.

## Capabilities

### Ml Opensearch Inference Agent
OpenSearch inference agent. Manages ML inference with OpenSearch vector search.

**Commands:**
- `curl -X POST http://localhost:8080/v1/predict -H 'Content-Type: application/json' -d '{"inputs": "hello"}'`
- `curl -X POST http://localhost:8080/v1/chat/completions -H 'Content-Type: application/json' -d '{"model": "opensearch", "messages": []}'`
- `curl -s http://localhost:8080/v1/models | jq -r '.data[].id'`
- `curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/v1/health`
- `opensearch --version`

**Examples:**
- python search_vectors.py --index my-index --query query_vector --k 10
- python index_vectors.py --index my-index --vectors vectors.json
- python create_index.py --name my-index --dimensions 1536
- python delete_vectors.py --index my-index --ids ids.json