---
applyTo: "**/*.r **/*.sh **/*.{yaml,yml}"
---

Implements standard deployment pipelines: rolling updates with health gates, versioned releases, and staged rollouts.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `kubectl rollout restart deployment/api -n prod`, `kubectl apply -f deploy/dev/api.yaml --record`
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

# API Deploy (Implementation)

Implements standard, repeatable deployment pipelines for APIs.

## When to Use
- Standardizing deploy steps
- Adding health-gated updates
- Rolling out environment-by-environment

## Real Commands

```bash
# Rolling update
kubectl rollout restart deployment/api -n prod
kubectl rollout status deployment/api -n prod --watch

# Check strategy
kubectl get deployment api -n prod -o yaml | grep -A5 strategy

# Staged rollout
kubectl apply -f deploy/dev/api.yaml --record
kubectl apply -f deploy/staging/api.yaml --record
kubectl rollout status deployment/api -n staging --timeout 120s
kubectl apply -f deploy/prod/api.yaml --record

# Rollback
kubectl rollout undo deployment/api -n prod
```

## Health Gates
- readinessProbe: /health endpoint
- livenessProbe: /healthz
- maxUnavailable: 25%

## Testing
Watch rollout status during a deploy and verify old pods drain before new ones serve.

## Best Practices
- Record every apply (`--record`)
- Promote only after staging gates pass

## Capabilities

### rolling-updates
Configure rolling updates with readiness and liveness gates

**Parameters:**
- `deployment` (string): Deployment name
- `namespace` (string): Namespace

**Commands:**
- `kubectl rollout restart deployment/api -n prod`
- `kubectl rollout status deployment/api -n prod --watch`
- `kubectl set resources deployment/api -n prod --limits=cpu=500m,memory=512Mi`
- `kubectl get deployment api -n prod -o yaml | grep -A5 strategy`
- `kubectl rollout undo deployment/api -n prod`

**Examples:**
- kubectl rollout restart deployment/api -n prod && kubectl rollout status deployment/api -n prod --watch
- kubectl get deployment api -n prod -o yaml | grep -A5 strategy
- kubectl rollout undo deployment/api -n prod

### staged-rollout
Roll out through dev, staging, then production with promotion checks

**Parameters:**
- `environment` (string): Target environment
- `manifest` (string): Manifest path

**Commands:**
- `kubectl apply -f deploy/dev/api.yaml --record`
- `kubectl apply -f deploy/staging/api.yaml --record`
- `kubectl apply -f deploy/prod/api.yaml --record`
- `kubectl rollout status deployment/api -n staging --timeout 120s`
- `kubectl describe deployment api -n staging | grep -E 'Replicas|Conditions'`

**Examples:**
- kubectl apply -f deploy/dev/api.yaml --record && kubectl apply -f deploy/staging/api.yaml --record
- kubectl rollout status deployment/api -n staging --timeout 120s
- kubectl describe deployment api -n staging | grep -E 'Replicas|Conditions'

## References
- [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Rollout Strategies](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#rolling-update-deployment)
