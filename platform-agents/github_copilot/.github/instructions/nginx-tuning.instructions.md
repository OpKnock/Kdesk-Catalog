---
applyTo: "**/*.css **/*.json **/*.r **/*.sh"
---

Optimizes nginx for production with worker process sizing, keepalive tuning, kernel parameter adjustments, gzip compression, and load testing validation with ab.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `nginx -t`
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

# nginx Tuning

Tune nginx and the OS so a single box handles maximum concurrent connections and throughput.

## What this skill does

- Sizes workers and connection pools
- Tunes kernel networking parameters
- Benchmarks before/after with ab

## When to use

- Capacity planning for high-traffic sites
- 499/502 errors under load

## Real commands

```bash
# Validate and inspect current config
nginx -t
nginx -T
nginx -s reload

# OS-level tuning
sysctl -w net.core.somaxconn=65535
sysctl -w net.ipv4.tcp_fin_timeout=30

# Benchmark
ab -n 10000 -c 100 http://localhost/
ab -n 5000 -c 50 -k http://localhost/api
```

## Recommended config

```nginx
worker_processes auto;
worker_rlimit_nofile 65535;
events {
    worker_connections 4096;
    use epoll;
    multi_accept on;
}
http {
    keepalive_timeout 65;
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    gzip on;
    gzip_types text/css application/json;
}
```

## Benchmark interpretation

- Requests/sec and time per request from ab
- Re-run after each change to measure impact

## Best practices

- Match worker_processes to CPU cores
- Raise `ulimit -n` and file descriptor limits
- Test one variable at a time

## Capabilities

### nginx-performance-tuning
Optimize nginx core settings and kernel parameters, then benchmark with ab.

**Parameters:**
- `workers` (integer): worker_processes value
- `connections` (integer): worker_connections value
- `url` (string): URL for load testing

**Commands:**
- `nginx -t`
- `nginx -s reload`
- `nginx -T`
- `sysctl -w net.core.somaxconn=65535`
- `ab -n 10000 -c 100 http://localhost/`

**Examples:**
- nginx -T | grep -E 'worker_processes|worker_connections'
- sysctl -w net.ipv4.tcp_fin_timeout=30
- ab -n 5000 -c 50 -k http://localhost/api

## References
- [nginx Core Module](https://nginx.org/en/docs/http/ngx_http_core_module.html)
- [nginx Tuning Guide](https://www.nginx.com/blog/tuning-nginx/)
