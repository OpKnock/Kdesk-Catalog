---
name: "ambassador-pattern"
description: "Implements the Ambassador pattern: Emissary-ingress (Edge Stack) as API gateway with Mapping CRDs, plus per-pod ambassador sidecars. Use when working with edge stack, sidecar proxy, api or when the user mentions edge stack, sidecar proxy, api."
---

Implements the Ambassador pattern: Emissary-ingress (Edge Stack) as API gateway with Mapping CRDs, plus per-pod ambassador sidecars.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `kubectl apply -f https://app.getambassador.io/yaml/edge-stac`, `kubectl apply -f sidecar-pod.yaml`
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

# Ambassador Pattern

## What this skill does

Implements the ambassador (sidecar proxy) architecture: Emissary-ingress as the edge gateway with Mapping CRDs, and per-pod sidecars that handle retries, auth, TLS, and observability for the app container.

## When to use

- A service needs consistent auth/TLS/retry logic without code changes
- Routing to microservices by hostname/path at the gateway
- Offloading circuit breaking and tracing to a sidecar

## Real commands

```bash
# Install Emissary-ingress (Edge Stack)
kubectl apply -f https://app.getambassador.io/yaml/edge-stack/latest/aes-crds.yaml
kubectl apply -f https://app.getambassador.io/yaml/edge-stack/latest/aes.yaml
kubectl get pods -n ambassador

# Inspect mappings
kubectl get mappings.getambassador.io
kubectl describe mapping api-mapping

# Sidecar troubleshooting
kubectl logs -c ambassador-sidecar my-api-7d9f5c64b9-x4k2n
```

## Mapping CRD

```yaml
apiVersion: getambassador.io/v3alpha1
kind: Mapping
metadata:
  name: api-mapping
spec:
  hostname: "api.your-app.test"
  prefix: /v1/
  service: api-service:8080
  timeout_ms: 5000
```

## Testing

- Port-forward the gateway and curl http://localhost:8080/v1/health
- Verify mapping routing with `kubectl get mapping -o yaml`

## Best practices

- Keep gateway logic in CRDs (git-ops friendly), not imperative config
- Right-size sidecars with requests/limits
- Prefer Emissary filters (AuthService/FilterPolicy) over app-level auth

## Capabilities

### edge-stack
Install and operate Emissary-ingress and its CRDs.

**Parameters:**
- `namespace` (string): Namespace where Edge Stack runs (default ambassador)
- `mapping_name` (string): Name of the Mapping CRD to inspect

**Commands:**
- `kubectl apply -f https://app.getambassador.io/yaml/edge-stack/latest/aes-crds.yaml`
- `kubectl apply -f https://app.getambassador.io/yaml/edge-stack/latest/aes.yaml`
- `kubectl get mappings.getambassador.io`
- `kubectl get pods -n ambassador`
- `kubectl port-forward svc/edge-stack 8080:80 -n ambassador`

**Examples:**
- kubectl apply -f https://app.getambassador.io/yaml/edge-stack/latest/aes-crds.yaml && kubectl apply -f https://app.getambassador.io/yaml/edge-stack/latest/aes.yaml
- kubectl get mappings.getambassador.io --namespace=default
- kubectl describe mapping api-mapping

### sidecar-proxy
Add ambassador sidecar containers to pods and debug their traffic.

**Parameters:**
- `pod` (string): Pod name with the sidecar
- `container` (string): Container name, e.g. ambassador-sidecar

**Commands:**
- `kubectl apply -f sidecar-pod.yaml`
- `kubectl get pods -l app=my-api`
- `kubectl logs -c ambassador-sidecar my-api-7d9f5c64b9-x4k2n`
- `kubectl exec -it my-api-7d9f5c64b9-x4k2n -c my-api -- curl -s localhost:15001/health`
- `kubectl describe pod my-api-7d9f5c64b9-x4k2n`

**Examples:**
- kubectl logs -f -c ambassador-sidecar my-api-7d9f5c64b9-x4k2n
- kubectl exec -c my-api my-api-7d9f5c64b9-x4k2n -- env | grep AMBASSADOR
- kubectl top pod my-api-7d9f5c64b9-x4k2n

## References
- [Emissary-ingress Docs](https://www.getambassador.io/docs/emissary/latest/)
- [Ambassador Pattern (Microsoft)](https://learn.microsoft.com/en-us/azure/architecture/patterns/ambassador)
- [Ambassador Pattern (Red Hat)](https://developers.redhat.com/articles/2023/02/06/ambassador-pattern-simplifies-burden-microservices)
