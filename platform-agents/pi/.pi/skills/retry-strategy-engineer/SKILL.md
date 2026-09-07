---
name: "retry-strategy-engineer"
description: "Engineers retry policies: curl retry flags, exponential backoff, jitter, and network fault injection with tc-netem. Use when working with curl retry, netem or when the user mentions curl retry, netem."
license: "MIT"
compatibility: "Requires node.js, python, redis, resilience4j, tenacity, retry. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "backend"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(tc:*)"
---

Engineers retry policies: curl retry flags, exponential backoff, jitter, and network fault injection with tc-netem.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl --retry 5 --retry-delay 2 --retry-all-errors -fsS http:`, `tc qdisc add dev eth0 root netem loss 10%`
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

# Retry Strategy

Retry correctly: enough to survive blips, not so much you amplify failures.

## When to Use

- Service calls with transient failures
- CI flakiness reduction
- Testing resilience under packet loss

## curl retries

```bash
curl --retry 5 --retry-delay 2 --retry-all-errors -fsS https://api.example.com/healthz
```

- `--retry` = max attempts after the first.
- `--retry-all-errors` retries 4xx/5xx too - use selectively.
- `--retry-max-time` bounds total retry duration.

## Backoff + jitter

- Exponential: 1s, 2s, 4s, 8s...
- Add jitter to break synchronized retry storms.
- Cap the maximum backoff (e.g. 30s).

## Fault injection

```bash
tc qdisc add dev eth0 root netem loss 10% delay 100ms
tc qdisc change dev eth0 root netem loss 30%
tc qdisc del dev eth0 root
```

## Anti-patterns

- Infinite retries on non-idempotent writes.
- Same fixed delay for every client (thundering herd).
- Retrying without checking for duplicate effects.

## Best practices

- Retry only idempotent or dedupable operations.
- Set a circuit breaker: stop retrying after consecutive failures.
- Log retry counts; high retry rate is a signal.
- Test with netem in staging before incidents hit prod.

## Testing

Inject 10-30% loss, verify recovery within the retry budget, then remove the qdisc.

## Capabilities

### curl-retry
Test and apply curl-level retry policies.

**Parameters:**
- `retry` (number): Max retry count
- `retry-delay` (number): Delay between retries
- `retry-all-errors` (string): Retry on 4xx/5xx and transport errors

**Commands:**
- `curl --retry 5 --retry-delay 2 --retry-all-errors -fsS http://localhost:8080/healthz`
- `curl --retry 3 --retry-connrefused --retry-delay 1 http://service:8080/`
- `curl --retry 5 --retry-delay 3 --retry-max-time 60 http://localhost:8080/data`
- `curl -w '%{http_code} %{num_retries}\n' --retry 3 --retry-all-errors -o /dev/null http://service:8080/`
- `curl --retry 2 --retry-all-errors --max-time 5 http://localhost:8080/`

**Examples:**
- curl --retry 5 --retry-delay 2 --retry-all-errors -fsS http://localhost:8080/healthz
- curl --retry 3 --retry-connrefused -s -o /dev/null -w '%{http_code} %{num_retries}\n' http://service:8080/
- curl --retry-max-time 30 --retry 4 --retry-delay 1 http://localhost:8080/upload

### netem
Inject network faults to test resilience.

**Parameters:**
- `device` (string): Network device
- `loss` (number): Packet loss percentage
- `delay` (string): Latency and jitter

**Commands:**
- `tc qdisc add dev eth0 root netem loss 10%`
- `tc qdisc add dev eth0 root netem delay 100ms 20ms distribution normal`
- `tc qdisc change dev eth0 root netem loss 30% delay 200ms`
- `tc qdisc del dev eth0 root`
- `tc qdisc show dev eth0`

**Examples:**
- tc qdisc add dev eth0 root netem loss 10% delay 100ms
- tc qdisc change dev eth0 root netem loss 50%
- tc qdisc del dev eth0 root && tc qdisc show dev eth0

## References
- [curl --retry](https://curl.se/docs/manpage.html#--retry)
- [tc-netem](https://man7.org/linux/man-pages/man8/tc-netem.8.html)
- [AWS retry guide](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/retries.html)
