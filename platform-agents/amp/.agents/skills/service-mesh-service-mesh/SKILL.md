---
name: "service-mesh-service-mesh"
description: "Deploys, injects, and diagnoses service meshes (Istio, Linkerd) including mTLS, traffic routing, and observability dashboards. Use when working with istio management, linkerd management, traffic routing or when the user mentions istio management, linkerd management, traffic routing."
license: "MIT"
compatibility: "Requires kubernetes, istio, linkerd, helm, jaeger. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "infrastructure"}
allowed-tools: "Glob Grep Read Bash(istioctl:*) Bash(kubectl:*) Bash(linkerd:*)"
---

Deploys, injects, and diagnoses service meshes (Istio, Linkerd) including mTLS, traffic routing, and observability dashboards.

## Agentic Workflow: Read -> Reason -> Act (service-mesh-service-mesh)

You are **service-mesh-service-mesh** (infrastructure) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — infrastructure context for `service-mesh-service-mesh`
- Domain: Deploys, injects, and diagnoses service meshes (Istio, Linkerd) including mTLS, traffic routing, and observability dashboards.
- **istio-management**: Install Istio, inject sidecars, and inspect the mesh. — `istioctl install --set profile=demo -y`
- **linkerd-management**: Install Linkerd, inject proxies, and verify mesh health. — `linkerd install | kubectl apply -f -`
- **traffic-routing**: Apply mTLS, routing, and canary rules. — `istioctl x waypoint apply --enroll-namespace default`
- Check `knowledge` and `prerequisites: kubernetes, istio, linkerd, helm`

### 2. Reason — think for `service-mesh-service-mesh`
- For `istio-management`: Install Istio, inject sidecars, and inspect the mesh. — decide which checks to run
- For `linkerd-management`: Install Linkerd, inject proxies, and verify mesh health. — decide which checks to run
- For `traffic-routing`: Apply mTLS, routing, and canary rules. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `service-mesh-service-mesh` tools
- Tools: `Glob`, `Grep`, `Read`, `Istioctl`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `service-mesh-service-mesh:bea487ad`

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

**Parameters:**
- `profile` (string): Installation profile: default, demo, minimal, external
- `namespace` (string): Namespace to label for injection

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

**Parameters:**
- `deploy` (string): Deployment to inject, stat, or tap
- `namespace` (string): Target namespace

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

**Parameters:**
- `manifest` (string): Mesh config manifest path
- `weight` (number): Traffic weight for canary routing

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

## References
- [Istio Documentation](https://istio.io/latest/docs/)
- [Linkerd Documentation](https://linkerd.io/2.16/overview/)
