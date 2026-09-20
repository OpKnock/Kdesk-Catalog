---
name: "api-gateway-engineer"
description: "Hands-on API gateway engineering: Kong and Traefik installation, ingress setup on Kubernetes, and plugin wiring. Use when working with kong setup, traefik ingress or when the user mentions kong setup, traefik ingress."
---

Hands-on API gateway engineering: Kong and Traefik installation, ingress setup on Kubernetes, and plugin wiring.

## Agentic Workflow: Read -> Reason -> Act (api-gateway-engineer)

You are **api-gateway-engineer** (infrastructure) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — infrastructure context for `api-gateway-engineer`
- Domain: Hands-on API gateway engineering: Kong and Traefik installation, ingress setup on Kubernetes, and plugin wiring.
- **kong-setup**: Install Kong, bootstrap the database, and configure services and routes — `kong migrations bootstrap`
- **traefik-ingress**: Configure Traefik as Kubernetes ingress with middlewares and TLS — `helm repo add traefik https://helm.traefik.io/traefik && helm install traefik tr`
- Check `knowledge` and `prerequisites: kong, traefik, aws-cli`

### 2. Reason — think for `api-gateway-engineer`
- For `kong-setup`: Install Kong, bootstrap the database, and configure services and routes — decide which checks to run
- For `traefik-ingress`: Configure Traefik as Kubernetes ingress with middlewares and TLS — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-gateway-engineer` tools
- Tools: `Glob`, `Grep`, `Read`, `Kong`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-gateway-engineer:5e95f123`

# API Gateway Engineer

Installs and operates API gateways in front of services.

## When to Use
- Rolling out a gateway for the first time
- Moving auth/rate limits to the edge
- Kubernetes ingress management

## Real Commands

```bash
# Kong
kong migrations bootstrap
kong start
curl -s -X POST http://localhost:8001/services -H 'Content-Type: application/json' -d '{"name":"orders","url":"http://orders-service:8080"}'
curl -s -X POST http://localhost:8001/services/orders/routes -H 'Content-Type: application/json' -d '{"paths":["/orders"]}'

# Traefik on K8s
helm repo add traefik https://helm.traefik.io/traefik
helm install traefik traefik/traefik
kubectl apply -f ingressroute.yaml
kubectl get ingressroute -A
```

## IngressRoute Example

```yaml
apiVersion: traefik.io/v1alpha1
kind: IngressRoute
metadata: {name: api}
spec:
  entryPoints: [web]
  routes:
    - match: Host(`api.example.com`) && PathPrefix(`/orders`)
      kind: Rule
      services: [{name: orders, port: 8080}]
```

## Testing
Route real traffic through the gateway and verify headers, rate limits, and health checks.

## Best Practices
- Run gateway nodes with redundancy
- Enable access logs for auditing

## Capabilities

### kong-setup
Install Kong, bootstrap the database, and configure services and routes

**Parameters:**
- `service` (string): Upstream service
- `upstreamUrl` (string): Upstream URL

**Commands:**
- `kong migrations bootstrap`
- `kong start`
- `curl -s -X POST http://localhost:8001/services -H 'Content-Type: application/json' -d '{"name":"orders","url":"http://orders-service:8080"}'`
- `curl -s -X POST http://localhost:8001/services/orders/routes -H 'Content-Type: application/json' -d '{"paths":["/orders"]}'`
- `kong health`

**Examples:**
- kong migrations bootstrap && kong start
- curl -s -X POST http://localhost:8001/services -H 'Content-Type: application/json' -d '{"name":"orders","url":"http://orders-service:8080"}'
- curl -s http://localhost:8001/services | python -m json.tool

### traefik-ingress
Configure Traefik as Kubernetes ingress with middlewares and TLS

**Parameters:**
- `namespace` (string): Kubernetes namespace
- `host` (string): Ingress host

**Commands:**
- `helm repo add traefik https://helm.traefik.io/traefik && helm install traefik traefik/traefik`
- `kubectl apply -f ingressroute.yaml`
- `kubectl get ingressroute -A`
- `kubectl apply -f middleware-rate-limit.yaml`
- `kubectl logs -l app.kubernetes.io/name=traefik -n traefik --tail=50`

**Examples:**
- helm install traefik traefik/traefik -n traefik --create-namespace
- kubectl apply -f ingressroute.yaml && kubectl get ingressroute -A
- kubectl logs -l app.kubernetes.io/name=traefik -n traefik --tail=50

## References
- [Kong Gateway Install](https://docs.konghq.com/gateway/latest/install/)
- [Traefik Kubernetes Ingress](https://doc.traefik.io/traefik/routing/providers/kubernetes-crd/)
