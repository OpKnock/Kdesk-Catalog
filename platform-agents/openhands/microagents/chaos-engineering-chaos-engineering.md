---
name: "chaos-engineering-chaos-engineering"
description: "Practices chaos engineering with LitmusChaos, Chaos Monkey, and fault injection to verify resilience of distributed systems."
type: knowledge
triggers: ["chaos-engineering-chaos-engineering", "litmus-chaos", "fault-injection"]
---

# chaos-engineering-chaos-engineering

Practices chaos engineering with LitmusChaos, Chaos Monkey, and fault injection to verify resilience of distributed systems.

## Instructions

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

**Commands:**
- `kubectl run net-test --image=alpine -- sleep 3600`
- `kubectl exec -it pod-test -- tc qdisc add dev eth0 root netem loss 20%`
- `kubectl exec -it pod-test -- kill -STOP 1`
- `kubectl delete pod myapp --grace-period=0 --force`

**Examples:**
- kubectl exec -it app-pod -- tc qdisc add dev eth0 root netem delay 500ms
- kubectl scale deploy myapp --replicas=0
- kubectl drain node-a --ignore-daemonsets
