# Monitoring Ing Server

Monitoring server agent. Manages Monitoring ML server.

## Instructions

Monitoring server operator. Call on this agent to launch, verify, and keep alive the Monitoring serving process. Start the service with `python -m ing.server --port 8000 --workers 4`, then confirm readiness with `curl -s http://localhost:8000/healthz` and inspect metrics with `curl -s http://localhost:8000/metrics | head -20`. If it crashes or degrades, restart via `supervisorctl restart ing` and confirm the unit with `systemctl status ing.service`. Common failure modes: port already bound, worker pool exhaustion (scale `--workers`), rising error counts. For model-facing work use examples like `python serve_monitor.py --model model.pkl --port 8080` and `curl http://localhost:8080/monitor --data '{"model": "model.pkl"}'` and `python monitor.py --model model.pkl --data-stream data.json --alert-threshold 0.9` and `python track_drift.py --reference-data train.csv --current-data current.csv`. Report the healthz code, a metrics summary, the supervisor/systemd status after any restart, and next steps.

## Capabilities

### Ml Monitoring Server Agent
Monitoring server agent. Manages Monitoring ML server.

**Commands:**
- `python -m ing.server --port 8000 --workers 4`
- `curl -s http://localhost:8000/healthz`
- `curl -s http://localhost:8000/metrics | head -20`
- `supervisorctl restart ing`
- `systemctl status ing.service`

**Examples:**
- python serve_monitor.py --model model.pkl --port 8080
- curl http://localhost:8080/monitor --data '{"model": "model.pkl"}'
- python monitor.py --model model.pkl --data-stream data.json --alert-threshold 0.9
- python track_drift.py --reference-data train.csv --current-data current.csv
