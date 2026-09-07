Kubernetes networking and security with Calico: network policies, IPAM, and node status via calicoctl.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `calicoctl node status`
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

**Parameters:**
- `namespace` (string): Namespace scope for policies
- `output` (string): Output format: yaml, json, wide
- `filename` (string): Policy manifest file for apply/delete (-f)

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

## References
- [Calico docs](https://docs.tigera.io/calico/)
- [Calico network policy guide](https://docs.tigera.io/calico/latest/network-policy/)