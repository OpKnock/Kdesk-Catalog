# Sealed Secrets

Expert reference for kubeseal encryption of Kubernetes Secrets, cert fetch/management, sealed secret creation, and GitOps-safe secret commits.

## Instructions

# Sealed Secrets

Expert skill for GitOps-safe secrets with Bitnami Sealed Secrets.

## What this skill does

- Encrypts Kubernetes Secrets into SealedSecret manifests with kubeseal
- Fetches the controller's public cert for offline sealing
- Applies sealed manifests that the controller unseals at runtime

## When to use

- Storing secrets in a git repository safely
- Cluster bootstrap where Vault is not available
- Giving developers access to secret creation without the cluster key

## Real commands

```bash
# Fetch the controller public cert once
kubeseal --fetch-cert --controller-name sealed-secrets --controller-namespace kube-system > pub-cert.pem

# Create and seal a secret
kubectl create secret generic db --from-literal=password=hunter2 --dry-run=client -o yaml | kubeseal --cert pub-cert.pem --format yaml > sealed-db.yaml

# Apply it; the controller decrypts into a regular Secret
kubectl apply -f sealed-db.yaml

# Inspect results
kubectl get sealedsecrets -o yaml
kubectl get secret db -o yaml
```

## SealedSecret example

```yaml
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: db
  namespace: default
spec:
  encryptedData:
    password: AgBy3i4OJSWK+PiTySYZ...
```

## Testing

```bash
kubectl apply -f sealed-db.yaml
kubectl get secret db -o jsonpath='{.data.password}' | base64 -d
```

## Best practices

- Seal with a scope that includes the target namespace (default)
- Back up the controller's private key: it is irreplaceable
- Commit only .yaml SealedSecrets, never plain Secrets

## Capabilities

### kubeseal
Encrypt Kubernetes Secrets with kubeseal and manage sealing certs

**Commands:**
- `kubeseal --fetch-cert --controller-name sealed-secrets --controller-namespace kube-system > pub-cert.pem`
- `kubectl create secret generic db --from-literal=password=hunter2 --dry-run=client -o yaml | kubeseal --cert pub-cert.pem --format yaml > sealed-db.yaml`
- `kubectl apply -f sealed-db.yaml`
- `kubectl get sealedsecrets -o yaml`
- `kubectl get secret db -o yaml`

**Examples:**
- kubectl create secret generic api --from-literal=API_KEY=xxx --dry-run=client -o yaml | kubeseal --format yaml > sealed-api.yaml
- kubeseal --fetch-cert --controller-name sealed-secrets --controller-namespace kube-system > pub-cert.pem
- kubectl apply -f sealed-db.yaml