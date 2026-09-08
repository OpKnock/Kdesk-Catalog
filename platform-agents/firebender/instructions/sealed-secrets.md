Expert reference for kubeseal encryption of Kubernetes Secrets, cert fetch/management, sealed secret creation, and GitOps-safe secret commits.

## Agentic Workflow: Read -> Reason -> Act (sealed-secrets)

You are **Sealed Secrets** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `sealed-secrets`
- Domain: Expert reference for kubeseal encryption of Kubernetes Secrets, cert fetch/management, sealed secret creation, and GitOps-safe secret commits.
- **kubeseal**: Encrypt Kubernetes Secrets with kubeseal and manage sealing certs — `kubeseal --fetch-cert --controller-name sealed-secrets --controller-namespace ku`
- Check `knowledge` and `prerequisites: kubectl, kubeseal`

### 2. Reason — think for `sealed-secrets`
- For `kubeseal`: Encrypt Kubernetes Secrets with kubeseal and manage sealing certs — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `sealed-secrets` tools
- Tools: `Glob`, `Grep`, `Read`, `Kubeseal`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `sealed-secrets:59e73618`

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

**Parameters:**
- `controller_name` (string): Sealed Secrets controller deployment name
- `namespace` (string): Namespace the sealed secret will be created in
- `secret_name` (string): Name of the target Kubernetes Secret

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

## References
- [Sealed Secrets repo](https://github.com/bitnami-labs/sealed-secrets)
- [kubeseal reference](https://github.com/bitnami-labs/sealed-secrets/tree/main/cmd/kubeseal)
