---
name: "sealed-secrets-security"
description: "Encrypts Kubernetes Secrets into SealedSecrets so they can be stored in Git and decrypted only by the in-cluster controller. Use when working with kubeseal sealing, controller management, security or when the user mentions kubeseal sealing, controller management, security."
---

Encrypts Kubernetes Secrets into SealedSecrets so they can be stored in Git and decrypted only by the in-cluster controller.

## Agentic Workflow: Read -> Reason -> Act (sealed-secrets-security)

You are **sealed-secrets-security** (security/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — security context for `sealed-secrets-security`
- Domain: Encrypts Kubernetes Secrets into SealedSecrets so they can be stored in Git and decrypted only by the in-cluster controller.
- **kubeseal-sealing**: Seal secrets with kubeseal and manage scopes. — `kubeseal --format yaml demo-secret-yaml sealed-secret.yaml`
- **controller-management**: Install the controller and inspect sealed/decrypted secrets. — `helm repo add sealed-secrets https://bitnami-labs.github.io/sealed-secrets`
- Check `knowledge` and `prerequisites: helm, kubectl, kubeseal`

### 2. Reason — think for `sealed-secrets-security`
- For `kubeseal-sealing`: Seal secrets with kubeseal and manage scopes. — decide which checks to run
- For `controller-management`: Install the controller and inspect sealed/decrypted secrets. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `sealed-secrets-security` tools
- Tools: `Glob`, `Grep`, `Read`, `Kubeseal`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `sealed-secrets-security:e60116a2`

# Sealed Secrets

GitOps-friendly secret management: encrypt once, store anywhere.

## What This Skill Does

- Seals Kubernetes Secrets with a cluster controller public cert
- Supports strict, namespace-wide, and cluster-wide scopes
- Lets you commit sealed manifests to Git safely
- Re-encrypts sealed secrets when the controller key rotates

## When to Use

- Secrets belong in GitOps repos (Flux/ArgoCD)
- Unsealing by the controller should be the only decryption path
- Team review of secret changes via PRs

## Real Commands

```bash
# Install the controller
helm repo add sealed-secrets https://bitnami-labs.github.io/sealed-secrets
helm install sealed-secrets sealed-secrets/sealed-secrets -n kube-system

# Seal
kubeseal --format yaml < secret.yaml > sealed-secret.yaml
kubeseal --scope cluster-wide -f secret.yaml
kubeseal --scope strict -f secret.yaml

# Re-encrypt after key rotation
kubeseal --re-encrypt < sealed-secret.yaml

# Verify
kubectl get sealedsecrets -A
kubectl get secrets -l sealed-secrets.bitnami.com/namespace=default
```

## Best Practices

- Use namespace-wide or strict scope so a sealed secret can't leak across namespaces
- Only store the public cert in the repo/CI; private key lives in the cluster
- Re-encrypt all sealed secrets when rotating controller keys
- Review sealed manifests in PRs; the controller decrypts on apply
- Never store plaintext Secret manifests in the same repo

## Capabilities

### kubeseal-sealing
Seal secrets with kubeseal and manage scopes.

**Parameters:**
- `scope` (string): Sealing scope: strict, namespace-wide, cluster-wide
- `format` (string): Output format: yaml or json

**Commands:**
- `kubeseal --format yaml demo-secret-yaml sealed-secret.yaml`
- `kubeseal --scope cluster-wide -f secret.yaml`
- `kubeseal --scope strict -f secret.yaml`
- `kubeseal --format json -f secret.yaml -o sealed.json`
- `kubeseal --re-encrypt < sealed-secret.yaml`

**Examples:**
- kubeseal --format yaml demo-secret-yaml sealed-secret.yaml
- kubeseal --scope cluster-wide -f secret.yaml
- kubeseal --re-encrypt demo-sealed-yaml re-sealed.yaml

### controller-management
Install the controller and inspect sealed/decrypted secrets.

**Parameters:**
- `namespace` (string): Namespace filter for sealed secrets
- `certFile` (string): Where kubeseal --fetch-cert writes the controller public cert.

**Commands:**
- `helm repo add sealed-secrets https://bitnami-labs.github.io/sealed-secrets`
- `helm install sealed-secrets sealed-secrets/sealed-secrets -n kube-system`
- `kubectl get sealedsecrets -A`
- `kubectl get secrets -l sealed-secrets.bitnami.com/namespace=default`
- `kubeseal --fetch-cert > pub-cert.pem`

**Examples:**
- helm install sealed-secrets sealed-secrets/sealed-secrets -n kube-system
- kubectl get sealedsecrets -A
- kubeseal --fetch-cert > pub-cert.pem

## References
- [Sealed Secrets GitHub](https://github.com/bitnami-labs/sealed-secrets)
- [Sealed Secrets Helm Chart](https://artifacthub.io/packages/helm/sealed-secrets/sealed-secrets)
