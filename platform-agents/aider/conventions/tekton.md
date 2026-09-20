# Tekton

Create and run Kubernetes-native CI/CD pipelines with Tekton using the tkn CLI. Applies Task and Pipeline definitions, starts runs with streaming logs, and inspects pipelinerun statuses and step output — replacing external CI systems with cluster-based execution.

## Instructions

# Tekton

Hand-crafted skill for CI/CD pipelines with Tekton on Kubernetes.

## What this skill does

- Applies Task and Pipeline YAML into a cluster
- Starts pipelines and streams logs with the tkn CLI
- Inspects pipelineruns and their step statuses

## When to use

- Kubernetes-native CI where Pods do the work
- Replacing cloud CI for cluster-based builds
- Per-namespace pipelines with shared tasks

## Real commands

```bash
# Apply task definitions
kubectl apply -f tasks/build-image.yaml

# Inventory
tkn task list -n ci
tkn pipeline list -n ci

# Start a run and watch it
tkn pipeline start build-deploy --showlog -n ci

# Inspect runs
tkn pipelinerun list -n ci
kubectl get pipelineruns -n ci -w

# Stream logs of a finished run
tkn pipelinerun logs -f build-deploy-run-abc -n ci
```

## Pipeline example

```yaml
apiVersion: tekton.dev/v1
kind: Pipeline
metadata:
  name: build-deploy
spec:
  tasks:
    - name: build-image
      taskRef:
        name: build-image
    - name: deploy
      taskRef:
        name: deploy
      runAfter: [build-image]
```

## Testing

```bash
kubectl apply -f tasks/build-image.yaml
tkn task start build-image --showlog -n ci
tkn taskrun list -n ci
```

## Best practices

- Version tasks in a shared git repo and apply them in CI
- Use workspaces (PVCs) for caching between tasks
- Set timeouts on tasks so stuck runs do not hold namespaces

## Capabilities

### tekton-pipelines
Create and run Tekton pipelines with the tkn CLI

**Commands:**
- `kubectl apply -f tasks/build-image.yaml`
- `tkn task list -n ci`
- `tkn pipeline start build-deploy --showlog -n ci`
- `tkn pipelinerun list -n ci`
- `tkn pipelinerun logs -f build-deploy-run-abc -n ci`
- `kubectl get pipelineruns -n ci -w`

**Examples:**
- tkn pipeline start build-deploy --showlog -n ci
- tkn pipelinerun logs -f build-deploy-run-abc -n ci
- kubectl apply -f pipeline.yaml
