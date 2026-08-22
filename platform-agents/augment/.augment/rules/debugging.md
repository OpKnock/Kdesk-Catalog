---
type: agent_requested
description: "Debug applications systematically with interactive debuggers, logging, tracing, and profilers across runtimes."
---

# debugging

Debug applications systematically with interactive debuggers, logging, tracing, and profilers across runtimes.

## Instructions

# Debugging

Find root causes systematically.

## When to Use

- Unexplained errors, hangs, and crashes
- Timing and race condition investigation
- Attaching to a running process without restarting
- Confirming network-level behavior

## Method

1. Reproduce with the smallest input
2. Bisect: recent change, code path, data slice
3. Inspect state at the failure point
4. Form a hypothesis and verify
5. Fix, then add a regression test

## Commands

```bash
# Node
node --inspect-brk server.js

# Python
python -m pdb app.py
python -m pdb -c "break app.py:42" app.py

# Go
dlv debug ./cmd/app
dlv exec ./app -- --config prod.yaml

# Logs and network
tail -f logs/app.log
kubectl logs -f deploy/myapp --tail=100
tcpdump -i any port 8080 -nn
curl -sv http://localhost:8080/api
```

## Best Practices

- Add logging at entry/exit of suspicious functions
- Capture the stack trace before guessing
- Reproduce on the smallest dataset that fails
- Check logs, then network, then state, in that order
- Use -c continue with pdb to reach a breakpoint fast
- Never ship debug prints; replace with proper logging
- Turn every fix into a regression test

## Capabilities

### runtime-debuggers
Attach interactive debuggers in Node, Python, and Go.

**Commands:**
- `node --inspect-brk server.js`
- `python -m pdb app.py`
- `python -m pdb -c continue app.py`
- `dlv debug ./cmd/app`
- `dlv test ./...`

**Examples:**
- node --inspect-brk=0.0.0.0:9229 server.js
- dlv exec ./app -- --config prod.yaml
- python -m pdb -c "break app.py:42" app.py

### tracing-observability
Use logs and traces to isolate faults.

**Commands:**
- `tail -f logs/app.log`
- `kubectl logs -f deploy/myapp --tail=100`
- `tcpdump -i any port 8080 -nn`
- `curl -sv http://localhost:8080/api`
- `ngrep -d any "POST /api"`

**Examples:**
- kubectl logs deploy/myapp -c sidecar --since=10m
- tcpdump -i any -w traffic.pcap port 8080
- curl -sv -X POST http://localhost:8080/api -d "{}"