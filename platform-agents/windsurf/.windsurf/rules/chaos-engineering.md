---
trigger: glob
description: "Run Kubernetes chaos experiments with Litmus: install the operator, create chaos engines, and inspect experiment results."
globs: ["**/*.json", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

# Chaos Engineering

Run Kubernetes chaos experiments with Litmus: install the operator, create chaos engines, and inspect experiment results.

## Instructions

# Chaos Engineering (Litmus)

Run Kubernetes-native chaos experiments with Litmus.

## When to Use

- Testing pod deletion, CPU spikes, and network faults on k8s
- Building a repeatable chaos suite for a service
- Measuring blast radius with controlled targeting

## Install

```bash
helm repo add litmuschaos https://charts.litmuschaos.io
helm install chaos litmuschaos/litmus --namespace litmus --create-namespace
kubectl get pods -n litmus
```

## Pod Delete Experiment

```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: pod-delete-nginx
  namespace: myapp
spec:
  appinfo:
    appns: myapp
    applabel: app=nginx
    appkind: deployment
  chaosServiceAccount: litmus-sa
  experiments:
    - name: pod-delete
      spec:
        components:
          env:
            - name: TOTAL_CHAOS_DURATION
              value: "30"
            - name: CHAOS_INTERVAL
              value: "10"
```

```bash
kubectl apply -f pod-delete.yaml
kubectl get chaosengines -n myapp
kubectl get chaosexperiments -n myapp
kubectl describe chaosresult pod-delete-nginx -n myapp
```

## Connect Chaos Center

```bash
litmusctl connect agent --config=config.yaml --non-interactive
```

## Testing

```bash
# Confirm injection is done and experiment passed
kubectl get chaosresult pod-delete-nginx -n myapp -o jsonpath='{.status.experimentStatus.verdict}'
```

## Best Practices

- Always scope appinfo with a unique applabel
- Set TOTAL_CHAOS_DURATION and CHAOS_INTERVAL explicitly
- Run experiments against staging before prod
- Use chaos runners only where a service account exists
- Pair experiments with dashboards to correlate incidents
- Start with pod-delete, then add network and CPU faults
- Clean up engines after runs

## Capabilities

### litmus-install
Install Litmus Chaos operator and connect agents via helm and litmusctl

**Commands:**
- `helm repo add litmuschaos https://charts.litmuschaos.io`
- `helm install chaos litmuschaos/litmus --namespace litmus --create-namespace`
- `kubectl get pods -n litmus`
- `litmusctl version`

**Examples:**
- helm repo add litmuschaos https://charts.litmuschaos.io && helm install chaos litmuschaos/litmus --namespace litmus --create-namespace
- kubectl get pods -n litmus -l app.kubernetes.io/name=litmus
- litmusctl version

### chaos-experiments
Apply chaos experiments and engines, then inspect fault injection results

**Commands:**
- `kubectl apply -f pod-delete.yaml`
- `kubectl get chaosengines -n myapp`
- `kubectl get chaosexperiments -n myapp`
- `kubectl describe chaosresult pod-delete-nginx -n myapp`

**Examples:**
- kubectl apply -f pod-delete.yaml && kubectl get chaosengines -n myapp
- kubectl describe chaosresult pod-delete-nginx -n myapp
- kubectl logs -n litmus -l app.kubernetes.io/name=chaos-exporter
