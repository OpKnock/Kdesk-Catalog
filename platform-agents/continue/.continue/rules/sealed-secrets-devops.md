---
name: "Sealed Secrets"
description: "Encrypts Kubernetes secrets at rest in git with Sealed Secrets and kubeseal: certificate management, encryption, and decryption workflows."
globs: ["**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
alwaysApply: false
---

# Sealed Secrets

Encrypts Kubernetes secrets at rest in git with Sealed Secrets and kubeseal: certificate management, encryption, and decryption workflows.

## Instructions

# Sealed Secrets for GitOps

Store Kubernetes Secrets encrypted in git and decrypt only inside the cluster.

## What This Skill Does

- Installs the sealed-secrets controller with Helm
- Fetches the cluster sealing certificate
- Encrypts plain secrets into SealedSecret CRs with kubeseal
- Applies SealedSecrets that the controller decrypts
- Manages sealing scopes and certificate rotation

## When to Use

- GitOps repos that cannot contain plaintext secrets
- Multi-cluster secrets with cluster-specific encryption
- Replacing SOPS with cluster-native decryption

## Real Commands

```bash
# Install controller
helm install sealed-secrets bitnami/sealed-secrets -n kube-system

# Fetch cert
kubeseal --fetch-cert > pub-cert.pem
kubeseal --controller-namespace kube-system --fetch-cert

# Seal (pipeline)
kubectl create secret generic db-pass   --from-literal=password=s3cr3t   --dry-run=client -o yaml > secret.yaml
kubeseal --format yaml < secret.yaml > sealed-secret.yaml

# Offline sealing with the saved cert
kubeseal --cert pub-cert.pem -o yaml < secret.yaml > sealed-secret.yaml

# Apply and verify
kubectl apply -f sealed-secret.yaml
kubectl get sealedsecrets
kubectl get secret db-pass
```

## Scopes

- `strict` — only sealed for the exact namespace/name
- `namespace-wide` — any name in the namespace
- `cluster-wide` — any namespace and name

## Best Practices

- Use strict scope for prod secrets; cluster-wide for shared templates
- Keep the public cert in the repo for CI sealing jobs
- Rotate keys yearly; the controller supports multiple active keys
- Never commit the controller's private key anywhere
- Validate decrypted secret in staging before applying to prod

## Capabilities

### sealing
Create SealedSecrets from plain secrets and apply them to clusters.

**Commands:**
- `kubectl create secret generic db-pass --from-literal=password=s3cr3t --dry-run=client -o yaml > secret.yaml`
- `kubeseal --format yaml demo-secret-yaml sealed-secret.yaml`
- `kubeseal --scope cluster-wide -o yaml < secret.yaml`
- `kubectl apply -f sealed-secret.yaml`
- `kubectl get sealedsecrets`

**Examples:**
- kubeseal --format yaml demo-secret-yaml sealed-secret.yaml
- kubeseal --scope cluster-wide -o yaml < secret.yaml
- kubectl apply -f sealed-secret.yaml

### certificate-management
Fetch and manage the sealing certificate for kubeseal.

**Commands:**
- `kubeseal --fetch-cert > pub-cert.pem`
- `kubeseal --controller-namespace kube-system --fetch-cert`
- `kubectl get secret -n kube-system -l sealedsecrets.bitnami.com/sealed-secrets-key -o yaml`
- `helm install sealed-secrets bitnami/sealed-secrets -n kube-system`
- `kubeseal --cert pub-cert.pem -o yaml < secret.yaml`

**Examples:**
- kubeseal --fetch-cert > pub-cert.pem
- helm install sealed-secrets bitnami/sealed-secrets -n kube-system
- kubeseal --cert pub-cert.pem -o yaml < secret.yaml