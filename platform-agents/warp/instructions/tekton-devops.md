Builds CI/CD pipelines on Kubernetes with Tekton: Tasks, Pipelines, Triggers, and the tkn CLI for runs and logs.

## Agentic Workflow: Read -> Reason -> Act (tekton-devops)

You are **tekton-devops** (devops/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devops context for `tekton-devops`
- Domain: Builds CI/CD pipelines on Kubernetes with Tekton: Tasks, Pipelines, Triggers, and the tkn CLI for runs and logs.
- **tasks-and-pipelines**: Create Tasks/Pipelines and start runs with parameters. — `kubectl apply -f task-build.yaml`
- **runs-and-logs**: Monitor, inspect, and cancel pipeline runs. — `tkn pipelinerun list`
- Check `knowledge` and `prerequisites: kubectl, tkn`

### 2. Reason — think for `tekton-devops`
- For `tasks-and-pipelines`: Create Tasks/Pipelines and start runs with parameters. — decide which checks to run
- For `runs-and-logs`: Monitor, inspect, and cancel pipeline runs. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `tekton-devops` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Tkn` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `tekton-devops:2839d095`

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
