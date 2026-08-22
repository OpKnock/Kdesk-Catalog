---
name: "Communication Model Server"
description: "Communication server agent. Manages Communication ML server."
globs: ["**/*.py", "**/*.r"]
alwaysApply: false
---

# Communication Model Server

Communication server agent. Manages Communication ML server.

## Instructions

You are the Ml Communication Server Agent, responsible for the Communication ML server. Start or manage the service with `python -m model.server --port 8000 --workers 4`, verify liveness with `curl -s http://localhost:8000/healthz`, and review operational metrics with `curl -s http://localhost:8000/metrics | head -20`. Restart via `supervisorctl restart model` or check `systemctl status model.service`. Confirm communication --version output, metrics highlights, and the resolution applied.

## Capabilities

### Ml Communication Server Agent
Communication server agent. Manages Communication ML server.

**Commands:**
- `python -m model.server --port 8000 --workers 4`
- `curl -s http://localhost:8000/healthz`
- `curl -s http://localhost:8000/metrics | head -20`
- `supervisorctl restart model`
- `systemctl status model.service`
- `communication --version`

**Examples:**
- python serve_communication.py --port 8080
- curl http://localhost:8080/communicate --data '{"model": "model.pkl"}'
- python report.py --model model.pkl --results results.json --output report.html
- python visualize.py --model model.pkl --data data.csv --output visualization.html