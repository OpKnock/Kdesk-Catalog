Operates and troubleshoots the kubelet: service management, journal logs, kubeadm join flow, config flags, and node registration.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `systemctl status kubelet`, `kubeadm token create --print-join-command`
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

# kubelet Operations

Run and fix the node agent that registers workers and runs pods.

## What This Skill Does

- Manages the kubelet systemd unit (status, restart, logs)
- Joins worker nodes via kubeadm tokens
- Dumps and validates kubelet config
- Checks node conditions and registration
- Troubleshoots crashes, auth, and CNI registration failures

## When to Use

- A node shows NotReady
- Kubelet fails to start or constantly restarts
- Adding worker nodes to a cluster

## Real Commands

```bash
# Service management
systemctl status kubelet
systemctl restart kubelet
journalctl -u kubelet -f
journalctl -u kubelet --since '1 hour ago' --no-pager -p err

# Join flow (from control plane)
kubeadm token create --print-join-command
# from worker
kubeadm join 10.0.0.5:6443 --token <token>   --discovery-token-ca-cert-hash sha256:<hash>

# Config and version
kubelet --version
kubelet --config /var/lib/kubelet/config.yaml --dump-config
kubectl get node worker-1 -o jsonpath='{.status.conditions[*].type}'

# Registration check
kubectl get nodes -o wide
kubectl describe node worker-1
```

## Common Failure Patterns

- `failed to run Kubelet: misconfiguration` -> fix --config flags
- `NodeNotReady` + CNI errors -> check CNI pods and kubelet network plugin flag
- Certificate expiry -> `kubeadm certs renew all` + restart

## Best Practices

- Always look at `journalctl -u kubelet -f` first during node issues
- Use `--config` file over legacy flags; keep it in git
- Restart kubelet after config edits and verify with kubectl get nodes
- Keep kubelet and kubeadm versions aligned with the control plane
- Rotate certs proactively before 1-year expiry

## Capabilities

### kubelet-service
Check, restart, and inspect the kubelet systemd service.

**Parameters:**
- `since` (string): Time window for journal logs
- `follow` (boolean): Tail logs with -f

**Commands:**
- `systemctl status kubelet`
- `systemctl restart kubelet`
- `journalctl -u kubelet -f`
- `journalctl -u kubelet --since '1 hour ago' --no-pager`
- `systemctl enable kubelet`
- `kubectl get nodes`

**Examples:**
- systemctl status kubelet
- journalctl -u kubelet -f
- systemctl restart kubelet

### join-and-config
Join nodes to the cluster and inspect kubelet configuration.

**Parameters:**
- `config` (string): Kubelet config file path
- `api-server` (string): Control plane endpoint address

**Commands:**
- `kubeadm token create --print-join-command`
- `kubeadm join 10.0.0.5:6443 --token demo-token --discovery-token-ca-cert-hash sha256:demo-hash`
- `kubelet --version`
- `kubelet --config /var/lib/kubelet/config.yaml --dump-config`
- `kubectl get node worker-1 -o jsonpath='{.status.conditions[*].type}'`

**Examples:**
- kubeadm token create --print-join-command
- kubeadm join 10.0.0.5:6443 --token ... --discovery-token-ca-cert-hash sha256:...
- kubelet --config /var/lib/kubelet/config.yaml --dump-config

## References
- [kubelet Reference](https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/)
- [Kubelet Configuration](https://kubernetes.io/docs/reference/config-api/kubelet-config.v1/)
- [kubeadm Join](https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-join/)