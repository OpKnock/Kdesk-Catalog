---
name: "Gitops Principles"
description: "GitOps principles and workflows: declarative cluster state in git, pull-based sync, and safe rollback practices with kubectl and flux."
globs: ["**/*.go", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
alwaysApply: false
---

# Gitops Principles

GitOps principles and workflows: declarative cluster state in git, pull-based sync, and safe rollback practices with kubectl and flux.

## Instructions

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