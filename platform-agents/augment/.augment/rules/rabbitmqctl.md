---
type: agent_requested
description: "Administers RabbitMQ: queues, users, permissions, bindings, and server status via rabbitmqctl."
---

# rabbitmqctl

Administers RabbitMQ: queues, users, permissions, bindings, and server status via rabbitmqctl.

## Instructions

# rabbitmqctl

Administration CLI for RabbitMQ: queues, users, permissions, and cluster status.

## When to Use

- Inspecting queue depth and consumer counts
- Creating users and scoping permissions
- Purging stuck queues

## Real Commands

```bash
# Server status
sudo rabbitmqctl status

# Queues
sudo rabbitmqctl list_queues name messages messages_ready messages_unacknowledged consumers
sudo rabbitmqctl list_queues -p app

# Bindings and exchanges
sudo rabbitmqctl list_bindings -p app
sudo rabbitmqctl list_exchanges -p app name type

# Users and permissions
sudo rabbitmqctl add_user deployer secret123
sudo rabbitmqctl set_permissions -p / deployer ".*" ".*" ".*"
sudo rabbitmqctl list_permissions -p /
sudo rabbitmqctl delete_user deployer

# Connections
sudo rabbitmqctl list_connections state channels peer_host

# Purging
sudo rabbitmqctl purge_queue -p app jobs
```

## Best Practices

- Scope permissions to the vhost and patterns (configure/write/read)
- Use `list_queues` to detect queue growth early
- Purge only queues you can afford to lose; consumers may be mid-processing
- Prefer cluster-wide `rabbitmqctl` on one node for read commands
- Keep credentials out of shell history (env vars)

## Example Response

For stuck messages: reports queue depth, ready vs unacked, and consumer counts,
then recommends purge, consumer fix, or queue redeclare.

## Capabilities

### rabbitmqctl
Manage vhosts, users, queues, and inspect server state

**Commands:**
- `rabbitmqctl status`
- `rabbitmqctl list_queues name messages consumers`
- `rabbitmqctl add_user deployer secret123`
- `rabbitmqctl set_permissions -p / deployer ".*" ".*" ".*"`
- `rabbitmqctl list_queues -p app name messages messages_ready messages_unacknowledged`

**Examples:**
- rabbitmqctl list_bindings -p app
- rabbitmqctl purge_queue -p app jobs
- rabbitmqctl list_connections state channels