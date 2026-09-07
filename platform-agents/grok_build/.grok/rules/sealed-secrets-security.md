Encrypts Kubernetes Secrets into SealedSecrets so they can be stored in Git and decrypted only by the in-cluster controller.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `kubeseal --format yaml demo-secret-yaml sealed-secret.yaml`, `helm repo add sealed-secrets https://bitnami-labs.github.io/`
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