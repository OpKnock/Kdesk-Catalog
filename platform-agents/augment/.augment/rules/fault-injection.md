---
type: agent_requested
description: "Chaos engineering for API resilience: inject network latency and aborts via Istio VirtualService, run Chaos Mesh pod/network/stress experiments on Kubernetes, and use Toxiproxy for proxy-level fault simulation to validate retry and fallback behavior before production."
---

# Fault Injection

Chaos engineering for API resilience: inject network latency and aborts via Istio VirtualService, run Chaos Mesh pod/network/stress experiments on Kubernetes, and use Toxiproxy for proxy-level fault simulation to validate retry and fallback behavior before production.

## Instructions

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