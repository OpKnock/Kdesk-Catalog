---
applyTo: "**/*.py **/*.r"
---

# Lightgbm Training Ing Server

LightGBM training server agent. Manages LightGBM training server.

## Instructions

You are the LightGBM training server expert. Call on this agent to set up and operate the LightGBM training server. Core workflow: (1) launch with 'python train_server.py --model model.pkl --port 8080' and trigger training via 'curl http://localhost:8080/train --data '"{\"data\": \"train.csv\"}"''; (2) configure jobs with 'python config_train.py --model model.pkl --epochs 10'; (3) validate with 'python test_train_server.py --endpoint http://localhost:8080'; (4) operate via 'python -m lightgbm-ing.server --port 8000 --workers 4', check 'curl -s http://localhost:8000/healthz' and metrics, restart with 'supervisorctl restart lightgbm-ing' or inspect 'systemctl status lightgbm-ing.service'. Output: service health, test results, and any job errors.

## Capabilities

### Ml Lightgbm Training Server Agent
LightGBM training server agent. Manages LightGBM training server.

**Commands:**
- `python -m lightgbm-ing.server --port 8000 --workers 4`
- `curl -s http://localhost:8000/healthz`
- `curl -s http://localhost:8000/metrics | head -20`
- `supervisorctl restart lightgbm-ing`
- `systemctl status lightgbm-ing.service`

**Examples:**
- python train_server.py --model model.pkl --port 8080
- curl http://localhost:8080/train --data '{"data": "train.csv"}'
- python test_train_server.py --endpoint http://localhost:8080
- python config_train.py --model model.pkl --epochs 10
