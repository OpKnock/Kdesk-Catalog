Inject network faults into connections with it.

## Agentic Workflow: Read -> Reason -> Act (toxiproxy)

You are **Toxiproxy** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `toxiproxy`
- Domain: Inject network faults into connections with it.
- **toxiproxy-faults**: Inject network faults into connections with Toxiproxy — `toxiproxy-cli create -l localhost:26379 -u localhost:6379 redis`
- Check `knowledge` and `prerequisites: toxiproxy-cli`

### 2. Reason — think for `toxiproxy`
- For `toxiproxy-faults`: Inject network faults into connections with Toxiproxy — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `toxiproxy` tools
- Tools: `Glob`, `Grep`, `Read`, `Toxiproxy-cli` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `toxiproxy:87307241`

# Toxiproxy

Hand-crafted skill for fault injection with Shopify Toxiproxy.

## What this skill does

- Proxies TCP connections to a target service
- Injects latency, timeouts, bandwidth, and loss mid-stream
- Toggles faults on and off without restarting anything

## When to use

- Testing client retries and timeouts against real sockets
- Chaos drills on databases and caches
- Reproducing network bug reports deterministically

## Real commands

```bash
# Proxy traffic: clients hit 26379, real redis at 6379
toxiproxy-cli create -l localhost:26379 -u localhost:6379 redis
toxiproxy-cli list

# Add 1000ms latency with jitter
toxiproxy-cli toxic add -t latency -a latency=1000 -a jitter=100 redis

# Time out all traffic after 5s
toxiproxy-cli toxic add -t timeout -a timeout=5000 redis

# Limit bandwidth to 50 kbps
toxiproxy-cli toxic add -t bandwidth -a rate=50 redis

# Inspect and clean up
toxiproxy-cli toxic list redis
toxiproxy-cli delete redis
```

## Toxic types

- latency: delay packets
- timeout: stall responses for a duration
- bandwidth: cap throughput
- loss: drop a percentage of packets
- corrupt: corrupt bytes

## Test recipe

```bash
toxiproxy-cli create -l localhost:26379 -u localhost:6379 redis
redis-cli -p 26379 ping          # baseline
toxiproxy-cli toxic add -t latency -a latency=2000 redis
redis-cli -p 26379 ping          # now slow: client must handle it
toxiproxy-cli delete redis
```

## Best practices

- Name proxies after the dependency they represent
- Combine latency with client timeout settings to verify failures
- Clean up proxies in CI teardown steps

## Capabilities

### toxiproxy-faults
Inject network faults into connections with Toxiproxy

**Parameters:**
- `proxy_name` (string): Proxy name, e.g. redis
- `listen` (string): Client-facing listen address
- `upstream` (string): Real service address

**Commands:**
- `toxiproxy-cli create -l localhost:26379 -u localhost:6379 redis`
- `toxiproxy-cli list`
- `toxiproxy-cli toxic add -t latency -a latency=1000 -a jitter=100 redis`
- `toxiproxy-cli toxic add -t timeout -a timeout=5000 redis`
- `toxiproxy-cli toxic list redis`
- `toxiproxy-cli delete redis`

**Examples:**
- toxiproxy-cli create -l localhost:26379 -u localhost:6379 redis
- toxiproxy-cli toxic add -t latency -a latency=1000 -a jitter=100 redis
- toxiproxy-cli toxic add -t bandwidth -a rate=50 redis

## References
- [Toxiproxy repo](https://github.com/Shopify/toxiproxy)
- [Toxiproxy toxic types](https://github.com/Shopify/toxiproxy#toxics)
