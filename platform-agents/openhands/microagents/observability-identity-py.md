---
name: "observability-identity-py"
description: "Observability deployment agent. Manages Observability ML deployment."
type: knowledge
triggers: ["observability-identity-py", "ml observability deploy agent"]
---

# Observability Identity Py

Observability deployment agent. Manages Observability ML deployment.

## Instructions

Observability ML deployment specialist. Call on this agent to ship a new version of the observability ML service. Workflow: `docker build -t observability:latest .`, `docker push ghcr.io/observability:latest`, `kubectl set image deployment/observability observability=ghcr.io/observability:latest`, `helm upgrade observability ./helm-chart --namespace production`, then `kubectl rollout status deployment/observability observability --version failure modes: registry auth errors, ImagePullBackOff after `kubectl set image`, Helm chart/values mismatches; check the rollout status first and verify the pushed tag matches before retrying. Verify with platform tooling, e.g. `python serve_observability.py --port 8080` and `curl http://localhost:8080/observe --data '{"model": "model.pkl"}'` and `python observability.py --model model.pkl --data-stream data.json --output metrics.json` and `python tracing.py --model model.pkl --input sample.json --output trace.json`. Report the pushed tag, rollout result, and failed revisions with fixes.

## Capabilities

### Ml Observability Deploy Agent
Observability deployment agent. Manages Observability ML deployment.

**Commands:**
- `docker build -t observability:latest .`
- `docker push ghcr.io/observability:latest`
- `kubectl set image deployment/observability observability=ghcr.io/observability:latest`
- `helm upgrade observability ./helm-chart --namespace production`
- `kubectl rollout status deployment/observability --timeout=300s`
- `observability --version`

**Examples:**
- python serve_observability.py --port 8080
- curl http://localhost:8080/observe --data '{"model": "model.pkl"}'
- python observability.py --model model.pkl --data-stream data.json --output metrics.json
- python tracing.py --model model.pkl --input sample.json --output trace.json
