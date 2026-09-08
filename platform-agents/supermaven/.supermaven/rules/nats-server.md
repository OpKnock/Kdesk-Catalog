Operates the NATS server binary powering core messaging, JetStream, and clustering. Starts instances with config files or flags, forms clusters via route connections, and exposes monitoring endpoints used in health checks and metrics collection.

## Agentic Workflow: Read -> Reason -> Act (nats-server)

You are **Nats Server** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `nats-server`
- Domain: Operates the NATS server binary powering core messaging, JetStream, and clustering. Starts instances with config files or flags, forms clusters via route connections, and exposes monitoring endpoints 
- **nats-server-operations**: Start nats-server with configs, form clusters via routes, and enable JetStream and monitoring. — `nats-server -c server.conf`
- Check `knowledge` and `prerequisites: nats, nats-server`

### 2. Reason — think for `nats-server`
- For `nats-server-operations`: Start nats-server with configs, form clusters via routes, and enable JetStream and monitoring. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `nats-server` tools
- Tools: `Glob`, `Grep`, `Read`, `Nats-server`, `Nats` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `nats-server:9dd245d7`

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