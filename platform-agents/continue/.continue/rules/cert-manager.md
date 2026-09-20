---
name: "cert-manager"
description: "Automates TLS certificates in Kubernetes with cert-manager: issuers, certificates, and cmctl status."
globs: ["**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
alwaysApply: false
---

# cert-manager

Automates TLS certificates in Kubernetes with cert-manager: issuers, certificates, and cmctl status.

## Instructions

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