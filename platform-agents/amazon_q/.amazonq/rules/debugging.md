Debug applications systematically with interactive debuggers, logging, tracing, and profilers across runtimes.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `node --inspect-brk server.js`, `tail -f logs/app.log`
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