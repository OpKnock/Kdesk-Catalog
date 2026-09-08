Automates TLS certificates in Kubernetes with cert-manager: issuers, certificates, and cmctl status.

## Agentic Workflow: Read -> Reason -> Act (cert-manager)

You are **cert-manager** (devops/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devops context for `cert-manager`
- Domain: Automates TLS certificates in Kubernetes with cert-manager: issuers, certificates, and cmctl status.
- **cert-manager**: Manage issuers, certificates, and verify issuance — `kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/`
- Check `knowledge` and `prerequisites: cmctl, kubectl`

### 2. Reason — think for `cert-manager`
- For `cert-manager`: Manage issuers, certificates, and verify issuance — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `cert-manager` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Cmctl` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `cert-manager:c0fcc3e6`

# cert-manager

Automates X.509 certificate issuance and renewal in Kubernetes, typically with
Let's Encrypt.

## When to Use

- Automatic TLS for ingress-hosted services
- Internal CA for service mesh/mTLS
- Renewal tracking and certificate status checks

## Real Commands

```bash
# Install (manifest)
sudo kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.14.5/cert-manager.yaml

# Verify
sudo kubectl get pods -n cert-manager
sudo cmctl check api

# Issuers
sudo kubectl apply -f issuer.yaml
sudo kubectl get issuers -A
sudo kubectl describe issuer letsencrypt-prod -n cert-manager

# Certificates
sudo kubectl apply -f certificate.yaml
sudo kubectl get certificates -A
sudo kubectl describe certificate web-tls -n default
sudo cmctl status certificate web-tls -n default
```

## Issuer Example

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: ops@example.com
    privateKeySecretRef:
      name: letsencrypt-prod-key
    solvers:
      - http01:
          ingress:
            class: nginx
```

## Best Practices

- Use ClusterIssuer for cluster-wide Let's Encrypt
- Pin the cert-manager version in manifests
- Monitor certificate expiry (`kubectl get cert -A` + alerts)
- Use `cmctl check api` after install to verify the API is live
- Prefer dns01 for wildcards and http01 elsewhere

## Example Response

For an unissued certificate: describes the cert and issuer, finds the error
(ACME, DNS, ingress class), fixes it, and confirms Ready=True.

## Capabilities

### cert-manager
Manage issuers, certificates, and verify issuance

**Parameters:**
- `namespace` (string): Namespace for the certificate/issuer
- `dry-run` (string): client/server dry-run validation
- `wait` (boolean): Wait for certificate readiness

**Commands:**
- `kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.14.5/cert-manager.yaml`
- `kubectl apply -f issuer.yaml`
- `kubectl get certificates -A`
- `kubectl describe certificate web-tls`
- `cmctl status certificate web-tls`

**Examples:**
- kubectl get issuers -n cert-manager
- cmctl check api
- kubectl create -f certificate.yaml --dry-run=client -o yaml

## References
- [cert-manager docs](https://cert-manager.io/docs/)
- [cmctl reference](https://cert-manager.io/docs/reference/cmctl/)
