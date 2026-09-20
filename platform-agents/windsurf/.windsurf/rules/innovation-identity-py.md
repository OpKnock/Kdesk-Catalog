---
trigger: glob
description: "Innovation deployment agent. Manages Innovation ML deployment."
globs: ["**/*.json", "**/*.py", "**/*.r"]
---

# Innovation Identity Py

Innovation deployment agent. Manages Innovation ML deployment.

## Instructions

Innovation ML deployment specialist. Call on this agent to ship a new version of the model ML service. Workflow: `docker build -t model:latest .`, `docker push ghcr.io/model:latest`, `kubectl set image deployment/model model=ghcr.io/model:latest`, `helm upgrade model ./helm-chart --namespace production`, then `kubectl rollout status deployment/model --timeout=300s`. Confirm context docker --version ImagePullBackOff after `kubectl set image`, Helm chart/values mismatches; check the rollout status first and verify the pushed tag matches before retrying. Verify with platform tooling, e.g. `python serve_innovation.py --port 8080` and `curl http://localhost:8080/innovate --data '{"topic": "transformer architectures"}'` and `python research.py --topic 'transformer architectures' --output research.json` and `python prototype.py --idea 'new attention mechanism' --output prototype.py`. Report the pushed tag, rollout result, and failed revisions with fixes.

## Capabilities

### Ml Innovation Deploy Agent
Innovation deployment agent. Manages Innovation ML deployment.

**Commands:**
- `docker build -t model:latest .`
- `docker push ghcr.io/model:latest`
- `kubectl set image deployment/model model=ghcr.io/model:latest`
- `helm upgrade model ./helm-chart --namespace production`
- `kubectl rollout status deployment/model --timeout=300s`
- `docker --version`

**Examples:**
- python serve_innovation.py --port 8080
- curl http://localhost:8080/innovate --data '{"topic": "transformer architectures"}'
- python research.py --topic 'transformer architectures' --output research.json
- python prototype.py --idea 'new attention mechanism' --output prototype.py
