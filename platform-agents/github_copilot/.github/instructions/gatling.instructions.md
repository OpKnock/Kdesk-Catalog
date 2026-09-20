---
applyTo: "**/*.html **/*.json **/*.r **/*.scala **/*.sh"
---

Load and performance testing with Gatling: write Scala simulations, run scenarios with the CLI, and parse HTML/JSON reports.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `gatling.sh --simulation orders.Simulation --results-folder .`
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

# Gatling

## What this skill does

Gatling is a Scala-based load testing tool with a code-first DSL. Simulations describe scenarios (users ramping, injecting, asserting); the CLI runs them and renders HTML and JSON reports.

## When to use

- Scripted load tests with assertions in CI
- Ramp/steady-state soak testing
- Comparing build-to-build performance

## Real commands

```bash
# List available simulations
gatling.sh --list

# Run one
 gatling.sh --simulation orders.Simulation --results-folder ./results

# Annotate the run
gatling.sh --run-description 'smoke v1.2.3' --simulation orders.Simulation

# Rebuild a report from a previous run
 gatling.sh --results-folder results --reports-only results/orderapi-20240101
```

## Simulation example

```scala
import io.gatling.core.Predef._
import io.gatling.http.Predef._

class OrdersSimulation extends Simulation {
  val httpConf = http.baseUrl("http://localhost:8080")
  val scn = scenario("Get orders")
    .exec(http("list orders").get("/api/orders").check(status.is(200)))
  setUp(scn.inject(rampUsers(50).during(30.seconds)))
    .assertions(global.responseTime.percentile3.lt(300))
    .protocols(httpConf)
}
```

## Inspecting results

```bash
# Tail the simulation log for request stats
 tail -20 results/orderapi-20240101/simulation.log | grep -E 'request|assert'
# Global stats JSON
jq '.stats' results/orderapi-20240101/js/global_stats.json
```

## Best practices

- Run with assertions so CI fails on regressions.
- Reuse the same base URL via protocol config; vary per environment.
- Use `--run-description` to tag builds for report comparison.
- Keep simulations short in smoke runs; soak separately.
- Store simulation.log and global_stats.json for trend dashboards.

## Capabilities

### gatling-simulations
Author and run Gatling simulations, and inspect results.

**Parameters:**
- `simulation-class` (string): Fully qualified simulation class
- `users` (integer): Number of virtual users
- `duration` (string): Ramp/steady duration in the scenario

**Commands:**
- `gatling.sh --simulation orders.Simulation --results-folder ./results`
- `gatling.sh --list`
- `gatling.sh --run-description 'smoke v1.2.3' --simulation orders.Simulation`
- `gatling.sh --results-folder results --reports-only results/orderapi-20240101`
- `tail -20 results/orderapi-20240101/simulation.log | grep -E 'request|assert'`

**Examples:**
- gatling.sh --simulation orders.Simulation --results-folder ./results
- gatling.sh --list
- gatling.sh --results-folder results --reports-only results/orderapi-20240101

## References
- [Gatling documentation](https://docs.gatling.io/)
- [Gatling CLI reference](https://docs.gatling.io/reference/script/cli/)
