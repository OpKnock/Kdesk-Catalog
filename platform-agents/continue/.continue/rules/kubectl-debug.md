---
name: "kubectl-debug"
description: "Debugs failing Kubernetes workloads: pod inspection, log analysis, exec shells, ephemeral debug containers, port-forwarding, and node troubleshooting. Use when working with pod diagnostics, interactive debugging, devops or when the user mentions pod diagnostics, interactive debugging, devops."
globs: ["**/*.r", "**/*.sh"]
alwaysApply: false
---

Debugs failing Kubernetes workloads: pod inspection, log analysis, exec shells, ephemeral debug containers, port-forwarding, and node troubleshooting.

## Agentic Workflow: Read -> Reason -> Act (kubectl-debug)

You are **kubectl-debug** (devops/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devops context for `kubectl-debug`
- Domain: Debugs failing Kubernetes workloads: pod inspection, log analysis, exec shells, ephemeral debug containers, port-forwarding, and node troubleshooting.
- **pod-diagnostics**: Inspect pod state, events, and logs to root-cause failures. — `kubectl describe pod demo-pod`
- **interactive-debugging**: Exec into pods, run ephemeral debug containers, and forward ports. — `kubectl exec -it demo-pod -- sh`
- Check `knowledge` and `prerequisites: kubectl`

### 2. Reason — think for `kubectl-debug`
- For `pod-diagnostics`: Inspect pod state, events, and logs to root-cause failures. — decide which checks to run
- For `interactive-debugging`: Exec into pods, run ephemeral debug containers, and forward ports. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `kubectl-debug` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `kubectl-debug:9d7bf38b`

# Kubernetes Debugging

Root-cause workload failures with a structured kubectl debugging playbook.

## What This Skill Does

- Reads pod status, events, and container logs (incl. previous crashes)
- Execs into containers and runs ephemeral debug images
- Debugs node-level issues without SSH (kubectl debug node/)
- Forwards ports to test services locally
- Copies files out of pods for forensics

## When to Use

- Pods in CrashLoopBackOff, ImagePullBackOff, or Pending
- App misbehaves in-cluster but works locally
- Node issues: kubelet errors, disk pressure, network drops

## Real Commands

```bash
# Diagnose
kubectl describe pod web-7d9f8c9d4-xk2pq
kubectl get events --sort-by=.lastTimestamp
kubectl logs web-7d9f8c9d4-xk2pq --previous
kubectl logs web-7d9f8c9d4-xk2pq -c istio-proxy -f --since=1h
kubectl get pods -o wide
kubectl top pod

# Interact
kubectl exec -it web-7d9f8c9d4-xk2pq -- sh
kubectl run debug --rm -it --restart=Never --image=busybox -- /bin/sh
kubectl debug web-7d9f8c9d4-xk2pq -it --copy-to=debug-pod --container=debug
kubectl debug node/worker-1 -it --image=ubuntu
kubectl port-forward svc/web 8080:80
kubectl cp web-7d9f8c9d4-xk2pq:/var/log/app.log ./app.log
```

## Debug Flow

1. `kubectl get pods -o wide` — where and what state
2. `kubectl describe pod` — events, probes, mounts, images
3. `kubectl logs --previous` — crash loop cause
4. Exec/debug container — runtime evidence
5. Node debug — kubelet/CNI-level causes

## Best Practices

- Check `--previous` logs first on CrashLoopBackOff
- Use ephemeral containers over exec when the image lacks tools
- Time-box port-forward sessions; use `&` with job control
- Capture `kubectl get events` before deleting evidence
- For DNS/network issues, debug from inside the pod network namespace

## Capabilities

### pod-diagnostics
Inspect pod state, events, and logs to root-cause failures.

**Parameters:**
- `pod` (string): Pod name
- `container` (string): Container name for logs

**Commands:**
- `kubectl describe pod demo-pod`
- `kubectl get events --sort-by=.lastTimestamp`
- `kubectl logs demo-pod --previous`
- `kubectl logs demo-pod -c sidecar -f --since=1h`
- `kubectl get pods -o wide`
- `kubectl top pod`

**Examples:**
- kubectl describe pod web-7d9f8c9d4-xk2pq
- kubectl logs web-7d9f8c9d4-xk2pq --previous
- kubectl get events --sort-by=.lastTimestamp | tail -30

### interactive-debugging
Exec into pods, run ephemeral debug containers, and forward ports.

**Parameters:**
- `node` (string): Node name for node debugging
- `image` (string): Debug image
- `local-port` (string): Port mapping for port-forward

**Commands:**
- `kubectl exec -it demo-pod -- sh`
- `kubectl run debug --rm -it --restart=Never --image=busybox -- /bin/sh`
- `kubectl debug node/demo-node -it --image=ubuntu`
- `kubectl port-forward svc/web 8080:80`
- `kubectl debug demo-pod -it --copy-to=debug-pod --container=debug`
- `kubectl cp demo-pod:/tmp/dump.tar ./dump.tar`

**Examples:**
- kubectl exec -it web-7d9f8c9d4-xk2pq -- sh
- kubectl debug node/worker-1 -it --image=ubuntu
- kubectl port-forward svc/web 8080:80

## References
- [Debugging Running Pods](https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/)
- [kubectl debug](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_debug/)
- [Debugging Nodes](https://kubernetes.io/docs/tasks/debug/debug-cluster/kubectl-node-debug/)