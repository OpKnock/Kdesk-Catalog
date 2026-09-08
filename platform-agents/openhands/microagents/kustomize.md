---
name: "kustomize"
description: "Manage Kubernetes manifests with Kustomize: overlays per environment, image/namespace overrides, and build-to-apply workflows. Use when working with kustomize build, kustomize edit, api or when the user mentions kustomize build, kustomize edit, api."
type: knowledge
triggers: ["kustomize", "kustomize-build", "kustomize-edit"]
---

Manage Kubernetes manifests with Kustomize: overlays per environment, image/namespace overrides, and build-to-apply workflows.

## Agentic Workflow: Read -> Reason -> Act (kustomize)

You are **Kustomize** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `kustomize`
- Domain: Manage Kubernetes manifests with Kustomize: overlays per environment, image/namespace overrides, and build-to-apply workflows.
- **kustomize-build**: Build and apply kustomized manifests. — `kustomize build .`
- **kustomize-edit**: Edit kustomization.yaml: images, namespaces, and common labels. — `kustomize create --resources=../base`
- Check `knowledge` and `prerequisites: kubectl, kustomize`

### 2. Reason — think for `kustomize`
- For `kustomize-build`: Build and apply kustomized manifests. — decide which checks to run
- For `kustomize-edit`: Edit kustomization.yaml: images, namespaces, and common labels. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `kustomize` tools
- Tools: `Glob`, `Grep`, `Read`, `Kustomize`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `kustomize:88dc1910`

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
