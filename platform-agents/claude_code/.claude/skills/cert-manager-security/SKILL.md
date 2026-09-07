---
name: "cert-manager-security"
description: "Issues, renews, and troubleshoots TLS certificates in Kubernetes with cert-manager, ACME issuers, and the cmctl CLI. Use when working with cmctl management, acme issuer setup, security or when the user mentions cmctl management, acme issuer setup, security."
license: "MIT"
compatibility: "Requires cmctl, kubectl. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "security"}
allowed-tools: "Glob Grep Read Bash(cmctl:*) Bash(kubectl:*)"
---

Issues, renews, and troubleshoots TLS certificates in Kubernetes with cert-manager, ACME issuers, and the cmctl CLI.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `kubectl apply -f https://github.com/cert-manager/cert-manage`, `kubectl get clusterissuers`
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

# cert-manager

Automatic TLS certificate issuance and renewal in Kubernetes using cert-manager.

## What This Skill Does

- Installs cert-manager and verifies the API is available
- Creates ClusterIssuers for ACME (Let's Encrypt), CA, and self-signed backends
- Issues Certificate resources and tracks their lifecycle
- Forces renewals and debugs ACME order/challenge failures

## When to Use

- A cluster needs automatic HTTPS for ingresses
- Certificates fail to issue or renew
- An issuer needs switching (staging to production Let's Encrypt)

## Real Commands

```bash
# Install
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.15.0/cert-manager.yaml
cmctl check api

# Issuer and certificate status
kubectl get clusterissuers
kubectl get certificates -A
kubectl describe certificate example-tls
cmctl status certificate example-tls

# Debug ACME
kubectl get orders.acme.cert-manager.io
kubectl get challenges.acme.cert-manager.io
kubectl get certificaterequests -A

# Operations
cmctl renew example-tls
cmctl renew --all
```

## Sample Certificate

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: example-tls
  namespace: istio-system
spec:
  secretName: example-tls
  dnsNames:
    - example.com
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
```

## Best Practices

- Use ClusterIssuer for shared issuers, Issuer for namespace-scoped control
- Start with the staging ACME server to avoid rate limits
- Enable the HTTP-01 solver via an ingress class annotation or DNS-01 for wildcards
- Monitor certificate expiry with cert-manager's built-in metrics
- Pin the cert-manager release and upgrade via helm to match CRD versions

## Capabilities

### cmctl-management
Inspect and manage certificates, issuers, and renewals with cmctl.

**Parameters:**
- `name` (string): Certificate resource name
- `namespace` (string): Namespace of the certificate

**Commands:**
- `kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.15.0/cert-manager.yaml`
- `kubectl get certificates -A`
- `kubectl describe certificate example-tls`
- `cmctl check api`
- `cmctl renew example-tls`
- `cmctl status certificate example-tls`

**Examples:**
- kubectl get certificates -A
- cmctl status certificate example-tls
- cmctl renew --all

### acme-issuer-setup
Configure ClusterIssuers with Let's Encrypt and manage issuance resources.

**Parameters:**
- `issuerFile` (string): ClusterIssuer manifest path
- `server` (string): ACME directory URL, e.g. https://acme-v02.api.letsencrypt.org/directory

**Commands:**
- `kubectl get clusterissuers`
- `kubectl apply -f cluster-issuer-letsencrypt.yaml`
- `kubectl get orders.acme.cert-manager.io`
- `kubectl get challenges.acme.cert-manager.io`
- `kubectl get certificaterequests`

**Examples:**
- kubectl apply -f cluster-issuer-letsencrypt.yaml
- kubectl get orders.acme.cert-manager.io -n istio-system
- kubectl get certificaterequests -A

## References
- [cert-manager Documentation](https://cert-manager.io/docs/)
- [cmctl Reference](https://cert-manager.io/docs/usage/cmctl/)
