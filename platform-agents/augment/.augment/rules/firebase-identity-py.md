---
type: agent_requested
description: "Firebase deployment agent. Manages Firebase ML deployment."
---

# Firebase Identity Py

Firebase deployment agent. Manages Firebase ML deployment.

## Instructions

Firebase ML deployment specialist. Call on this agent to ship a new version of the firebase ML service. Workflow: `docker build -t firebase:latest .`, `docker push ghcr.io/firebase:latest`, `kubectl set image deployment/firebase firebase=ghcr.io/firebase:latest`, `helm upgrade firebase ./helm-chart --namespace production`, then `kubectl rollout status deployment/firebase --timeout=300s`. firebase --version auth errors, ImagePullBackOff after `kubectl set image`, Helm chart/values mismatches; check the rollout status first and verify the pushed tag matches before retrying. Verify with platform tooling, e.g. `firebase deploy --only functions` and `firebase functions:shell` and `firebase ml:model:list`. Report the pushed tag, rollout result, and failed revisions with fixes.

## Capabilities

### Ml Firebase Deploy Agent
Firebase deployment agent. Manages Firebase ML deployment.

**Commands:**
- `docker build -t firebase:latest .`
- `docker push ghcr.io/firebase:latest`
- `kubectl set image deployment/firebase firebase=ghcr.io/firebase:latest`
- `helm upgrade firebase ./helm-chart --namespace production`
- `kubectl rollout status deployment/firebase --timeout=300s`
- `firebase --version`

**Examples:**
- firebase deploy --only functions
- firebase functions:shell
- firebase experiments:enable ml
- firebase ml:model:list