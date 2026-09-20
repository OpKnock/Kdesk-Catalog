---
trigger: glob
description: "Designs zero-trust pod networking with Kubernetes NetworkPolicies: default-deny, allowlists, and verification of actual traffic flow. Use when working with policies, verify or when the user mentions policies, verify."
globs: ["**/*.json", "**/*.r", "**/*.rs", "**/*.sh", "**/*.{yaml,yml}"]
---

Designs zero-trust pod networking with Kubernetes NetworkPolicies: default-deny, allowlists, and verification of actual traffic flow.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `kubectl get networkpolicies -A`, `kubectl run nettest --image=curlimages/curl -it --rm -- curl`
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

# Kubernetes Network Policies

Lock down pod-to-pod traffic with NetworkPolicies and prove it.

## When to Use

- Zero-trust segmentation between services
- PCI/HIPAA namespace isolation
- Debugging why a policy blocks legitimate traffic

## Default-deny first

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny
  namespace: payments
spec:
  podSelector: {}
  policyTypes: [Ingress, Egress]
```

```bash
kubectl apply -f default-deny.yaml
```

Start with default-deny, then add allow rules - never the reverse.

## Allow ingress from api

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-api
  namespace: payments
spec:
  podSelector:
    matchLabels: { app: payments }
  policyTypes: [Ingress]
  ingress:
    - from:
        - podSelector:
            matchLabels: { app: api }
      ports:
        - port: 8080
```

## Verify with real traffic

```bash
kubectl run nettest --image=curlimages/curl -it --rm --namespace payments -- curl -s http://api:80/healthz
kubectl exec deploy/payments -- wget -qO- http://db:5432 -T 2 || echo 'blocked'
```

A timeout (not connection refused) usually means the policy dropped the packet.

## Egress for DNS and TLS

Allow kube-dns egress, plus explicit egress targets with ports.

## Best practices

- Enforce default-deny globally via an admission controller.
- Policy as code: review in the same PR as the workload.
- Test both allowed and blocked paths in CI.
- Use Cilium/KubeArmor for L7 rules where L4 is not enough.

## Testing

Run the probe matrix after every policy change: expected-allow and expected-block cases.

## Capabilities

### policies
Create and inspect NetworkPolicies.

**Parameters:**
- `namespace` (string): Namespace to scope queries
- `manifest` (string): Policy YAML file
- `output` (string): Output format: wide, yaml, json

**Commands:**
- `kubectl get networkpolicies -A`
- `kubectl apply -f default-deny.yaml`
- `kubectl describe netpol checkout-allow --namespace payments`
- `kubectl get networkpolicies --all-namespaces -o json | jq '.items[] | {name: .metadata.name, ns: .metadata.namespace}'`
- `kubectl delete netpol legacy-allow --namespace legacy`

**Examples:**
- kubectl get networkpolicies -n payments -o wide
- kubectl apply -f allow-api.yaml --dry-run=client -o yaml
- kubectl describe networkpolicies -n ingress | grep -E 'PolicyTypes|To|From'

### verify
Prove policy behavior with real traffic probes.

**Parameters:**
- `image` (string): Probe container image
- `timeout` (number): Connection timeout to detect blocking
- `namespace` (string): Namespace for the probe pod

**Commands:**
- `kubectl run nettest --image=curlimages/curl -it --rm -- curl -s http://payments:8080/healthz`
- `kubectl run probe --image=busybox -it --rm -- wget -qO- http://auth-service:80`
- `kubectl exec deploy/payments -- wget -qO- http://db:5432 -T 2 || echo 'blocked'`
- `kubectl run probe --image=curlimages/curl -it --rm --timeout 5s -- curl -s http://localhost:8080`
- `kubectl logs deploy/probe -n kube-system --tail=20`

**Examples:**
- kubectl run nettest --image=curlimages/curl -it --rm --namespace payments -- curl -s http://web:80
- kubectl exec deploy/api -- wget -T 2 -qO- http://redis:6379 && echo allowed
- kubectl run probe --image=busybox --rm -it -- wget -T 3 -qO- http://auth:80

## References
- [Kubernetes NetworkPolicies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
- [Cilium Network Policy docs](https://docs.cilium.io/en/stable/security/policy/)
- [kubectl cheatsheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
