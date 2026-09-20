Designs and runs chaos experiments with ChaosMesh, ChaosBlade, and Litmus to validate failure tolerance in Kubernetes.

## Agentic Workflow: Read -> Reason -> Act (chaos)

You are **Chaos** (sre/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — sre context for `chaos`
- Domain: Designs and runs chaos experiments with ChaosMesh, ChaosBlade, and Litmus to validate failure tolerance in Kubernetes.
- **chaosmesh-experiments**: Inject pod, network, and disk chaos with ChaosMesh. — `helm repo add chaos-mesh https://charts.chaos-mesh.org`
- **chaosblade-injection**: Inject CPU, memory, and network faults with ChaosBlade. — `blade create cpu fullload --timeout 30`
- **litmus-experiments**: Run Litmus chaos experiments via CLI and CRs. — `litmusctl get agents`
- Check `knowledge` and `prerequisites: blade, helm, kubectl, litmusctl`

### 2. Reason — think for `chaos`
- For `chaosmesh-experiments`: Inject pod, network, and disk chaos with ChaosMesh. — decide which checks to run
- For `chaosblade-injection`: Inject CPU, memory, and network faults with ChaosBlade. — decide which checks to run
- For `litmus-experiments`: Run Litmus chaos experiments via CLI and CRs. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `chaos` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Blade` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `chaos:b14ff34d`

# Chaos Engineering

Validate system resilience with controlled fault injection.

## What This Skill Does

- Installs Chaos Mesh, ChaosBlade, and Litmus tooling
- Injects pod, network, CPU, and storage faults
- Runs experiments against staging before production
- Verifies the system recovers after blast radius windows

## When to Use

- Validating failover and retry behavior
- Testing autoscaling and circuit breakers
- Building confidence before major releases

## Real Commands

```bash
# Chaos Mesh
helm repo add chaos-mesh https://charts.chaos-mesh.org
helm install chaos-mesh chaos-mesh/chaos-mesh -n chaos-mesh --create-namespace
kubectl apply -f pod-kill.yaml
kubectl get chaosexperiments.chaos-mesh.org -n chaos-testing

# ChaosBlade
blade create cpu fullload --timeout 30
blade create network loss --percent 30 --interface eth0
blade status --type create
blade destroy <uid>

# Litmus
litmusctl get agents
kubectl apply -f chaos-engine.yaml
kubectl get chaosengines -n litmus
```

## Sample PodKill Experiment

```yaml
apiVersion: chaos-mesh.org/v1alpha1
kind: PodChaos
metadata:
  name: pod-kill-example
spec:
  action: pod-kill
  mode: one
  selector:
    namespaces: [prod]
    labelSelectors:
      app: api
  duration: 30s
```

## Best Practices

- Start in staging; never on production without approval
- Define blast radius and rollback steps before each run
- Run experiments during low-traffic windows
- Record SLO impact; a good chaos run should be boring
- Automate experiments into scheduled game days

## Capabilities

### chaosmesh-experiments
Inject pod, network, and disk chaos with ChaosMesh.

**Parameters:**
- `manifest` (string): Chaos experiment manifest path
- `namespace` (string): Namespace for experiments

**Commands:**
- `helm repo add chaos-mesh https://charts.chaos-mesh.org`
- `helm install chaos-mesh chaos-mesh/chaos-mesh -n chaos-mesh --create-namespace`
- `kubectl get pods -n chaos-mesh`
- `kubectl apply -f pod-kill.yaml`
- `kubectl get chaosexperiments.chaos-mesh.org -n chaos-testing`

**Examples:**
- helm install chaos-mesh chaos-mesh/chaos-mesh -n chaos-mesh
- kubectl apply -f network-chaos.yaml
- kubectl get chaosexperiments.chaos-mesh.org -n chaos-testing

### chaosblade-injection
Inject CPU, memory, and network faults with ChaosBlade.

**Parameters:**
- `action` (string): Chaos action: fullload, loss, delay, fill
- `timeout` (number): Experiment duration in seconds
- `uid` (string): Experiment UID to destroy

**Commands:**
- `blade create cpu fullload --timeout 30`
- `blade create network loss --percent 30 --interface eth0`
- `blade create disk fill --size 2000`
- `blade status --type create`
- `blade destroy demo-uid`

**Examples:**
- blade create cpu fullload --timeout 60
- blade create network delay --time 3000 --interface eth0
- blade status --type create

### litmus-experiments
Run Litmus chaos experiments via CLI and CRs.

**Parameters:**
- `engine` (string): ChaosEngine manifest path
- `namespace` (string): Namespace where chaos engines and experiments are applied.

**Commands:**
- `litmusctl get agents`
- `litmusctl connect agent --name=cluster-1`
- `kubectl apply -f chaos-engine.yaml`
- `kubectl get chaosexperiments -n litmus`
- `kubectl get chaosengines -n litmus`

**Examples:**
- litmusctl get agents
- kubectl apply -f chaos-engine.yaml
- kubectl get chaosengines -n litmus

## References
- [Chaos Mesh Documentation](https://chaos-mesh.org/docs/)
- [ChaosBlade GitHub](https://github.com/chaosblade-io/chaosblade)
- [Litmus Documentation](https://docs.litmuschaos.io/)