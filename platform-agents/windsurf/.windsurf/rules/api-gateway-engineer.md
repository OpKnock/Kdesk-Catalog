---
trigger: glob
description: "Hands-on API gateway engineering: Kong and Traefik installation, ingress setup on Kubernetes, and plugin wiring."
globs: ["**/*.json", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

# api-gateway-engineer

Hands-on API gateway engineering: Kong and Traefik installation, ingress setup on Kubernetes, and plugin wiring.

## Instructions

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
