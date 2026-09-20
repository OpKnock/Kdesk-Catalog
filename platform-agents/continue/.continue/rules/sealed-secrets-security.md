---
name: "sealed-secrets-security"
description: "Encrypts Kubernetes Secrets into SealedSecrets so they can be stored in Git and decrypted only by the in-cluster controller."
globs: ["**/*.go", "**/*.json", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
alwaysApply: false
---

# sealed-secrets-security

Encrypts Kubernetes Secrets into SealedSecrets so they can be stored in Git and decrypted only by the in-cluster controller.

## Instructions

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