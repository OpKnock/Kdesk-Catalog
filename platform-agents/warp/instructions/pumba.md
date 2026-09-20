# Pumba

Inject container-level chaos with Pumba: kill, pause, network emulation, and CPU/memory stress to validate resilience.

## Instructions

# Pumba

Pumba injects chaos into Docker containers: kill them, pause them, damage their network, or stress their resources.

## What this skill does

- Kills and pauses containers for failover tests
- Emulates network loss/delay with netem
- Stresses CPU/memory

## When to use

- Resilience testing in dev/staging
- Validating Kubernetes self-healing

## Real commands

```bash
# Kill
pumba kill --signal SIGKILL docker://web-container
pumba kill --signal SIGTERM docker://web-1

# Pause
pumba pause --duration 60s docker://db-container
pumba pause --duration 45s --regex '^svc' docker

# Network chaos
pumba netem --duration 30s loss --percent 100 docker://api-container
pumba netem --duration 20s delay --time 500 docker://api-container
pumba netem --duration 30s delay --time 1000 --jitter 200 docker://api-1

# Resource stress
pumba stress --duration 60s --cpu 2 docker://app-container
```

## Targeting

- `docker://name` exact match
- `--regex '^svc'` match many containers

## Best practices

- Run pumba in a dedicated chaos namespace
- Pair with monitoring to prove detection works
- Always scope chaos to staging first

## Capabilities

### pumba-chaos-actions
Inject chaos into containers: kill, pause, network emulation and resource stress.

**Commands:**
- `pumba kill --signal SIGKILL docker://web-container`
- `pumba pause --duration 60s docker://db-container`
- `pumba netem --duration 30s loss --percent 100 docker://api-container`
- `pumba netem --duration 20s delay --time 500 docker://api-container`
- `pumba stress --duration 60s --cpu 2 docker://app-container`

**Examples:**
- pumba kill --signal SIGTERM docker://web-1
- pumba netem --duration 30s delay --time 1000 --jitter 200 docker://api-1
- pumba pause --duration 45s --regex '^svc' docker
