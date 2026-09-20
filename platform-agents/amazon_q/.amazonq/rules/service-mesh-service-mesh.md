# service-mesh-service-mesh

Deploys, injects, and diagnoses service meshes (Istio, Linkerd) including mTLS, traffic routing, and observability dashboards.

## Instructions

# Service Mesh

Operate Istio and Linkerd service meshes for mTLS, routing, and observability.

## What This Skill Does

- Installs Istio/Linkerd and verifies mesh health
- Injects sidecars into namespaces and workloads
- Applies mTLS, virtual service, and canary routing rules
- Inspects proxy config and dashboards for traffic

## When to Use

- Securing service-to-service traffic with mTLS
- Rolling out canary or weighted routing
- Debugging mesh latency or connectivity

## Real Commands

```bash
# Istio
istioctl install --set profile=demo -y
istioctl analyze
istioctl proxy-status
istioctl proxy-config routes deployment/reviews.default
kubectl label namespace default istio-injection=enabled
istioctl dashboard kiali

# Linkerd
linkerd install | kubectl apply -f -
linkerd check
linkerd inject deploy/ | kubectl apply -f -
linkerd viz dashboard
linkerd stat deploy
linkerd tap deploy/web
```

## Canary Routing (Istio)

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: reviews
spec:
  hosts: [reviews]
  http:
    - route:
        - destination: { host: reviews, subset: v2 }
          weight: 10
        - destination: { host: reviews, subset: v1 }
          weight: 90
```

## Best Practices

- Verify sidecar injection before rollout (kubectl get pods -o wide)
- Run istioctl analyze after every manifest change
- Enforce strict mTLS via PeerAuthentication after staged rollout
- Use weighted routing for canaries; shift 10% increments
- Monitor with Kiali/Grafana dashboards in every mesh

## Capabilities

### istio-management
Install Istio, inject sidecars, and inspect the mesh.

**Commands:**
- `istioctl install --set profile=demo -y`
- `istioctl analyze`
- `istioctl proxy-status`
- `istioctl proxy-config routes deployment/reviews.default`
- `kubectl label namespace default istio-injection=enabled`
- `istioctl dashboard kiali`

**Examples:**
- istioctl install --set profile=demo -y
- istioctl analyze --use-kube=false --list-validators
- istioctl proxy-status

### linkerd-management
Install Linkerd, inject proxies, and verify mesh health.

**Commands:**
- `linkerd install | kubectl apply -f -`
- `linkerd check`
- `linkerd inject deploy/ | kubectl apply -f -`
- `linkerd viz dashboard`
- `linkerd stat deploy`
- `linkerd tap deploy/web`

**Examples:**
- linkerd install | kubectl apply -f -
- linkerd check --pre
- linkerd stat deploy

### traffic-routing
Apply mTLS, routing, and canary rules.

**Commands:**
- `istioctl x waypoint apply --enroll-namespace default`
- `kubectl apply -f virtualservice.yaml`
- `kubectl apply -f peerauthentication.yaml`
- `kubectl apply -f destinationrule.yaml`
- `kubectl get virtualservices`

**Examples:**
- kubectl apply -f virtualservice.yaml
- kubectl apply -f peerauthentication.yaml
- kubectl get virtualservices