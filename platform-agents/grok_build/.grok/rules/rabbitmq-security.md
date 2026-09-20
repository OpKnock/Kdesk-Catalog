# Rabbitmq Security

Harden RabbitMQ with least-privilege users, vhost isolation, TLS listeners, and renamed dangerous commands for production readiness.

## Instructions

# RabbitMQ Security

Restrict who can touch what: users, vhosts, and per-vhost configure/write/read permissions.

## What this skill does

- Creates users and vhosts
- Grants minimal permissions
- Enables TLS

## When to use

- Multi-team brokers
- Compliance requirements

## Real commands

```bash
# Users
rabbitmqctl add_user svc-orders s3cret
rabbitmqctl set_user_tags svc-orders monitoring
rabbitmqctl list_users

# Vhosts
rabbitmqctl add_vhost orders-vhost

# Permissions (configure, write, read)
rabbitmqctl set_permissions -p orders-vhost svc-orders ".*" ".*" ".*"
rabbitmqctl list_permissions -p orders-vhost
rabbitmqctl clear_permissions -p orders-vhost svc-orders
```

## rabbitmq.conf TLS

```conf
listeners.ssl.default = 5671
ssl_options.cacertfile = /etc/rabbitmq/ca.crt
ssl_options.certfile   = /etc/rabbitmq/server.crt
ssl_options.keyfile    = /etc/rabbitmq/server.key
ssl_options.verify     = verify_peer
ssl_options.fail_if_no_peer_cert = true
```

## Best practices

- One user per service; rotate secrets regularly
- Give read-only access where possible
- Use 5671 with client certs for production

## Capabilities

### rabbitmq-security-config
Manage users, vhosts and permissions, and configure TLS with rabbitmq.conf.

**Commands:**
- `rabbitmqctl add_user svc-orders s3cret`
- `rabbitmqctl set_permissions -p orders-vhost svc-orders ".*" ".*" ".*"`
- `rabbitmqctl set_user_tags svc-orders monitoring`
- `rabbitmqctl add_vhost orders-vhost`
- `rabbitmqctl list_permissions -p orders-vhost`

**Examples:**
- rabbitmqctl add_user admin strongpass && rabbitmqctl set_user_tags admin administrator
- rabbitmqctl list_users
- rabbitmqctl clear_permissions -p orders-vhost svc-orders