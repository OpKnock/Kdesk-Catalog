---
name: "fault-injection"
description: "Chaos engineering for API resilience: inject network latency and aborts via Istio VirtualService, run Chaos Mesh pod/network/stress experiments on Kubernetes, and use Toxiproxy for proxy-level fault simulation to validate retry and fallback behavior before production. Use when working with chaos experiments, api or when the user mentions chaos experiments, api."
license: "MIT"
compatibility: "Requires docker, kubectl. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(docker:*) Bash(kubectl:*)"
---

Chaos engineering for API resilience: inject network latency and aborts via Istio VirtualService, run Chaos Mesh pod/network/stress experiments on Kubernetes, and use Toxiproxy for proxy-level fault simulation to validate retry and fallback behavior before production.

## Agentic Workflow: Read -> Reason -> Act (fault-injection)

You are **Fault Injection** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `fault-injection`
- Domain: Chaos engineering for API resilience: inject network latency and aborts via Istio VirtualService, run Chaos Mesh pod/network/stress experiments on Kubernetes, and use Toxiproxy for proxy-level fault s
- **chaos-experiments**: Inject faults at proxy, mesh, and node level, then verify application resilience. — `kubectl apply -f fault-injection.yaml`
- Check `knowledge` and `prerequisites: docker, kubectl`

### 2. Reason — think for `fault-injection`
- For `chaos-experiments`: Inject faults at proxy, mesh, and node level, then verify application resilience. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `fault-injection` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `fault-injection:2bc13fb2`

# Fault Injection

## What this skill does

Fault injection deliberately breaks parts of the system to prove resilience: Istio delays/aborts HTTP traffic, Chaos Mesh kills pods or saturates IO, and toxiproxy simulates proxy-level failures. The goal is finding weaknesses before customers do.

## When to use

- Validating retries and fallbacks actually work
- Testing degraded-mode behavior before launch
- Game-day exercises for on-call

## Real commands

```bash
# Istio: delay 2s on 50% of requests to reviews
kubectl apply -f fault-injection.yaml
kubectl get virtualservice reviews -o yaml | grep -A5 fault

# Chaos Mesh: kill 20% of pods for 1 minute
kubectl apply -f chaos-mesh-experiment.yaml
kubectl get chaosexperiments -n chaos-mesh

# Toxiproxy: run and add a proxy
 docker run -d -p 8474:8474 shopify/toxiproxy
curl -s -X POST localhost:8474/proxies -d '{"name":"db","listen":"0.0.0.0:5433","upstream":"db:5432"}'
```

## Istio fault injection example

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: reviews
spec:
  hosts:
    - reviews
  http:
    - fault:
        delay:
          percentage:
            value: 50
          fixedDelay: 2s
      route:
        - destination:
            host: reviews
```

## Safe experiment checklist

- Start in staging; 5-10% blast radius.
- Set a hard end time for every experiment.
- Verify monitoring covers the injected failure before running.
- Roll back via kubectl delete -f <experiment> immediately if impact surprises.

## Testing

```bash
# During the delay injection, watch client behavior
curl -s -o /dev/null -w '%{http_code} %{time_total}s\n' http://gateway.example/reviews
```

## Best practices

- Run experiments during low traffic windows first.
- Tie experiments to a specific hypothesis (e.g. "retry 3x survives 2s delays").
- Automate with a game-day schedule; never run ad hoc in prod.

## Capabilities

### chaos-experiments
Inject faults at proxy, mesh, and node level, then verify application resilience.

**Parameters:**
- `fault-type` (string): delay, abort, or packet-loss
- `target` (string): Service or pod targeted by the experiment
- `duration` (string): Fault duration like 30s or 5m

**Commands:**
- `kubectl apply -f fault-injection.yaml`
- `kubectl get virtualservice reviews -o yaml | grep -A5 fault`
- `kubectl apply -f chaos-mesh-experiment.yaml`
- `kubectl get chaosexperiments -n chaos-mesh`
- `docker run -d -p 8474:8474 shopify/toxiproxy`
- `curl -s -X POST localhost:8474/proxies -d '{"name":"db","listen":"0.0.0.0:5433","upstream":"db:5432"}'`

**Examples:**
- kubectl apply -f fault-injection.yaml && kubectl get virtualservice reviews -o yaml | grep -A5 fault
- curl -s -X POST localhost:8474/proxies -d '{"name":"db","listen":"0.0.0.0:5433","upstream":"db:5432"}'
- kubectl get chaosexperiments -n chaos-mesh

## References
- [Istio Fault Injection](https://istio.io/latest/docs/tasks/traffic-management/fault-injection/)
- [Chaos Mesh docs](https://chaos-mesh.org/docs/)
