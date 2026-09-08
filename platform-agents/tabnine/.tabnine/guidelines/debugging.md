Debug applications systematically with interactive debuggers, logging, tracing, and profilers across runtimes.

## Agentic Workflow: Read -> Reason -> Act (debugging)

You are **debugging** (code-quality/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — code-quality context for `debugging`
- Domain: Debug applications systematically with interactive debuggers, logging, tracing, and profilers across runtimes.
- **runtime-debuggers**: Attach interactive debuggers in Node, Python, and Go. — `node --inspect-brk server.js`
- **tracing-observability**: Use logs and traces to isolate faults. — `tail -f logs/app.log`
- Check `knowledge` and `prerequisites: dlv, kubectl, ngrep, node`

### 2. Reason — think for `debugging`
- For `runtime-debuggers`: Attach interactive debuggers in Node, Python, and Go. — decide which checks to run
- For `tracing-observability`: Use logs and traces to isolate faults. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `debugging` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Dlv` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `debugging:8ac47b3d`

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

**Parameters:**
- `entry` (string): Entry point
- `breakpoint` (string): file:line breakpoint

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

**Parameters:**
- `target` (string): Service or pod to inspect
- `since` (string): Log window, e.g. 10m

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

## References
- [Node Debugger Docs](https://nodejs.org/api/debugger.html)
- [pdb Docs](https://docs.python.org/3/library/pdb.html)
- [Delve Docs](https://github.com/go-delve/delve)