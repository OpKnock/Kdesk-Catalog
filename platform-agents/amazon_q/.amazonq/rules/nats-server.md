Operates the NATS server binary powering core messaging, JetStream, and clustering. Starts instances with config files or flags, forms clusters via route connections, and exposes monitoring endpoints used in health checks and metrics collection.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `nats-server -c server.conf`
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

**Parameters:**
- `config` (string): Path to the server config file
- `port` (integer): Client listen port (default 4222)
- `cluster_port` (integer): Cluster route listen port (default 6222)

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

## References
- [NATS Server Configuration](https://docs.nats.io/running-a-nats-service/configuration)
- [NATS Monitoring Endpoints](https://docs.nats.io/running-a-nats-service/nats_admin/monitoring)