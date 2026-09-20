---
applyTo: "**/*.go **/*.r **/*.sh **/*.{yaml,yml}"
---

GitOps principles and workflows: declarative cluster state in git, pull-based sync, and safe rollback practices with kubectl and flux.

## Agentic Workflow: Read -> Reason -> Act (gitops-principles)

You are **Gitops Principles** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `gitops-principles`
- Domain: GitOps principles and workflows: declarative cluster state in git, pull-based sync, and safe rollback practices with kubectl and flux.
- **gitops-workflow**: Apply GitOps practices: declarative manifests, sync reconciliation, and rollbacks. — `kubectl apply --dry-run=client -f manifests/ -o yaml > /dev/null && echo 'valid'`
- Check `knowledge` and `prerequisites: flux, kubectl`

### 2. Reason — think for `gitops-principles`
- For `gitops-workflow`: Apply GitOps practices: declarative manifests, sync reconciliation, and rollbacks. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `gitops-principles` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Flux` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `gitops-principles:5b3b76fa`

# GitOps Principles

## What this skill does

GitOps treats git as the single source of truth for infrastructure: desired state is declarative in repos, agents (Flux/Argo) pull and apply it, and rollback is a git revert.

## When to use

- Moving from click-ops to pull-based delivery
- Making every change reviewable and revertible
- Recovering a cluster by re-syncing from git

## Real commands

```bash
# Validate before applying
kubectl apply --dry-run=client -f manifests/ -o yaml > /dev/null && echo 'valid'

# Diff what would change
kubectl diff -f manifests/

# Apply (when not using a GitOps agent)
kubectl apply -f manifests/

# Force the agent to sync
flux reconcile kustomization apps --with-source

# Verify and roll back
kubectl rollout status deployment/orders -n app --timeout=120s
kubectl rollout undo deployment/orders -n app
```

## Core principles

1. Declarative: desired state expressed as manifests.
2. Versioned: changes go through git with review.
3. Pulled: agents fetch and apply; nobody applies ad hoc.
4. Continuous: the cluster always converges to git.

## Workflow example

```bash
git checkout -b fix/rollback-orders
git revert <breaking-commit>
kubectl diff -f manifests/ | head -40
# review the diff, then merge; the agent applies the revert
```

## Best practices

- Review every change via MR/PR before merge.
- Prefer agents (Flux/Argo) over human kubectl apply.
- Keep secrets out of git (Sealed Secrets, external-secrets).
- Add drift detection alerts for out-of-sync resources.
- Practice disaster recovery: re-sync a blank cluster from git.

## Capabilities

### gitops-workflow
Apply GitOps practices: declarative manifests, sync reconciliation, and rollbacks.

**Parameters:**
- `manifest-dir` (string): Directory with declarative manifests
- `deployment` (string): Deployment to verify or roll back
- `namespace` (string): Target namespace

**Commands:**
- `kubectl apply --dry-run=client -f manifests/ -o yaml > /dev/null && echo 'valid'`
- `kubectl diff -f manifests/`
- `kubectl apply -f manifests/`
- `flux reconcile kustomization apps --with-source`
- `kubectl rollout status deployment/orders -n app --timeout=120s`
- `kubectl rollout undo deployment/orders -n app`

**Examples:**
- kubectl diff -f manifests/ && kubectl apply -f manifests/
- kubectl rollout undo deployment/orders -n app
- flux reconcile kustomization apps --with-source

## References
- [GitOps Principles (CNCF)](https://opengitops.dev/)
- [Weaveworks GitOps guide](https://www.weave.works/technologies/gitops/)
