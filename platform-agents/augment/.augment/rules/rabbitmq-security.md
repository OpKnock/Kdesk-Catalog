---
type: agent_requested
description: "Harden RabbitMQ with least-privilege users, vhost isolation, TLS listeners, and renamed dangerous commands for production readiness. Use when working with rabbitmq security config, api or when the user mentions rabbitmq security config, api."
---

Harden RabbitMQ with least-privilege users, vhost isolation, TLS listeners, and renamed dangerous commands for production readiness.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `rabbitmqctl add_user svc-orders s3cret`
- Check `knowledge` references and prerequisites before proceeding

### 2. Reason
Analyze and plan:
- Compare current state vs desired state (drift, checksums, policy)
- Evaluate trust, compatibility, and risk: use `kdesk trust` and `kdesk doctor` patterns
- Decide: which capabilities/tools are needed, which can be skipped

### 3. Act
Execute with guards:
- Run only `allowed-tools` (see frontmatter); use `safe_path` for writes
- Prefer `Bash` with explicit binaries (`curl`, `kubectl`, `kdesk`) over generic shell
- Record evidence: file paths, checksums, and tool outputs for verification

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