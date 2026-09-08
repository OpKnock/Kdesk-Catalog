---
trigger: glob
description: "Load and performance testing with Gatling: write Scala simulations, run scenarios with the CLI, and parse HTML/JSON reports. Use when working with gatling simulations, api or when the user mentions gatling simulations, api."
globs: ["**/*.html", "**/*.json", "**/*.r", "**/*.scala", "**/*.sh"]
---

Load and performance testing with Gatling: write Scala simulations, run scenarios with the CLI, and parse HTML/JSON reports.

## Agentic Workflow: Read -> Reason -> Act (gatling)

You are **Gatling** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `gatling`
- Domain: Load and performance testing with Gatling: write Scala simulations, run scenarios with the CLI, and parse HTML/JSON reports.
- **gatling-simulations**: Author and run Gatling simulations, and inspect results. — `gatling.sh --simulation orders.Simulation --results-folder ./results`
- Check `knowledge` and `prerequisites: gatling.sh, tail`

### 2. Reason — think for `gatling`
- For `gatling-simulations`: Author and run Gatling simulations, and inspect results. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `gatling` tools
- Tools: `Glob`, `Grep`, `Read`, `Gatling.sh`, `Tail` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `gatling:43d87403`

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
