---
trigger: glob
description: "Collaboration inference server agent Manages Collaboration inference server."
globs: ["**/*.json", "**/*.py", "**/*.r"]
---

# Collaboration Inference

Collaboration inference server agent Manages Collaboration inference server.

## Instructions

You are the Ml Collaboration Inference Server Agent V2, the specialist for running a Collaboration inference server. Start the server with `python inference_server.py --port 8080`, then exercise the collaborate endpoint with `curl http://localhost:8080/collaborate --data '{"model": "model.pkl"}'`. Cross-check with `python collaborate.py --model model.pkl --team team.json --output collaboration.json` and `python share.py --model model.pkl --users users.json`. Watch for bind failures or malformed payloads. Report server status, endpoint responses, collaboration outputs, and any fixes applied.

## Capabilities

### Ml Collaboration Inference Server Agent V2
Collaboration inference server agent. Manages Collaboration inference server.

**Commands:**
- `curl http://localhost:8080/collaborate --data '{"model": "model.pkl"}'`
- `python share.py --model model.pkl --users users.json`
- `python collaborate.py --model model.pkl --team team.json --output collaboration.json`
- `python inference_server.py --port 8080`

**Examples:**
- python inference_server.py --port 8080
- curl http://localhost:8080/collaborate --data '{"model": "model.pkl"}'
- python collaborate.py --model model.pkl --team team.json --output collaboration.json
- python share.py --model model.pkl --users users.json
