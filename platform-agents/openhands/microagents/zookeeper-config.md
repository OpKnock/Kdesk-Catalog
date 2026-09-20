---
name: "zookeeper-config"
description: "Use ZooKeeper as a distributed configuration store: create and update ZNodes with zkCli, read config at startup, and subscribe to changes with watches."
type: knowledge
triggers: ["zookeeper-config", "zk-config"]
---

# ZooKeeper Config

Use ZooKeeper as a distributed configuration store: create and update ZNodes with zkCli, read config at startup, and subscribe to changes with watches.

## Instructions

# ZooKeeper Config

## What this skill does
Use ZooKeeper as a distributed configuration store: create and update ZNodes with zkCli, read config at startup, and subscribe to changes with watches.

## When to use
- Coordinating config across many API instances
- Feature flags that need live updates
- Service discovery registration

## Real commands
```bash
# Connect to an ensemble
zkCli.sh -server localhost:2181

# Create a config node
zkCli.sh create /config/app '{"port":8080}'

# Read config
zkCli.sh get /config/app

# Read with stat (version for optimistic updates)
zkCli.sh get -s /config/app

# Update config (all clients with watches get notified)
zkCli.sh set /config/app '{"port":9090}'

# List children
zkCli.sh ls /config

# Delete recursively
zkCli.sh deleteall /config/app
```

## Ephemeral nodes for discovery
```bash
# Ephemeral node: vanishes when the session dies
zkCli.sh create -e /services/orders/instance-1 '192.168.0.5:8080'
```

## Client pattern
```
1. Connect to the ensemble
2. Read /config/app at startup
3. Set a watch on the node
4. On NodeDataChanged, re-read and hot-reload
```

## Best practices
- Keep config under a dedicated root (e.g. /config)
- Store JSON; validate before applying
- Use `get -s` to check version for CAS-style updates
- Never store secrets: use a vault instead
- Prefer ephemeral+sequential nodes for discovery

## Testing
```bash
zkCli.sh create /config/app '{"port":8080}'
zkCli.sh get /config/app
zkCli.sh set /config/app '{"port":9090}'
zkCli.sh get /config/app
```

## Capabilities

### zk-config
Read, write, and watch configuration in ZooKeeper

**Commands:**
- `zkCli.sh -server localhost:2181`
- `zkCli.sh create /config/app '{"port":8080}'`
- `zkCli.sh get /config/app`
- `zkCli.sh set /config/app '{"port":9090}'`
- `zkCli.sh ls /config`

**Examples:**
- zkCli.sh -server zk1:2181,zk2:2181,zk3:2181 create /config/feature-flags '{"newUi":true}'
- zkCli.sh get -s /config/app
- zkCli.sh deleteall /config/app
