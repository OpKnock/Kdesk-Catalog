---
trigger: glob
description: "Debugs containers and pods at the CRI level with crictl: inspect sandboxes, run containers directly, and read container logs and stats. Use when working with cri inspection, debug and logs, devops or when the user mentions cri inspection, debug and logs, devops."
globs: ["**/*.json", "**/*.r", "**/*.sh"]
---

Debugs containers and pods at the CRI level with crictl: inspect sandboxes, run containers directly, and read container logs and stats.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `crictl ps`, `crictl run --no-pull debug-container.json sandbox.json`
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

# crictl CRI Debugging

Inspect containers and pods at the container-runtime-interface level, below kubectl.

## What This Skill Does

- Lists pods and containers the way containerd sees them
- Inspects sandbox and container details (images, mounts, labels)
- Execs and reads logs without relying on the API server
- Runs one-off debug containers (e.g. busybox) inside the runtime
- Pulls stats and prunes stale images/containers

## When to Use

- kubectl hangs or the API server is down but nodes run containers
- Debugging container start failures, OOM kills, or runtime errors
- Forensics: what is actually running on a node right now

## Real Commands

```bash
# Inspect
crictl pods
crictl pods --state Ready
crictl ps -a
crictl inspect 3e2d1c4a          # container details
crictl inspectp a9b8c7d6         # pod sandbox details
crictl images
crictl info                      # runtime + CRI version

# Debug
crictl run --no-pull debug.json sandbox.json
crictl exec -it 3e2d1c4a sh
crictl logs --tail 200 3e2d1c4a
crictl stats

# Cleanup
crictl rm -f <id>
crictl rmi --prune
crictl cleanup
```

## Debug Container Config

```json
{
  "metadata": { "name": "debug-container" },
  "image": { "image": "busybox" },
  "command": ["sh", "-c", "sleep 3600"],
  "stdin": true
}
```

## Best Practices

- Set `--runtime-endpoint unix:///run/containerd/containerd.sock` on containerd nodes
- Use `crictl inspect` output (JSON) with jq for scripting
- Prefer `crictl logs --tail` over full logs in production
- Use `crictl stats` to spot CPU/mem pressure before OOM-kill forensics

## Capabilities

### cri-inspection
List, inspect, and describe pods and containers as seen by the container runtime.

**Parameters:**
- `id` (string): Container or pod sandbox ID prefix
- `state` (string): Filter by state: Running, Exited, Ready

**Commands:**
- `crictl ps`
- `crictl pods`
- `crictl inspect $(docker ps -q)`
- `crictl inspectp demo-pod-id`
- `crictl images`
- `crictl info`

**Examples:**
- crictl ps -a
- crictl inspect 3e2d1c4a
- crictl pods --state Ready

### debug-and-logs
Run one-off debug containers, exec into running containers, and stream logs at runtime level.

**Parameters:**
- `container-id` (string): Container ID prefix
- `tail` (integer): Number of log lines to show

**Commands:**
- `crictl run --no-pull debug-container.json sandbox.json`
- `crictl exec -it $(docker ps -q) sh`
- `crictl logs --tail 100 $(docker ps -q)`
- `crictl stats`
- `crictl rm $(docker ps -q)`
- `crictl rmi --prune`

**Examples:**
- crictl exec -it 3e2d1c4a sh
- crictl logs --tail 200 3e2d1c4a
- crictl stats

## References
- [crictl Reference (Kubernetes)](https://kubernetes.io/docs/reference/tools/mapcrictl/)
- [crictl GitHub](https://github.com/kubernetes-sigs/cri-tools/blob/master/docs/crictl.md)
