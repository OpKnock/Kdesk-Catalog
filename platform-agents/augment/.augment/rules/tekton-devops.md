---
type: agent_requested
description: "Builds CI/CD pipelines on Kubernetes with Tekton: Tasks, Pipelines, Triggers, and the tkn CLI for runs and logs."
---

# tekton-devops

Builds CI/CD pipelines on Kubernetes with Tekton: Tasks, Pipelines, Triggers, and the tkn CLI for runs and logs.

## Instructions

# Tekton Pipelines

Run Kubernetes-native CI/CD: Tasks and Pipelines as CRDs, driven by the tkn CLI.

## What This Skill Does

- Defines Tasks and Pipelines with steps, params, and workspaces
- Starts runs with parameter and workspace bindings
- Streams logs and describes run status
- Cancels stuck runs and lists history
- Reuses community Tasks from the Tekton catalog

## When to Use

- CI/CD inside Kubernetes without external services
- Cluster-adjacent build pipelines (in-cluster builds, privileged steps)
- GitOps-friendly pipeline definitions in git

## Real Commands

```bash
# Define and install
kubectl apply -f task-build.yaml
kubectl apply -f pipeline-ci.yaml
tkn task list
tkn pipeline list

# Start runs
tkn pipeline start ci -p revision=main   -w name=workspace,claimName=build-pvc
tkn pipeline start ci --use-param-defaults

# Observe
tkn pipelinerun list
tkn pipelinerun logs ci-run-123 -f
tkn pipelinerun describe ci-run-123
tkn pipelinerun cancel ci-run-123
kubectl get pipelineruns --sort-by=.metadata.creationTimestamp
```

## Pipeline Sketch

```yaml
apiVersion: tekton.dev/v1
kind: Pipeline
metadata: { name: ci }
spec:
  workspaces: [{ name: workspace }]
  tasks:
    - name: build
      taskRef: { name: build-image }
      workspaces: [{ name: source, workspace: workspace }]
```

## Best Practices

- Keep Tasks small and reusable; compose with Pipeline params
- Use workspaces (PVC/emptyDir) for shared state between tasks
- Add timeouts and retries on flaky steps
- Run the Tekton dashboard or use tkn for day-2 ops
- Version pipelines in git and apply with kubectl apply for auditability

## Capabilities

### tasks-and-pipelines
Create Tasks/Pipelines and start runs with parameters.

**Commands:**
- `kubectl apply -f task-build.yaml`
- `tkn task create -f task-build.yaml`
- `tkn task list`
- `kubectl apply -f pipeline-ci.yaml`
- `tkn pipeline start ci -p revision=main -w name=workspace,claimName=build-pvc`
- `tkn pipeline list`

**Examples:**
- tkn pipeline start ci -p revision=main
- kubectl apply -f pipeline-ci.yaml
- tkn task list

### runs-and-logs
Monitor, inspect, and cancel pipeline runs.

**Commands:**
- `tkn pipelinerun list`
- `tkn pipelinerun logs ci-run-123 -f`
- `tkn pipelinerun describe ci-run-123`
- `tkn pipelinerun cancel ci-run-123`
- `tkn taskrun logs taskrun-abc --follow`
- `kubectl get pipelineruns --sort-by=.metadata.creationTimestamp`

**Examples:**
- tkn pipelinerun logs ci-run-123 -f
- tkn pipelinerun describe ci-run-123
- tkn pipelinerun cancel ci-run-123