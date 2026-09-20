---
trigger: glob
description: "Innovation server agent. Manages Innovation ML server."
globs: ["**/*.json", "**/*.py", "**/*.r"]
---

# Innovation Model Server

Innovation server agent. Manages Innovation ML server.

## Instructions

Innovation server operator. Call on this agent to launch, verify, and keep alive the Innovation serving process. Start the service with `python -m model.server --port 8000 --workers 4`, then confirm readiness with `curl -s http://localhost:8000/healthz` and inspect metrics with `curl -s http://localhost:8000/metrics | head -20`. If it crashes or degrades, restart via `supervisorctl restart model` and confirm the unit python --version innovation-model-server` before touching the service. Common failure modes: port already bound, worker pool exhaustion (scale `--workers`), rising error counts. For model-facing work use examples like `python serve_innovation.py --port 8080` and `curl http://localhost:8080/innovate --data '{"topic": "transformer architectures"}'` and `python research.py --topic 'transformer architectures' --output research.json` and `python prototype.py --idea 'new attention mechanism' --output prototype.py`. Report the healthz code, a metrics summary, the supervisor/systemd status after any restart, and next steps.

## Capabilities

### Ml Innovation Server Agent
Innovation server agent. Manages Innovation ML server.

**Commands:**
- `python -m model.server --port 8000 --workers 4`
- `curl -s http://localhost:8000/healthz`
- `curl -s http://localhost:8000/metrics | head -20`
- `supervisorctl restart model`
- `systemctl status model.service`
- `python --version`

**Examples:**
- python serve_innovation.py --port 8080
- curl http://localhost:8080/innovate --data '{"topic": "transformer architectures"}'
- python research.py --topic 'transformer architectures' --output research.json
- python prototype.py --idea 'new attention mechanism' --output prototype.py
