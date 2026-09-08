---
name: "Rabbitmq Security"
description: "Harden RabbitMQ with least-privilege users, vhost isolation, TLS listeners, and renamed dangerous commands for production readiness. Use when working with rabbitmq security config, api or when the user mentions rabbitmq security config, api."
globs: ["**/*.r", "**/*.sh"]
alwaysApply: false
---

Harden RabbitMQ with least-privilege users, vhost isolation, TLS listeners, and renamed dangerous commands for production readiness.

## Agentic Workflow: Read -> Reason -> Act (rabbitmq-security)

You are **Rabbitmq Security** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `rabbitmq-security`
- Domain: Harden RabbitMQ with least-privilege users, vhost isolation, TLS listeners, and renamed dangerous commands for production readiness.
- **rabbitmq-security-config**: Manage users, vhosts and permissions, and configure TLS with rabbitmq.conf. — `rabbitmqctl add_user svc-orders s3cret`
- Check `knowledge` and `prerequisites: rabbitmqctl`

### 2. Reason — think for `rabbitmq-security`
- For `rabbitmq-security-config`: Manage users, vhosts and permissions, and configure TLS with rabbitmq.conf. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `rabbitmq-security` tools
- Tools: `Glob`, `Grep`, `Read`, `Rabbitmqctl` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `rabbitmq-security:b6dec6b4`

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

**Parameters:**
- `user` (string): RabbitMQ username
- `vhost` (string): Virtual host
- `permissions` (array): configure, write, read regex patterns

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

## References
- [RabbitMQ Access Control](https://www.rabbitmq.com/access-control.html)
- [TLS for RabbitMQ](https://www.rabbitmq.com/ssl.html)