---
name: "toxiproxy"
description: "Inject network faults into connections with it. Use when working with toxiproxy faults, api or when the user mentions toxiproxy faults, api."
license: "MIT"
compatibility: "Requires toxiproxy-cli."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(toxiproxy-cli:*)"
---

Inject network faults into connections with it.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `toxiproxy-cli create -l localhost:26379 -u localhost:6379 re`
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
