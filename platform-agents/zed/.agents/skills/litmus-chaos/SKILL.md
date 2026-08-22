---
name: "litmus-chaos"
description: "Run chaos experiments on Kubernetes with LitmusChaos: install agents via litmusctl, apply chaos engines, and execute pod-delete experiments."
---

# Litmus Chaos

Run chaos experiments on Kubernetes with LitmusChaos: install agents via litmusctl, apply chaos engines, and execute pod-delete experiments.

## Instructions

# LitmusChaos

Run Kubernetes chaos experiments with the LitmusChaos platform.

## What this skill does

- Connects Kubernetes agents to the Litmus portal with litmusctl.
- Applies ChaosEngine manifests targeting workloads.
- Monitors experiment results (ChaosResult CRs).

## When to use

- Validating pod failure tolerance in staging.
- Testing deployment rollbacks under pod deletion.
- Building a chaos regression suite before releases.

## Real commands

```bash
# Connect an agent (cluster) to the portal
litmusctl connect agent \
  --endpoint=http://litmus-frontend:3001 \
  --username admin --password=litmus

# Verify agent state
litmusctl get agents

# Apply the experiment definitions
kubectl apply -f pod-delete-experiment.yaml -n litmus

# Apply the chaos engine (targets the workload)
litmusctl apply chaosengine -f chaosengine.yaml
kubectl apply -f chaosengine.yaml -n litmus

# Watch the run
kubectl get chaosengine -n litmus
kubectl get chaosresult -n litmus
kubectl logs -n litmus -l app=chaos-exporter --tail=50
```

## ChaosEngine example

```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: nginx-chaos
  namespace: litmus
spec:
  appinfo:
    appns: default
    applabel: app=nginx
    appkind: deployment
  chaosServiceAccount: litmus-admin
  experiments:
    - name: pod-delete
      spec:
        components:
          env:
            - name: TOTAL_CHAOS_DURATION
              value: "30"
```

## Testing

```bash
kubectl get chaosresult -n litmus -o jsonpath='{.items[0].status.experimentStatus.verdict}'
```

## Best practices

- Scope experiments to staging first; use namespaces to bound blast radius.
- Define steady-state checks (Probes) so failures surface automatically.
- Clean up ChaosEngines after runs to avoid repeating experiments.

## Capabilities

### litmusctl-connect
Connect agents and manage experiments with litmusctl.

**Commands:**
- `litmusctl version`
- `litmusctl connect agent --endpoint=http://litmus-frontend:3001 --username admin --password=litmus`
- `litmusctl get agents`
- `litmusctl get chaosengines`
- `litmusctl apply chaosengine -f chaosengine.yaml`

**Examples:**
- litmusctl connect agent --endpoint=http://litmus-frontend:3001 --username admin --password=litmus
- litmusctl get agents
- litmusctl apply chaosengine -f chaosengine.yaml

### chaos-runs
Apply chaos experiments (pod-delete, cpu-hog) and monitor runs.

**Commands:**
- `kubectl apply -f pod-delete-experiment.yaml -n litmus`
- `kubectl apply -f chaosengine.yaml -n litmus`
- `kubectl get chaosengine -n litmus`
- `kubectl get chaosresult -n litmus`
- `kubectl logs -n litmus -l app=chaos-exporter --tail=50`

**Examples:**
- kubectl apply -f pod-delete-experiment.yaml -n litmus
- kubectl get chaosresult -n litmus
- kubectl apply -f chaosengine.yaml -n litmus
