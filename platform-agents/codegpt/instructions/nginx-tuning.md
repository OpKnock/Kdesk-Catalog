# Nginx Tuning

Optimizes nginx for production with worker process sizing, keepalive tuning, kernel parameter adjustments, gzip compression, and load testing validation with ab.

## Instructions

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
