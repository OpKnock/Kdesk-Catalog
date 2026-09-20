---
name: "kustomize-devops"
description: "Composes Kubernetes manifests with kustomize: overlays, bases, patches, generators, and kubectl apply -k workflows."
globs: ["**/*.json", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
alwaysApply: false
---

# kustomize-devops

Composes Kubernetes manifests with kustomize: overlays, bases, patches, generators, and kubectl apply -k workflows.

## Instructions

# Kustomize Configuration

Manage environment-specific Kubernetes configs with bases and overlays.

## What This Skill Does

- Builds final manifests from base + overlay layers
- Patches any field with strategic merge or JSON patches
- Generates ConfigMaps and Secrets from files/literals
- Sets images, labels, namespaces per overlay
- Applies straight to the cluster with kubectl apply -k

## When to Use

- Running the same app in dev/staging/prod with small diffs
- Replacing sed-heavy templating in deployment scripts
- Vendoring upstream manifests with local tweaks

## Real Commands

```bash
# Build
kustomize build ./overlays/prod
kustomize build . | kubectl apply -f -
kubectl apply -k ./overlays/prod
kustomize cfg tree .          # view resource tree

# Edit kustomization.yaml
kustomize create --resources=base
kustomize edit add resource deployment.yaml
kustomize edit add patch --kind Deployment --name web --path patch.yaml
kustomize edit set image myapp:1.2.0
kustomize edit add label app.kubernetes.io/part-of:web
kustomize edit add configmap app-config --from-literal=DEBUG=false
```

## Layout

```
base/
  deployment.yaml
  service.yaml
  kustomization.yaml
overlays/
  dev/    # kustomization.yaml -> base + patches
  prod/   # kustomization.yaml -> base + patches
```

## Best Practices

- Keep base pristine; all environment diffs live in overlays
- Use `edit set image` for immutable image promotion (gitops-friendly)
- Generate secrets via sealed-secrets/kustomize secretGenerator with encryption
- Validate built output in CI: `kustomize build | kubectl apply --dry-run=client -f -`
- Name overlays after environment; keep field paths stable

## Capabilities

### build-and-apply
Build overlays into final manifests and apply them directly.

**Commands:**
- `kustomize build ./overlays/prod`
- `kustomize build . | kubectl apply -f -`
- `kubectl apply -k ./overlays/prod`
- `kustomize build ./overlays/dev > /tmp/dev.yaml`
- `kustomize cfg tree .`

**Examples:**
- kustomize build ./overlays/prod
- kubectl apply -k ./overlays/prod
- kustomize build . | kubectl apply -f -

### edit-and-patch
Modify kustomization.yaml: add resources, patches, and set images.

**Commands:**
- `kustomize create --resources=base`
- `kustomize edit add resource deployment.yaml`
- `kustomize edit add patch --kind Deployment --name web --path patch.yaml`
- `kustomize edit set image myapp:1.2.0`
- `kustomize edit add label app.kubernetes.io/part-of:web`
- `kustomize edit add configmap app-config --from-literal=DEBUG=false`

**Examples:**
- kustomize edit set image myapp:1.2.0
- kustomize edit add patch --kind Deployment --name web --path patch.yaml
- kustomize edit add configmap app-config --from-literal=DEBUG=false