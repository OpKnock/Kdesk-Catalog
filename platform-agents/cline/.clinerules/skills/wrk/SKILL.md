---
name: "wrk"
description: "Benchmark HTTP APIs with wrk, a lightweight multi-threaded HTTP load generator. Tune threads and connections, script requests with Lua, read latency distributions, and run repeatable benchmarks in CI."
---

# Wrk

Benchmark HTTP APIs with wrk, a lightweight multi-threaded HTTP load generator. Tune threads and connections, script requests with Lua, read latency distributions, and run repeatable benchmarks in CI.

## Instructions

# wrk

## What this skill does
Benchmark HTTP APIs with wrk, a lightweight multi-threaded HTTP load generator. Tune threads and connections, script requests with Lua, read latency distributions, and run repeatable benchmarks in CI.

## When to use
- Measuring throughput and latency
- Comparing config changes A/B
- Capacity planning

## Real commands
```bash
# Default benchmark
wrk -t12 -c400 -d30s http://localhost:8080/api/users

# Latency distribution
wrk -t4 -c100 -d60s --latency http://localhost:8080/api/users

# Lua-scripted POSTs
wrk -t2 -c50 -d10s -s post.lua http://localhost:8080/api/orders

# With auth header
wrk -H 'Authorization: Bearer token123' -d30s --latency https://httpbin.org/get

# Fixed request rate (throughput mode)
wrk -t8 -c200 -d120s -R 1000 http://localhost:8080/api/search
```

## post.lua
```lua
wrk.method = "POST"
wrk.headers["Content-Type"] = "application/json"
wrk.body = '{"customer": 1}'
```

## Interpreting output
```
Thread Stats   Avg      Stdev     Max   +/- Stdev
  Latency     12.5ms    8.0ms   200ms   90.00%
  Req/Sec      4.5k    300.0     5.5k    75.00%
Latency Distribution
  50%  10.0ms
  99%  90.0ms
```

## Best practices
- Match thread count to CPU cores (2-4x)
- Keep connections below fd limits (check `ulimit -n`)
- Warm up before timed runs
- Use `-R` for fixed-rate tests, default for max-rate

## Testing
```bash
wrk -t4 -c100 -d10s --latency http://localhost:8080/api/health | grep -E 'Requests/sec|99%'
```

## Capabilities

### wrk-benchmark
Run and interpret wrk HTTP benchmarks

**Commands:**
- `wrk -t12 -c400 -d30s http://localhost:8080/api/users`
- `wrk -t4 -c100 -d60s --latency http://localhost:8080/api/users`
- `wrk -t2 -c50 -d10s -s post.lua http://localhost:8080/api/orders`
- `wrk -H 'Authorization: Bearer token123' -d30s --latency https://httpbin.org/get`
- `wrk -t8 -c200 -d120s -R 1000 http://localhost:8080/api/search`

**Examples:**
- wrk -t4 -c200 -d30s --latency http://localhost:8080/api/health | grep -E 'Requests/sec|p99'
- wrk -t2 -c20 -d15s -s upload.lua http://localhost:8080/api/files
- wrk -t12 -c400 -d60s -R 2000 --latency https://httpbin.org/get
