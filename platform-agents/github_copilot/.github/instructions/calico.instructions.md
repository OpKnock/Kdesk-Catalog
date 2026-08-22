---
applyTo: "**/*.r **/*.sh **/*.{yaml,yml}"
---

# calico

Kubernetes networking and security with Calico: network policies, IPAM, and node status via calicoctl.

## Instructions

# Calico

Kubernetes CNI with policy enforcement: secure network policies, IP pool
management, and cluster health.

## When to Use

- Enforcing namespace/tenant isolation
- Controlling egress to the internet
- Diagnosing pod connectivity issues

## Real Commands

```bash
# Cluster state
sudo calicoctl node status
sudo calicoctl get nodes

# Policies
sudo calicoctl apply -f policy.yaml
sudo calicoctl get networkpolicy -o yaml
sudo calicoctl get networkpolicy --namespace=default -o wide
sudo calicoctl delete networkpolicy deny-all --namespace=default

# IPAM
sudo calicoctl ipam show
sudo calicoctl get ippool -o wide

# BGP
sudo calicoctl get bgppeer -o yaml
```

## Policy Example (policy.yaml)

```yaml
apiVersion: projectcalico.org/v3
kind: NetworkPolicy
metadata:
  name: app-only-ingress
  namespace: payments
spec:
  selector: app == 'api'
  ingress:
    - action: Allow
      protocol: TCP
      source:
        namespaceSelector: projectcalico.org/name == 'web'
      destination:
        ports: [8080]
```

## Best Practices

- Start with default-deny per namespace, then allow what's needed
- Use namespace selectors, not hardcoded IPs
- Test policy changes on staging namespaces first
- Check `calicoctl node status` when pods can't reach each other
- Watch IP pool exhaustion with ipam show

## Example Response

For connectivity failure: checks node status, IPAM, and policy selectors, then
applies the correct policy and verifies traffic.

## Capabilities

### calicoctl
Manage Calico network policies, IP pools, and node health

**Commands:**
- `calicoctl node status`
- `calicoctl get nodes`
- `calicoctl apply -f policy.yaml`
- `calicoctl get networkpolicy -o yaml`
- `calicoctl ipam show`

**Examples:**
- calicoctl get ippool -o wide
- calicoctl delete networkpolicy deny-all --namespace=default
- calicoctl get bgppeer -o yaml
