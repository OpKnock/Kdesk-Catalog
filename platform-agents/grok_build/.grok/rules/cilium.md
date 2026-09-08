Installs, verifies, and debugs the Cilium CNI with eBPF data plane, CiliumNetworkPolicy, and Hubble observability.

## Agentic Workflow: Read -> Reason -> Act (cilium)

You are **cilium** (devops/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devops context for `cilium`
- Domain: Installs, verifies, and debugs the Cilium CNI with eBPF data plane, CiliumNetworkPolicy, and Hubble observability.
- **cilium-install-and-verify**: Install Cilium into a Kubernetes cluster and run connectivity and upgrade verification. — `cilium install --version v1.16.4`
- **hubble-observability**: Inspect service-to-service traffic flows with Hubble CLI and troubleshoot connectivity issues. — `hubble status`
- Check `knowledge` and `prerequisites: cilium, hubble`

### 2. Reason — think for `cilium`
- For `cilium-install-and-verify`: Install Cilium into a Kubernetes cluster and run connectivity and upgrade verification. — decide which checks to run
- For `hubble-observability`: Inspect service-to-service traffic flows with Hubble CLI and troubleshoot connectivity issues. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `cilium` tools
- Tools: `Glob`, `Grep`, `Read`, `Cilium`, `Hubble` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `cilium:c627917d`

# Cilium Networking

Deploy and troubleshoot the Cilium CNI: eBPF data plane, network policies, and Hubble observability.

## What This Skill Does

- Installs Cilium with the cilium CLI and Helm
- Verifies the data plane with `cilium status` and `cilium connectivity test`
- Author CiliumNetworkPolicy (L3/L4/L7) policies
- Observes and filters traffic with Hubble
- Diagnoses dropped packets, DNS failures, and identity issues

## When to Use

- Installing a CNI with eBPF, kube-proxy replacement, or BGP
- Pods cannot reach each other and you need flow-level answers
- Enforcing zero-trust east-west policies

## Real Commands

```bash
# Install and verify
cilium install --version v1.16.4
cilium status --wait
cilium connectivity test --timeout 10m

# Inspect state
cilium identity list
cilium endpoint list
cilium policy get default/allow-all
cilium monitor --type drop

# Hubble traffic flows
hubble status
hubble observe --pod default/web-0 --last 200
hubble observe --verdict DROPPED --last 100
hubble observe --to-namespace kube-system --type to-endpoint
```

## CiliumNetworkPolicy Example

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: allow-nginx-ingress
  namespace: default
spec:
  endpointSelector:
    matchLabels: { app: nginx }
  ingress:
    - fromEndpoints:
        - matchLabels: { app: frontend }
      toPorts:
        - ports:
            - port: "80"
              protocol: TCP
```

## Best Practices

- Run `cilium connectivity test` after every upgrade
- Set `kubeProxyReplacement: strict` and verify with `cilium status | grep KubeProxyReplacement`
- Use CiliumNetworkPolicy namespaces to segment tenants
- Monitor drops with `cilium monitor --type drop` before changing policies
- Keep Hubble relay storage sized for your flow volume

## Capabilities

### cilium-install-and-verify
Install Cilium into a Kubernetes cluster and run connectivity and upgrade verification.

**Parameters:**
- `version` (string): Cilium version to install or upgrade to
- `kubeconfig` (string): Path to kubeconfig when outside the cluster

**Commands:**
- `cilium install --version v1.16.4`
- `cilium status --wait`
- `cilium connectivity test`
- `cilium upgrade`
- `cilium uninstall`

**Examples:**
- cilium install --version v1.16.4
- cilium status --wait
- cilium connectivity test --timeout 10m

### hubble-observability
Inspect service-to-service traffic flows with Hubble CLI and troubleshoot connectivity issues.

**Parameters:**
- `verdict` (string): Filter flows by verdict: FORWARDED, DROPPED, ERROR
- `namespace` (string): Filter flows by namespace

**Commands:**
- `hubble status`
- `hubble observe --pod default/web-0`
- `hubble observe --verdict DROPPED`
- `hubble observe --from-pod default/curl-0 --to-namespace kube-system`
- `hubble flow`

**Examples:**
- hubble observe --verdict DROPPED --last 100
- hubble observe --to-pod kube-system/coredns-*
- hubble status

## References
- [Cilium Documentation](https://docs.cilium.io/en/stable/)
- [Cilium CLI GitHub](https://github.com/cilium/cilium-cli)
- [Hubble UI](https://github.com/cilium/hubble)