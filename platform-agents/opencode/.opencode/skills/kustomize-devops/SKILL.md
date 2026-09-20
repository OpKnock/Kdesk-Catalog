---
name: "kustomize-devops"
description: "Composes Kubernetes manifests with kustomize: overlays, bases, patches, generators, and kubectl apply -k workflows. Use when working with build and apply, edit and patch, devops or when the user mentions build and apply, edit and patch, devops."
---

Composes Kubernetes manifests with kustomize: overlays, bases, patches, generators, and kubectl apply -k workflows.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `kustomize build ./overlays/prod`, `kustomize create --resources=base`
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

**Parameters:**
- `path` (string): Overlay or base directory
- `output-file` (string): Write built manifest to file

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

**Parameters:**
- `image` (string): Image tag to set
- `kind` (string): Resource kind for patches

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

## References
- [Kustomize Documentation](https://kubectl.docs.kubernetes.io/guides/introduction/kustomize/)
- [Kustomize GitHub](https://github.com/kubernetes-sigs/kustomize)
