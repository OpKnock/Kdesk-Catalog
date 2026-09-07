---
type: agent_requested
description: "Manage Kubernetes manifests with Kustomize: overlays per environment, image/namespace overrides, and build-to-apply workflows. Use when working with kustomize build, kustomize edit, api or when the user mentions kustomize build, kustomize edit, api."
---

Manage Kubernetes manifests with Kustomize: overlays per environment, image/namespace overrides, and build-to-apply workflows.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `kustomize build .`, `kustomize create --resources=../base`
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

# Kustomize

Manage Kubernetes manifests with overlays and patches, no templating needed.

## What this skill does

- Builds final manifests from base + overlays.
- Overrides images, namespaces, labels, and names.
- Applies via kubectl -k for GitOps-style flows.

## When to use

- Environment-specific tweaks (dev/staging/prod) of one base.
- Promoting a manifest set across clusters.
- Adding site-specific patches without forking manifests.

## Real commands

```bash
# Build merged output
kustomize build .

# Build a specific overlay
kustomize build overlays/prod

# Apply directly
kubectl apply -k .

# Pipe build into apply (audit trail)
kustomize build overlays/prod | kubectl apply -f -

# Create a new overlay from base
kustomize create --resources=../base --namespace=dev

# Edit kustomization.yaml
kustomize edit set image myapp=myapp:v2.0
kustomize edit set namespace production
kustomize edit add label app:myapp --force
kustomize edit set nameprefix prod-
```

## Directory layout

```text
base/
  deployment.yaml
  service.yaml
  kustomization.yaml
overlays/
  dev/
    kustomization.yaml
  prod/
    kustomization.yaml
    prod-patch.yaml
```

## kustomization.yaml example

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - ../../base
namespace: production
images:
  - name: myapp
    newTag: v2.0
patches:
  - path: prod-patch.yaml
```

## Testing

```bash
kustomize build overlays/prod | kubectl apply --dry-run=client -f -
```

## Best practices

- Keep the base pristine; put all environment changes in overlays.
- Use configMapGenerator for config auto-naming (rollout on change).
- Commit the built output only if auditors need it; otherwise build in CI.

## Capabilities

### kustomize-build
Build and apply kustomized manifests.

**Parameters:**
- `dir` (string): Kustomization directory.
- `restrictor` (string): LoadRestrictionsNone allows files outside the root.

**Commands:**
- `kustomize build .`
- `kubectl apply -k .`
- `kustomize build --load-restrictor LoadRestrictionsNone overlays/prod`
- `kustomize build . | kubectl apply -f -`

**Examples:**
- kustomize build .
- kubectl apply -k .
- kustomize build overlays/prod | kubectl apply -f -

### kustomize-edit
Edit kustomization.yaml: images, namespaces, and common labels.

**Parameters:**
- `image` (string): image=image:tag pair.
- `namespace` (string): Namespace to set for all resources.
- `nameprefix` (string): Prefix added to resource names.

**Commands:**
- `kustomize create --resources=../base`
- `kustomize edit set image myapp=myapp:v2.0`
- `kustomize edit set namespace production`
- `kustomize edit add label app:myapp --force`
- `kustomize edit set nameprefix prod-`

**Examples:**
- kustomize create --resources=../base
- kustomize edit set image myapp=myapp:v2.0
- kustomize edit set namespace production

## References
- [Kustomize](https://kubectl.docs.kubernetes.io/)
- [Kustomize CLI Reference](https://kubectl.docs.kubernetes.io/references/kustomize/)