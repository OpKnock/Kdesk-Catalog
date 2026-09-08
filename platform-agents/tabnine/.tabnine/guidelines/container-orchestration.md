Operates container orchestration platforms (Kubernetes, Docker Swarm, Nomad): cluster bootstrap, scheduling, scaling, and health checks.

## Agentic Workflow: Read -> Reason -> Act (container-orchestration)

You are **Container Orchestration** (devops/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devops context for `container-orchestration`
- Domain: Operates container orchestration platforms (Kubernetes, Docker Swarm, Nomad): cluster bootstrap, scheduling, scaling, and health checks.
- **kubernetes-cluster-ops**: Bootstrap and inspect Kubernetes clusters with kubeadm and kubectl. — `kubeadm init --pod-network-cidr=10.244.0.0/16`
- **swarm-and-nomad**: Manage Docker Swarm services and HashiCorp Nomad jobs as alternative orchestrators. — `docker swarm init --advertise-addr 10.0.0.5`
- Check `knowledge` and `prerequisites: docker, kubeadm, kubectl, nomad`

### 2. Reason — think for `container-orchestration`
- For `kubernetes-cluster-ops`: Bootstrap and inspect Kubernetes clusters with kubeadm and kubectl. — decide which checks to run
- For `swarm-and-nomad`: Manage Docker Swarm services and HashiCorp Nomad jobs as alternative orchestrators. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `container-orchestration` tools
- Tools: `Glob`, `Grep`, `Read`, `Kubeadm`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `container-orchestration:cf07c611`

# Container Orchestration

Run and troubleshoot container orchestrators: Kubernetes, Docker Swarm, and HashiCorp Nomad.

## What This Skill Does

- Bootstraps clusters (kubeadm, swarm init, nomad dev agent)
- Schedules workloads: Deployments, services, jobs, allocations
- Scales, updates, and performs rolling operations
- Diagnoses node health and scheduling failures

## When to Use

- Choosing or operating an orchestrator for a workload
- Investigating why a workload is unschedulable or unhealthy
- Migrating between Swarm, Kubernetes, or Nomad

## Real Commands

```bash
# Kubernetes bootstrap
kubeadm init --pod-network-cidr=10.244.0.0/16
kubeadm token create --print-join-command
kubectl cluster-info
kubectl get nodes -o wide
kubectl top node

# Docker Swarm
docker swarm init --advertise-addr 10.0.0.5
docker service create --name web --replicas 3 nginx:alpine
docker service ls
docker node ls
docker stack deploy -c stack.yml app

# Nomad
nomad agent -dev &
nomad job run web.nomad
nomad job status web
nomad alloc logs <alloc-id>
nomad node status
```

## Nomad Job Example

```hcl
job "web" {
  datacenters = ["dc1"]
  group "web" {
    count = 3
    task "nginx" {
      driver = "docker"
      config {
        image = "nginx:alpine"
      }
      resources {
        cpu    = 100
        memory = 128
      }
    }
  }
}
```

## Best Practices

- Use kubeadm's `--print-join-command` for repeatable joins
- Pin CNI and orchestrator versions together
- Set resource requests/limits for every workload
- Drain nodes before maintenance; plan for quorum loss in etcd/swarm managers
- Use stack/job files (declarative) over ad-hoc imperative commands

## Capabilities

### kubernetes-cluster-ops
Bootstrap and inspect Kubernetes clusters with kubeadm and kubectl.

**Parameters:**
- `pod-network-cidr` (string): CIDR for pod network, must match CNI plugin
- `node-name` (string): Node to inspect or drain

**Commands:**
- `kubeadm init --pod-network-cidr=10.244.0.0/16`
- `kubeadm token create --print-join-command`
- `kubectl cluster-info`
- `kubectl get nodes -o wide`
- `kubectl get componentstatuses`
- `kubectl top node`

**Examples:**
- kubeadm init --pod-network-cidr=10.244.0.0/16
- kubectl cluster-info
- kubectl get nodes -o wide

### swarm-and-nomad
Manage Docker Swarm services and HashiCorp Nomad jobs as alternative orchestrators.

**Parameters:**
- `service-name` (string): Swarm service name
- `replicas` (integer): Desired replica count
- `job-file` (string): Nomad HCL job file path

**Commands:**
- `docker swarm init --advertise-addr 10.0.0.5`
- `docker service create --name web --replicas 3 nginx`
- `docker node ls`
- `nomad job run web.nomad`
- `nomad job status web`
- `nomad node status`

**Examples:**
- docker service create --name web --replicas 3 nginx
- nomad job run web.nomad
- nomad node status

## References
- [Kubernetes Concepts](https://kubernetes.io/docs/concepts/overview/)
- [Docker Swarm Documentation](https://docs.docker.com/engine/swarm/)
- [Nomad Documentation](https://developer.hashicorp.com/nomad/docs)