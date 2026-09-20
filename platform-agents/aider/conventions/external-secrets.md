# External Secrets

Sync secrets from external providers (AWS Secrets Manager, Vault, GCP) into Kubernetes with External Secrets Operator: define ExternalSecrets and verify injected values.

## Instructions

# External Secrets

## What this skill does

External Secrets Operator (ESO) syncs secrets from external APIs (AWS Secrets Manager, Vault, GCP) into Kubernetes Secrets declaratively. You define SecretStore (provider+auth) and ExternalSecret (what to fetch), and ESO reconciles the target Secret.

## When to use

- Replacing long-lived Secrets baked into cluster manifests
- Rotating provider-side secrets without touching the cluster
- Centralizing secret access with IAM/role-based auth

## Real commands

```bash
# Install ESO
helm repo add external-secrets https://charts.external-secrets.io
helm install external-secrets external-secrets/external-secrets -n external-secrets --create-namespace

# Apply store + external secret
kubectl apply -f secret-store.yaml
kubectl apply -f external-secret.yaml

# Verify
kubectl get externalsecrets -n app
kubectl get secret my-secret -n app -o jsonpath='{.data.DATABASE_URL}' | base64 -d
kubectl describe externalsecret db-credentials -n app
```

## Manifests example

```yaml
# secret-store.yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: aws-store
spec:
  provider:
    aws:
      service: SecretsManager
      region: us-east-1
      auth:
        jwt:
          serviceAccountRef:
            name: eso-sa
---
# external-secret.yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: db-credentials
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-store
  target:
    name: my-secret
  data:
    - secretKey: DATABASE_URL
      remoteRef:
        key: prod/db
        property: url
```

## Testing

```bash
# Force an immediate reconcile
kubectl annotate externalsecret db-credentials force-sync=$(date +%s)
```

## Best practices

- Use `secretStoreRef` per namespace; use ClusterSecretStore only for shared stores.
- Give the operator an IRSA/workload identity, never static keys in the cluster.
- Check `status.conditions` message when sync fails; it carries the provider error.
- Test provider rotation by changing the remote value and forcing a sync.

## Capabilities

### external-secrets
Deploy ESO, create SecretStores and ExternalSecrets, and verify secrets land in the cluster.

**Commands:**
- `helm repo add external-secrets https://charts.external-secrets.io && helm install external-secrets external-secrets/external-secrets -n external-secrets --create-namespace`
- `kubectl apply -f secret-store.yaml`
- `kubectl apply -f external-secret.yaml`
- `kubectl get externalsecrets -n app`
- `kubectl get secret my-secret -n app -o jsonpath='{.data.DATABASE_URL}' | base64 -d`
- `kubectl describe externalsecret db-credentials -n app`

**Examples:**
- kubectl apply -f secret-store.yaml && kubectl apply -f external-secret.yaml
- kubectl get externalsecret db-credentials -n app -o jsonpath='{.status.conditions[0].message}'
- kubectl get secret my-secret -n app -o jsonpath='{.data.DATABASE_URL}' | base64 -d
