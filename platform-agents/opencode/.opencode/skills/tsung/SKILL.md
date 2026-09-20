---
name: "tsung"
description: "Runs distributed load tests using Tsung's XML scenario engine. Defines multi-phase arrival rates, simulates HTTP/WebSocket/AMQP workloads, aggregates latency and error stats into HTML reports, and scales across multiple load-generator nodes. Use when working with load test, api, load testing, performance or when the user mentions load test, api, load testing, performance."
---

Runs distributed load tests using Tsung's XML scenario engine. Defines multi-phase arrival rates, simulates HTTP/WebSocket/AMQP workloads, aggregates latency and error stats into HTML reports, and scales across multiple load-generator nodes.

## Agentic Workflow: Read -> Reason -> Act (tsung)

You are **Tsung** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `tsung`
- Domain: Runs distributed load tests using Tsung's XML scenario engine. Defines multi-phase arrival rates, simulates HTTP/WebSocket/AMQP workloads, aggregates latency and error stats into HTML reports, and sca
- **load-test**: Define and run Tsung load scenarios — `tsung -f tsung.xml start`
- Check `knowledge` and `prerequisites: tsung`

### 2. Reason — think for `tsung`
- For `load-test`: Define and run Tsung load scenarios — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `tsung` tools
- Tools: `Glob`, `Read`, `Tsung`, `Grep` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `tsung:66452832`

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
