---
name: "edge-computing"
description: "Deploys edge computing environments with K3s, k3d, and KubeEdge: lightweight clusters, offline agents, and edge device management. Use when working with lightweight clusters, edge devices or when the user mentions lightweight clusters, edge devices."
type: knowledge
triggers: ["edge-computing", "lightweight-clusters", "edge-devices"]
---

Deploys edge computing environments with K3s, k3d, and KubeEdge: lightweight clusters, offline agents, and edge device management.

## Agentic Workflow: Read -> Reason -> Act (edge-computing)

You are **edge-computing** (infrastructure) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — infrastructure context for `edge-computing`
- Domain: Deploys edge computing environments with K3s, k3d, and KubeEdge: lightweight clusters, offline agents, and edge device management.
- **lightweight-clusters**: Stand up K3s servers/agents and k3d dev clusters. — `curl -sfL https://get.k3s.io | sh -`
- **edge-devices**: Manage edge devices with balena and KubeEdge. — `balena login`
- Check `knowledge` and `prerequisites: node.js, deno, wrangler`

### 2. Reason — think for `edge-computing`
- For `lightweight-clusters`: Stand up K3s servers/agents and k3d dev clusters. — decide which checks to run
- For `edge-devices`: Manage edge devices with balena and KubeEdge. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `edge-computing` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `K3s` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `edge-computing:c456252e`

# Edge Computing Operations

Run Kubernetes and workloads at the edge: lightweight clusters and device fleets.

## What This Skill Does

- Installs K3s single-node and multi-node edge clusters
- Creates k3d clusters for edge development
- Joins edge agents to a K3s server
- Manages device fleets with balena
- Bridges cloud-edge with KubeEdge

## When to Use

- On-prem/shop-floor/field deployments with limited resources
- Developing against edge-shaped clusters
- Fleet management of many small devices

## Real Commands

```bash
# K3s single node
curl -sfL https://get.k3s.io | sh -
k3s kubectl get nodes
k3s ctr images ls
sudo k3s kubectl get pods -A

# K3s agent join
curl -sfL https://get.k3s.io |   K3S_URL=https://edge-master:6443 K3S_TOKEN=secret sh -

# k3d dev clusters
k3d cluster create edge --servers 1 --agents 2
k3d cluster list
k3d node list

# Balena fleet
balena login
balena push myfleet
balena logs myfleet --tail 100
balena ssh 27a3f1

# KubeEdge
keadm join --cloudcore-ipport=10.0.0.5:10000
kubeedge edgecore --config edgecore.yaml
```

## Best Practices

- Use K3s for constrained nodes; set ResourceQuota per edge device
- Keep K3s storage (local-path) tuned for SD cards (write frequency)
- Use k3d for CI-safe edge development
- Use balena for long-lived fleet updates and rollbacks
- For KubeEdge, pair cloudcore HA with edgecore retries

## Capabilities

### lightweight-clusters
Stand up K3s servers/agents and k3d dev clusters.

**Parameters:**
- `server-url` (string): K3s server URL for agents
- `token` (string): K3s join token

**Commands:**
- `curl -sfL https://get.k3s.io | sh -`
- `curl -sfL https://get.k3s.io | K3S_URL=https://edge-master:6443 K3S_TOKEN=secret sh -`
- `k3s kubectl get nodes`
- `k3d cluster create edge --servers 1 --agents 2`
- `k3d cluster list`
- `k3s ctr images ls`

**Examples:**
- curl -sfL https://get.k3s.io | sh -
- k3d cluster create edge --servers 1 --agents 2
- k3s kubectl get nodes

### edge-devices
Manage edge devices with balena and KubeEdge.

**Parameters:**
- `fleet` (string): Balena fleet name
- `device` (string): Balena device uuid

**Commands:**
- `balena login`
- `balena push myfleet`
- `balena logs myfleet --tail 100`
- `balena ssh 27a3f1`
- `kubeedge edgecore --config edgecore.yaml`
- `keadm join --cloudcore-ipport=10.0.0.5:10000`

**Examples:**
- balena push myfleet
- balena logs myfleet --tail 100
- keadm join --cloudcore-ipport=10.0.0.5:10000

## References
- [K3s Documentation](https://docs.k3s.io/)
- [k3d](https://k3d.io/)
- [KubeEdge](https://kubeedge.io/en/docs/)
- [balena CLI](https://www.balena.io/docs/reference/cli/)
