---
name: "tekton-devops"
description: "Builds CI/CD pipelines on Kubernetes with Tekton: Tasks, Pipelines, Triggers, and the tkn CLI for runs and logs. Use when working with tasks and pipelines, runs and logs, devops or when the user mentions tasks and pipelines, runs and logs, devops."
license: "MIT"
compatibility: "Requires kubectl, tkn. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "devops"}
allowed-tools: "Glob Grep Read Bash(kubectl:*) Bash(tkn:*)"
---

Builds CI/CD pipelines on Kubernetes with Tekton: Tasks, Pipelines, Triggers, and the tkn CLI for runs and logs.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `kubectl apply -f task-build.yaml`, `tkn pipelinerun list`
- Check `knowledge` references and prerequisites before proceeding

### 2. Reason
Analyze and plan:
- Compare current state vs desired state (drift, checksums, policy)
- Evaluate trust, compatibility, and risk: use `kdesk trust` and `kdesk doctor` patterns
- Decide: which capabilities/tools are needed, which can be skipped

### 3. Act
Execute with guards:
- Run only `allowed-tools` (see frontmatter); use `safe_path` for writes
- Prefer `Bash` with explicit binaries (`curl`, `kubectl`, `kdesk`) over generic shell
- Record evidence: file paths, checksums, and tool outputs for verification

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

**Parameters:**
- `pipeline` (string): Pipeline name
- `params` (object): Parameters passed with -p
- `workspace` (string): Workspace binding

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

**Parameters:**
- `run` (string): PipelineRun name
- `follow` (boolean): Stream logs

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

## References
- [Tekton Documentation](https://tekton.dev/docs/)
- [tkn CLI](https://tekton.dev/docs/cli/)
- [Tekton Catalog](https://github.com/tektoncd/catalog)
