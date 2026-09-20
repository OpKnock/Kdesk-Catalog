---
name: "monitoring-inference"
description: "Monitoring inference server agent Manages Monitoring inference server."
---

# Monitoring Inference

Monitoring inference server agent Manages Monitoring inference server.

## Instructions

Monitoring inference server operator (v2). Call on this agent to run the monitoring inference server that serves model health checks. Launch with `python inference_server.py --model model.pkl --port 8080`, then submit a model for inspection with `curl http://localhost:8080/monitor --data '{"model": "model.pkl"}'`. Run drift detection with `python track_drift.py --reference-data train.csv --current-data current.csv` and the alert pass with `python monitor.py --model model.pkl --data-stream data.json --alert-threshold 0.9`. Common failure modes: port 8080 already bound, missing reference/current data files, and unreadable model.pkl; check files and port before restarting. Report the monitor endpoint response, drift result, alert status, and server state. Cross-check with examples like `python inference_server.py --model model.pkl --port 8080` and `curl http://localhost:8080/monitor --data '{"model": "model.pkl"}'` and `python monitor.py --model model.pkl --data-stream data.json --alert-threshold 0.9` and `python track_drift.py --reference-data train.csv --current-data current.csv`.

## Capabilities

### Ml Monitoring Inference Server Agent V2
Monitoring inference server agent. Manages Monitoring inference server.

**Commands:**
- `python track_drift.py --reference-data train.csv --current-data current.csv`
- `python monitor.py --model model.pkl --data-stream data.json --alert-threshold 0.9`
- `python inference_server.py --model model.pkl --port 8080`
- `curl http://localhost:8080/monitor --data '{"model": "model.pkl"}'`

**Examples:**
- python inference_server.py --model model.pkl --port 8080
- curl http://localhost:8080/monitor --data '{"model": "model.pkl"}'
- python monitor.py --model model.pkl --data-stream data.json --alert-threshold 0.9
- python track_drift.py --reference-data train.csv --current-data current.csv
