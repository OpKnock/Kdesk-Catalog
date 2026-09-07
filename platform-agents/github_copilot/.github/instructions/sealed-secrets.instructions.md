---
applyTo: "**/*.json **/*.r **/*.sh **/*.{yaml,yml}"
---

Expert reference for kubeseal encryption of Kubernetes Secrets, cert fetch/management, sealed secret creation, and GitOps-safe secret commits.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `kubeseal --fetch-cert --controller-name sealed-secrets --con`
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
