Chaos test APIs by injecting latency, errors, and network faults with Toxiproxy, then load-testing resilience with vegeta and hey.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `toxiproxy-cli create api -l localhost:8081 -u localhost:8080`, `vegeta attack -targets targets.txt -rate 50 -duration 30s | `
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

# Chaos Testing

Test API resilience by injecting faults through a proxy and measuring behavior under load.

## When to Use

- Verifying circuit breakers and retries trigger correctly
- Measuring p95/p99 latency under injected latency
- Confirming the API degrades gracefully, not fatally

## Setup

```bash
toxiproxy-server &
# or in Docker
docker run -d -p 8474:8474 shopify/toxiproxy
export GOPATH=$(go env GOPATH)
go install github.com/tsenart/vegeta/v12@latest
```

## Proxy and Faults

```bash
toxiproxy-cli create api -l localhost:8081 -u localhost:8080
toxiproxy-cli toxic add -t latency -a latency=500 -a jitter=100 api
toxiproxy-cli list
toxiproxy-cli toxic remove -t latency api
toxiproxy-cli delete api
```

## Load Test

```bash
cat > targets.txt <<EOF
POST http://localhost:8081/api/users
Content-Type: application/json
EOF
vegeta attack -targets targets.txt -rate 50 -duration 30s | vegeta report
hey -n 1000 -c 50 http://localhost:8081/api/users
```

## Interpretation

- Latency 500ms injected: expect p95 to rise ~500ms
- Disconnect toxic: expect errors to spike and circuit breaker to open

## Testing

```bash
# Baseline without faults, then with faults, and compare
vegeta attack -targets targets.txt -rate 50 -duration 30s -output baseline.bin
vegeta report baseline.bin
```

## Best Practices

- Run baseline before injecting faults
- Inject one fault at a time to attribute effects
- Point load at the proxy (8081), not the real API (8080)
- Clean up toxics after each experiment
- Combine with monitoring to correlate spikes

## Capabilities

### fault-injection
Inject latency, bandwith, and error faults on a proxy between client and API using toxiproxy-cli

**Parameters:**
- `toxin_type` (string): latency, bandwidth, disconnect, timeout, or reset_peer
- `latency_ms` (string): Amount of latency to inject in milliseconds

**Commands:**
- `toxiproxy-cli create api -l localhost:8081 -u localhost:8080`
- `toxiproxy-cli toxic add -t latency -a latency=500 -a jitter=100 api`
- `toxiproxy-cli toxic add -t bandwidth -a rate=10 api`
- `toxiproxy-cli toxic add -t disconnect -a toxicity=1 api`

**Examples:**
- toxiproxy-cli create api -l localhost:8081 -u localhost:8080
- toxiproxy-cli toxic add -t latency -a latency=500 -a jitter=100 api
- toxiproxy-cli toxic remove -t latency api

### resilience-load
Generate load against the faulted API and measure error rates and percentiles

**Parameters:**
- `rate` (string): Requests per second for vegeta
- `duration` (string): Test duration such as 30s or 1m

**Commands:**
- `vegeta attack -targets targets.txt -rate 50 -duration 30s | vegeta report`
- `vegeta attack -targets targets.txt -rate 50 -duration 30s -output results.bin && vegeta report -type=json results.bin`
- `hey -n 1000 -c 50 http://localhost:8080/api/users`
- `ab -n 1000 -c 50 http://localhost:8080/api/users`

**Examples:**
- echo "POST http://localhost:8080/api/users" > targets.txt && echo "Content-Type: application/json" >> targets.txt && vegeta attack -targets targets.txt -rate 20 -duration 20s | vegeta report
- hey -n 500 -c 25 http://localhost:8080/api/users
- vegeta attack -targets targets.txt -rate 100 -duration 60s -output results.bin; vegeta report -type=hist[0,100ms,500ms,1s] results.bin

## References
- [Toxiproxy Docs](https://github.com/Shopify/toxiproxy)
- [Vegeta Docs](https://github.com/tsenart/vegeta)