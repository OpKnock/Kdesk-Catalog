---
name: "Nats Server"
description: "Operates the NATS server binary powering core messaging, JetStream, and clustering. Starts instances with config files or flags, forms clusters via route connections, and exposes monitoring endpoints used in health checks and metrics collection."
globs: ["**/*.r", "**/*.sh"]
alwaysApply: false
---

# Nats Server

Operates the NATS server binary powering core messaging, JetStream, and clustering. Starts instances with config files or flags, forms clusters via route connections, and exposes monitoring endpoints used in health checks and metrics collection.

## Instructions

# NATS Server

The nats-server is the single binary that powers core NATS, JetStream and clustering.

## What this skill does

- Starts servers with config files or flags
- Forms clusters with route connections
- Exposes monitoring endpoints and health checks

## When to use

- Standing up a NATS cluster
- Tuning server resources and limits
- Enabling JetStream on an existing deployment

## Real commands

```bash
# Run with config
nats-server -c server.conf

# JetStream on
nats-server -js -p 4222

# Cluster member
nats-server -p 4222 -cluster nats://0.0.0.0:6222 -routes nats://seed:6222

# Monitoring + debug verbosity
nats-server -m 8222 -DV

# Health check from CLI
nats server check -i nats://localhost:4222
```

## Monitoring

```bash
curl -s http://localhost:8222/varz
curl -s http://localhost:8222/connz
curl -s http://localhost:8222/healthz
```

## cluster.conf snippet

```conf
cluster {
  name: prod
  listen: 0.0.0.0:6222
  routes: [ nats://node1:6222, nats://node2:6222 ]
}
jetstream { store_dir: /var/lib/nats }
```

## Best practices

- Run 3+ cluster nodes with routes to each other
- Keep monitoring endpoints behind auth or a private net
- Set memory/store limits for JetStream in config

## Capabilities

### nats-server-operations
Start nats-server with configs, form clusters via routes, and enable JetStream and monitoring.

**Commands:**
- `nats-server -c server.conf`
- `nats-server -js -p 4222`
- `nats-server -p 4222 -cluster nats://0.0.0.0:6222 -routes nats://seed:6222`
- `nats-server -m 8222 -DV`
- `nats server check -i nats://localhost:4222`

**Examples:**
- nats-server --tls --tlscert server.crt --tlskey server.key -p 4222
- nats-server -c cluster.conf
- curl -s http://localhost:8222/varz