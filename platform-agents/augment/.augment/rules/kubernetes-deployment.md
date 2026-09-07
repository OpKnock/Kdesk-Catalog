---
type: agent_requested
description: "Deploy and operate workloads with kubectl: create deployments, scale replicas, update images, and manage rollouts. Use when working with deploy basic, rollout ops, api or when the user mentions deploy basic, rollout ops, api."
---

Deploy and operate workloads with kubectl: create deployments, scale replicas, update images, and manage rollouts.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `kubectl create deployment nginx --image=nginx:1.27 --replica`, `kubectl rollout status deployment/nginx`
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

# Kubernetes Deployments

Create and operate declarative workloads with kubectl.

## What this skill does

- Creates deployments from images with replica counts.
- Scales replicas and updates images.
- Manages rollouts and status checks.

## When to use

- Deploying stateless services.
- Day-2 operations: scaling, image bumps, restarts.
- Checking rollout health during releases.

## Real commands

```bash
# Create
kubectl create deployment nginx --image=nginx:1.27 --replicas=3

# Scale
kubectl scale deployment nginx --replicas=5

# Update image (triggers a rollout)
kubectl set image deployment/nginx nginx=nginx:1.28

# Expose as a service
kubectl expose deployment nginx --port=80 --type=ClusterIP

# Rollout status
kubectl rollout status deployment/nginx

# Restart (re-pull, new rollout)
kubectl rollout restart deployment/nginx

# Inspect
kubectl get deployments
kubectl get pods -l app=nginx -o wide
kubectl describe deployment nginx
```

## Deployment YAML example

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx:1.27
          ports:
            - containerPort: 80
```

## Testing

```bash
kubectl apply -f deployment.yaml
kubectl rollout status deployment/nginx
kubectl get pods --watch
```

## Best practices

- Always set resource requests/limits on containers.
- Use apply -f with versioned manifests, not ad-hoc create.
- Check rollout status before declaring a release done.

## Capabilities

### deploy-basic
Create, scale, and update deployments.

**Parameters:**
- `name` (string): Deployment name.
- `image` (string): Container image.
- `replicas` (integer): Desired replica count.

**Commands:**
- `kubectl create deployment nginx --image=nginx:1.27 --replicas=3`
- `kubectl scale deployment nginx --replicas=5`
- `kubectl set image deployment/nginx nginx=nginx:1.28`
- `kubectl expose deployment nginx --port=80 --type=ClusterIP`

**Examples:**
- kubectl create deployment nginx --image=nginx:1.27 --replicas=3
- kubectl scale deployment nginx --replicas=5
- kubectl set image deployment/nginx nginx=nginx:1.28

### rollout-ops
Monitor rollout progress and status.

**Parameters:**
- `name` (string): Deployment name.
- `label` (string): Pod selector label.

**Commands:**
- `kubectl rollout status deployment/nginx`
- `kubectl rollout restart deployment/nginx`
- `kubectl get deployments`
- `kubectl get pods -l app=nginx -o wide`
- `kubectl describe deployment nginx`

**Examples:**
- kubectl rollout status deployment/nginx
- kubectl rollout restart deployment/nginx
- kubectl get deployments

## References
- [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [kubectl cheat sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)