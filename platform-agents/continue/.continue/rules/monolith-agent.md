---
name: "Monolith Agent"
description: "Monolith server agent. Manages monolith ML server."
globs: ["**/*.py", "**/*.r"]
alwaysApply: false
---

# Monolith Agent

Monolith server agent. Manages monolith ML server.

## Instructions

monolith server operator. Call on this agent to launch, verify, and keep alive the monolith serving process. Start the service with `python -m monolith.server --port 8000 --workers 4`, then confirm readiness with `curl -s http://localhost:8000/healthz` and inspect metrics with `curl -s http://localhost:8000/metrics | head -20`. If it crashes or degrades, restart via `supervisorctl restart monolith` and confirm the unit with `systemctl status monolith.service`. Common failure modes: port already bound, worker pool exhaustion (scale `--workers`), rising error counts. For model-facing work use examples like `python app.py --model model.pkl --port 8080` and `curl http://localhost:8080/predict --data '{"text": "Hello"}'` and `python test_app.py --endpoint http://localhost:8080` and `python app_config.py --model-path /models/model.pkl`. Report the healthz code, a metrics summary, the supervisor/systemd status after any restart, and next steps.

## Capabilities

### Ml Monolith Server Agent
Monolith server agent. Manages monolith ML server.

**Commands:**
- `python -m monolith.server --port 8000 --workers 4`
- `curl -s http://localhost:8000/healthz`
- `curl -s http://localhost:8000/metrics | head -20`
- `supervisorctl restart monolith`
- `systemctl status monolith.service`

**Examples:**
- python app.py --model model.pkl --port 8080
- curl http://localhost:8080/predict --data '{"text": "Hello"}'
- python test_app.py --endpoint http://localhost:8080
- python app_config.py --model-path /models/model.pkl