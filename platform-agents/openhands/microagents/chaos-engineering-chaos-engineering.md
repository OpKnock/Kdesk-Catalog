---
name: "chaos-engineering-chaos-engineering"
description: "Practices chaos engineering with LitmusChaos, Chaos Monkey, and fault injection to verify resilience of distributed systems. Use when working with litmus chaos, fault injection or when the user mentions litmus chaos, fault injection."
type: knowledge
triggers: ["chaos-engineering-chaos-engineering", "litmus-chaos", "fault-injection"]
---

Practices chaos engineering with LitmusChaos, Chaos Monkey, and fault injection to verify resilience of distributed systems.

## Agentic Workflow: Read -> Reason -> Act (chaos-engineering-chaos-engineering)

You are **chaos-engineering-chaos-engineering** (devops) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devops context for `chaos-engineering-chaos-engineering`
- Domain: Practices chaos engineering with LitmusChaos, Chaos Monkey, and fault injection to verify resilience of distributed systems.
- **litmus-chaos**: Run chaos experiments on Kubernetes. — `kubectl apply -f https://litmuschaos.github.io/litmus/litmus-operator-v2.14.0.ya`
- **fault-injection**: Inject network and resource faults. — `kubectl run net-test --image=alpine -- sleep 3600`
- Check `knowledge` and `prerequisites: docker, kubernetes, litmus, chaos-mesh`

### 2. Reason — think for `chaos-engineering-chaos-engineering`
- For `litmus-chaos`: Run chaos experiments on Kubernetes. — decide which checks to run
- For `fault-injection`: Inject network and resource faults. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `chaos-engineering-chaos-engineering` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Litmusctl` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `chaos-engineering-chaos-engineering:3b72004e`

# Chaos Engineering

Verify resilience by breaking things on purpose.

## When to Use

- Proving retries, timeouts, and failover actually work
- Testing dependency failures (DB, cache, third-party API)
- Validating chaos under realistic traffic, not just in tests
- Building confidence for incident response

## Principles

- Steady state: define normal behavior first (latency, error rate)
- Hypothesis: the system tolerates fault X without user impact
- Blast radius: start small, expand gradually
- Roll back fast: abort experiment on threshold breach

## Commands

```bash
# Install Litmus
kubectl apply -f https://litmuschaos.github.io/litmus/litmus-operator-v2.14.0.yaml

# Inspect available experiments
kubectl get chaosexperiments

# Track results
kubectl get chaosresult
kubectl get chaosengine -n litmus

# Manual faults
kubectl exec -it app-pod -- kill -STOP 1
kubectl exec -it app-pod -- tc qdisc add dev eth0 root netem loss 20%
kubectl delete pod myapp --grace-period=0 --force
kubectl drain node-a --ignore-daemonsets
```

## Best Practices

- Run chaos in staging first, then carefully in prod
- Automate experiments into a pipeline with verdicts
- Monitor steady state throughout; abort on threshold breach
- Start with safe faults: network delay, then packet loss, then kill
- Pair each experiment with an alert so downtime is visible
- Clean up experiments; never leave faults running

## Capabilities

### litmus-chaos
Run chaos experiments on Kubernetes.

**Parameters:**
- `experiment` (string): Chaos experiment name
- `target` (string): Target workload

**Commands:**
- `kubectl apply -f https://litmuschaos.github.io/litmus/litmus-operator-v2.14.0.yaml`
- `kubectl get chaosexperiments`
- `litmusctl connect --agent-type cluster`
- `kubectl apply -f experiment.yaml`
- `kubectl get chaosresult`

**Examples:**
- kubectl get chaosengine -n litmus
- kubectl get chaosresult -n litmus -o jsonpath="{.items[*].status.experimentStatus.verdict}"
- litmusctl create agent --agent-type cluster

### fault-injection
Inject network and resource faults.

**Parameters:**
- `pod` (string): Target pod
- `fault` (string): delay, loss, kill, scale

**Commands:**
- `kubectl run net-test --image=alpine -- sleep 3600`
- `kubectl exec -it pod-test -- tc qdisc add dev eth0 root netem loss 20%`
- `kubectl exec -it pod-test -- kill -STOP 1`
- `kubectl delete pod myapp --grace-period=0 --force`

**Examples:**
- kubectl exec -it app-pod -- tc qdisc add dev eth0 root netem delay 500ms
- kubectl scale deploy myapp --replicas=0
- kubectl drain node-a --ignore-daemonsets

## References
- [LitmusChaos Docs](https://docs.litmuschaos.io)
- [Principles of Chaos Engineering](https://principlesofchaos.org)
