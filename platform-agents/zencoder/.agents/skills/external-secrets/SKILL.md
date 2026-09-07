---
name: "external-secrets"
description: "Sync secrets from external providers (AWS Secrets Manager, Vault, GCP) into Kubernetes with External Secrets Operator: define ExternalSecrets and verify injected values. Use when working with external secrets, api or when the user mentions external secrets, api."
license: "MIT"
compatibility: "Requires helm, kubectl. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(helm:*) Bash(kubectl:*)"
---

Sync secrets from external providers (AWS Secrets Manager, Vault, GCP) into Kubernetes with External Secrets Operator: define ExternalSecrets and verify injected values.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `helm repo add external-secrets https://charts.external-secre`
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

**Parameters:**
- `namespace` (string): Namespace for the ExternalSecret
- `secret-name` (string): Name of the Kubernetes Secret to sync into
- `provider` (string): aws, vault, gcp, azure provider for the SecretStore

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

## References
- [External Secrets Operator Docs](https://external-secrets.io/latest/introduction/overview/)
- [ESO AWS provider](https://external-secrets.io/latest/provider/aws-secrets-manager/)
