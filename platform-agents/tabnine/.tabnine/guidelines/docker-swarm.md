# docker-swarm

Deploys and manages Docker Swarm clusters: services, replicas, secrets, configs, stacks, and rolling updates.

## Instructions

# Docker Swarm Operations

Run a production Docker cluster: services with replicated scheduling, secrets, and rolling updates.

## What This Skill Does

- Bootstraps a swarm (manager quorum + workers)
- Creates services with replicas, publish ports, and constraints
- Deploys entire stacks from compose files
- Rolls out updates with zero-downtime settings
- Manages node availability and drain for maintenance

## When to Use

- Single-host-to-cluster growth on one or few VMs
- Deploying a compose stack without Kubernetes complexity
- Scheduled maintenance on worker nodes

## Real Commands

```bash
# Cluster setup
docker swarm init --advertise-addr 10.0.0.5
docker swarm join-token worker
docker node ls
docker node update --availability drain node2

# Services
docker service create --name web --replicas 3 --publish 80:80 nginx:1.26
docker service scale web=6
docker service ls
docker service ps web

# Updates (zero downtime)
docker service update --image nginx:1.27 web
docker service update --update-order start-first --update-delay 10s web

# Stacks and secrets
docker secret create db_password secrets/db_password.txt
docker stack deploy -c docker-compose.yml prod
docker stack ps prod
```

## Rolling Update Flags

```bash
docker service update   --image nginx:1.27   --update-order start-first   --update-delay 10s   --update-failure-action rollback   web
```

## Best Practices

- Run 3 or 5 managers for Raft quorum; never an even number
- Use `--update-order start-first` for stateful services
- Store credentials with `docker secret create`, not env vars
- Pin node labels and constraints for specialized workloads
- Drain nodes before reboots: `docker node update --availability drain <node>`

## Capabilities

### swarm-cluster
Initialize swarm, join workers and managers, and inspect cluster state.

**Commands:**
- `docker swarm init --advertise-addr 10.0.0.5`
- `docker swarm join-token worker`
- `docker swarm join --token SWMTKN-1-xxx 10.0.0.5:2377`
- `docker node ls`
- `docker node update --availability drain node2`
- `docker swarm leave --force`

**Examples:**
- docker swarm init --advertise-addr 10.0.0.5
- docker node ls
- docker node update --availability drain node2

### services-and-stacks
Create and update services, deploy stacks, and roll out changes safely.

**Commands:**
- `docker service create --name web --replicas 3 --publish 80:80 nginx:1.26`
- `docker service scale web=6`
- `docker service update --image nginx:1.27 web`
- `docker service update --update-order start-first web`
- `docker stack deploy -c docker-compose.yml prod`
- `docker service ls`
- `docker service ps web`

**Examples:**
- docker service create --name web --replicas 3 --publish 80:80 nginx:1.26
- docker stack deploy -c docker-compose.yml prod
- docker service update --image nginx:1.27 web