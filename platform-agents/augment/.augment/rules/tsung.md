---
type: agent_requested
description: "Runs distributed load tests using Tsung's XML scenario engine. Defines multi-phase arrival rates, simulates HTTP/WebSocket/AMQP workloads, aggregates latency and error stats into HTML reports, and scales across multiple load-generator nodes. Use when working with load test, api, load testing, performance or when the user mentions load test, api, load testing, performance."
---

Runs distributed load tests using Tsung's XML scenario engine. Defines multi-phase arrival rates, simulates HTTP/WebSocket/AMQP workloads, aggregates latency and error stats into HTML reports, and scales across multiple load-generator nodes.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `tsung -f tsung.xml start`
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

# Tsung

Distributed load testing with Tsung.

## What this skill does

- Runs XML-defined load scenarios against services
- Simulates ramping phases and multiple request types
- Aggregates stats into CSV and HTML reports
- Scales across multiple load-generator nodes

## When to use

- Load testing HTTP APIs from the CLI
- WebSocket or AMQP stress scenarios
- Soak runs with scheduled phases

## Real commands

```bash
# Run a scenario
tsung -f tsung.xml start

# With an explicit log directory
tsung -f tsung.xml -l /tmp/tsung-reports start

# Check running status
tsung status

# After the run, inspect the generated report
grep -E 'count.*mean' ~/.tsung/log/tsung.log | tail -20
grep -E 'http_rc|http_mean' ~/.tsung/log/tsung.log | tail -40
ls ~/.tsung/log/*/report.html
```

## Minimal scenario

```xml
<tsung loglevel="notice">
  <clients>
    <client host="localhost" use_controller_vm="true"/>
  </clients>
  <servers>
    <server host="http://localhost:8080" port="80" type="tcp"/>
  </servers>
  <load>
    <arrivalphase phase="1" duration="60" unit="second">
      <users arrivalrate="100" unit="second"/>
    </arrivalphase>
  </load>
  <sessions>
    <session name="health" probability="100">
      <request><http url="/healthz" method="GET"/></request>
    </session>
  </sessions>
</tsung>
```

## Best practices

- Start with one controller node, then add clients for scale
- Use separate sessions per user flow (login, search, checkout)
- Keep arrivalrate below failure onset; that is your ceiling
- Collect report.html into CI artifacts

## Capabilities

### load-test
Define and run Tsung load scenarios

**Parameters:**
- `config` (string): Path to tsung.xml scenario
- `logdir` (string): Report output directory
- `servers` (integer): Number of load generator nodes

**Commands:**
- `tsung -f tsung.xml start`
- `tsung -f tsung.xml -l /tmp/tsung-reports start`
- `tsung status`
- `grep -E "count.*mean" ~/.tsung/log/tsung.log | tail -20`
- `grep -E "http_rc|http_mean" ~/.tsung/log/tsung.log | tail -40`

**Examples:**
- tsung -f tsung.xml start
- tsung -f tsung.xml -l /tmp/tsung-reports start
- grep "session average" ~/.tsung/log/tsung.log | tail -5

## References
- [Tsung user's manual](https://tsung.erlang-projects.org/user_manual/)
- [Tsung benchmark examples](https://tsung.erlang-projects.org/examples/)
- [Tsung clustering guide](https://tsung.erlang-projects.org/user_manual/chapter-clustering.html)