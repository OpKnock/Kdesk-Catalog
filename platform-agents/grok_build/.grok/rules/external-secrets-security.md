Synchronizes secrets from external providers (AWS, Vault, GCP, Azure) into Kubernetes with External Secrets Operator and secret stores.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `helm repo add external-secrets https://charts.external-secre`, `kubectl apply -f externalsecret.yaml`
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

Synchronize Kubernetes Secrets from external secret management systems.

## What This Skill Does

- Installs External Secrets Operator via Helm
- Configures SecretStore/ClusterSecretStore backends (AWS, Vault, GCP, Azure, 1Password)
- Defines ExternalSecret resources that pull named keys into Kubernetes Secrets
- Refreshes secrets on a schedule and reports sync conditions

## When to Use

- Kubernetes workloads need secrets from an external provider
- Rotating secrets centrally instead of editing YAML by hand
- Multi-cluster secret management with a single source of truth

## Real Commands

```bash
# Install
helm repo add external-secrets https://charts.external-secrets.io
helm install external-secrets external-secrets/external-secrets -n external-secrets --create-namespace

# Inspect stores
kubectl get secretstores -A
kubectl get clustersecretstores
kubectl describe secretstore aws-secretsmanager

# Sync and verify
kubectl apply -f externalsecret.yaml
kubectl get externalsecrets -A
kubectl describe externalsecret db-credentials
kubectl get secret db-credentials -o jsonpath='{.data.username}' | base64 -d
```

## Sample ExternalSecret

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: db-credentials
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secretsmanager
    kind: ClusterSecretStore
  target:
    name: db-credentials
  data:
    - secretKey: username
      remoteRef:
        key: prod/db
        property: username
```

## Best Practices

- Use ClusterSecretStore for shared backends, SecretStore for namespaced control
- Grant the operator minimal IAM/Vault permissions per store
- Set refreshInterval to balance drift detection and API cost
- Check the Secret.Status.Conditions for sync errors before releasing
- Never mix plain data in the same target Secret as synced keys

## Capabilities

### secretstore-management
Deploy and inspect SecretStores and ClusterSecretStores.

**Parameters:**
- `name` (string): SecretStore name
- `provider` (string): Backend provider: aws, vault, gcp, azure, onepassword

**Commands:**
- `helm repo add external-secrets https://charts.external-secrets.io`
- `helm install external-secrets external-secrets/external-secrets -n external-secrets --create-namespace`
- `kubectl get secretstores -A`
- `kubectl get clustersecretstores`
- `kubectl describe secretstore aws-secretsmanager`

**Examples:**
- helm install external-secrets external-secrets/external-secrets -n external-secrets
- kubectl get clustersecretstores
- kubectl describe secretstore vault-store

### externalsecret-sync
Create ExternalSecrets, sync them, and read generated Kubernetes Secrets.

**Parameters:**
- `name` (string): ExternalSecret name
- `namespace` (string): Namespace where the secret should sync

**Commands:**
- `kubectl apply -f externalsecret.yaml`
- `kubectl get externalsecrets -A`
- `kubectl describe externalsecret db-credentials`
- `kubectl get secret db-credentials -o jsonpath='{.data.username}' | base64 -d`
- `kubectl get pushsecrets`

**Examples:**
- kubectl apply -f externalsecret.yaml
- kubectl get externalsecrets -A
- kubectl describe externalsecret db-credentials

## References
- [External Secrets Documentation](https://external-secrets.io/)
- [Provider Reference](https://external-secrets.io/latest/provider/)