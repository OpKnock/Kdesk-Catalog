---
type: agent_requested
description: "Manages TLS certificates in Kubernetes with cert-manager and cmctl: issuance, renewal, approval, and cluster status. Use when working with cmctl, issuers, infrastructure or when the user mentions cmctl, issuers, infrastructure."
---

Manages TLS certificates in Kubernetes with cert-manager and cmctl: issuance, renewal, approval, and cluster status.

## Agentic Workflow: Read -> Reason -> Act (cert-manager-infrastructure)

You are **Cert Manager** (infrastructure/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — infrastructure context for `cert-manager-infrastructure`
- Domain: Manages TLS certificates in Kubernetes with cert-manager and cmctl: issuance, renewal, approval, and cluster status.
- **cmctl**: Inspect and operate cert-manager resources with cmctl. — `cmctl check api`
- **issuers**: Manage ClusterIssuers and certificates via kubectl. — `kubectl apply -f clusterissuer.yaml`
- Check `knowledge` and `prerequisites: cmctl, kubectl`

### 2. Reason — think for `cert-manager-infrastructure`
- For `cmctl`: Inspect and operate cert-manager resources with cmctl. — decide which checks to run
- For `issuers`: Manage ClusterIssuers and certificates via kubectl. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `cert-manager-infrastructure` tools
- Tools: `Glob`, `Grep`, `Read`, `Cmctl`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `cert-manager-infrastructure:01349e8f`

# cert-manager

Automate TLS certificate lifecycle in Kubernetes.

## When to Use

- Issuing Let's Encrypt certificates for ingresses
- Monitoring certificate expiry and renewal failures
- Approving internal certificate requests

## ClusterIssuer

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: ops@example.com
    privateKeySecretRef: { name: letsencrypt-prod-key }
    solvers:
      - http01: { ingress: { class: nginx } }
```

```bash
kubectl apply -f clusterissuer.yaml
```

Use the staging server first to avoid rate limits during testing.

## Certificate

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata: { name: ingress-tls, namespace: web }
spec:
  secretName: ingress-tls
  issuerRef: { name: letsencrypt-prod, kind: ClusterIssuer }
  dnsNames: [www.example.com, api.example.com]
```

```bash
kubectl apply -f certificate.yaml
cmctl status certificate ingress-tls --namespace web
```

## Renewal and troubleshooting

```bash
cmctl renew ingress-tls --namespace web --failsafe
kubectl describe certificate ingress-tls
kubectl get challenges -A
```

Check challenges when renewal stalls - HTTP01 fails usually mean ingress misrouting.

## Best practices

- Set `renewBefore` to 30 days (default 2/3 lifetime).
- Alert when `cmctl status certificate` shows NotReady.
- Keep ACME email valid - expiry notices are sent there.
- Prefer external DNS01 for wildcards; internal ClusterIssuer for mTLS.

## Testing

```bash
cmctl check api
cmctl status certificate ingress-tls
```

Verify certs are 30+ days from expiry after renewal runs.

## Capabilities

### cmctl
Inspect and operate cert-manager resources with cmctl.

**Parameters:**
- `name` (string): Certificate or CertificateRequest name
- `namespace` (string): Namespace of the resource
- `wait` (string): Wait duration for API readiness

**Commands:**
- `cmctl check api`
- `cmctl status certificate my-tls-cert`
- `cmctl renew my-tls-cert`
- `cmctl approve certificate/my-tls-cert`
- `cmctl status certificaterequest/my-tls-cert-1234`

**Examples:**
- cmctl status certificate ingress-tls --namespace web
- cmctl renew ingress-tls --namespace web --failsafe
- cmctl check api --wait 10m

### issuers
Manage ClusterIssuers and certificates via kubectl.

**Parameters:**
- `resource` (string): certificate, certificaterequest, clusterissuer, challenge
- `all-namespaces` (string): Query across namespaces with -A
- `output` (string): Output format: wide, yaml, json

**Commands:**
- `kubectl apply -f clusterissuer.yaml`
- `kubectl get certificates -A`
- `kubectl get certificaterequests -A`
- `kubectl describe certificate ingress-tls`
- `kubectl get challenges -A`

**Examples:**
- kubectl get certificates -A | grep -v READY
- kubectl describe clusterissuer letsencrypt-prod
- kubectl get challenges -A -o wide

## References
- [cert-manager Docs](https://cert-manager.io/docs/)
- [cmctl](https://cert-manager.io/docs/usage/cmctl/)
- [Let's Encrypt with cert-manager](https://cert-manager.io/docs/configuration/acme/)