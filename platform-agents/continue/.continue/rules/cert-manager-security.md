---
name: "cert-manager-security"
description: "Issues, renews, and troubleshoots TLS certificates in Kubernetes with cert-manager, ACME issuers, and the cmctl CLI. Use when working with cmctl management, acme issuer setup, security or when the user mentions cmctl management, acme issuer setup, security."
globs: ["**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
alwaysApply: false
---

Issues, renews, and troubleshoots TLS certificates in Kubernetes with cert-manager, ACME issuers, and the cmctl CLI.

## Agentic Workflow: Read -> Reason -> Act (cert-manager-security)

You are **cert-manager-security** (security/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — security context for `cert-manager-security`
- Domain: Issues, renews, and troubleshoots TLS certificates in Kubernetes with cert-manager, ACME issuers, and the cmctl CLI.
- **cmctl-management**: Inspect and manage certificates, issuers, and renewals with cmctl. — `kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/`
- **acme-issuer-setup**: Configure ClusterIssuers with Let's Encrypt and manage issuance resources. — `kubectl get clusterissuers`
- Check `knowledge` and `prerequisites: cmctl, kubectl`

### 2. Reason — think for `cert-manager-security`
- For `cmctl-management`: Inspect and manage certificates, issuers, and renewals with cmctl. — decide which checks to run
- For `acme-issuer-setup`: Configure ClusterIssuers with Let's Encrypt and manage issuance resources. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `cert-manager-security` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Cmctl` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `cert-manager-security:19ac58ac`

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