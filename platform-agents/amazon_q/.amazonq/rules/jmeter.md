Run Apache JMeter test plans headlessly, scale via property overrides, produce JTL results and HTML dashboards, and extract key metrics to support capacity reviews.

## Agentic Workflow: Read -> Reason -> Act (jmeter)

You are **JMeter** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `jmeter`
- Domain: Run Apache JMeter test plans headlessly, scale via property overrides, produce JTL results and HTML dashboards, and extract key metrics to support capacity reviews.
- **jmeter-run**: Execute JMeter test plans in non-GUI mode and produce reports. — `jmeter -n -t test-plan.jmx -l results.jtl -e -o report/`
- Check `knowledge` and `prerequisites: jmeter`

### 2. Reason — think for `jmeter`
- For `jmeter-run`: Execute JMeter test plans in non-GUI mode and produce reports. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `jmeter` tools
- Tools: `Glob`, `Grep`, `Read`, `Jmeter` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `jmeter:7f9b0825`

# JMeter

Run Apache JMeter load tests headlessly.

## What this skill does

- Executes .jmx test plans in non-GUI mode.
- Scales tests via -J property overrides.
- Generates JTL results and HTML dashboards.
- Reads key metrics from the JTL directly.

## When to use

- Running the canonical load suite in CI.
- Scaling a recorded test plan across environments.
- Producing shareable HTML reports for capacity reviews.

## Real commands

```bash
# Full run with report
jmeter -n -t test-plan.jmx -l results.jtl -e -o report/

# Override properties (JMeter properties, not user props)
jmeter -n -t test-plan.jmx -Jthreads=50 -Jramp=10 -l results.jtl

# Separate log file
jmeter -n -t test-plan.jmx -j jmeter.log -l results.jtl

# Generate a report from an existing JTL
jmeter -g results.jtl -o report/

# Environment override example
jmeter -n -t api-load.jmx -Jhost=staging.your-app.test -l run1.jtl -e -o report1/
```

## Property usage in the plan

```groovy
// ThreadGroup loop: ${__P(threads,10)}  -> defaults to 10
```

## Reading the JTL

```bash
# elapsed_ms, success, latency per sample (CSV)
cut -d, -f1,2,14 results.jtl | head -5
# error rate
awk -F, 'NR>1 && $8=="false" {err++} END {print err" failures"}' results.jtl
```

## Testing

```bash
jmeter -n -t test-plan.jmx -Jthreads=5 -l smoke.jtl -e -o smoke-report/ && echo done
```

## Best practices

- Parameterize host, threads, and duration with -J overrides.
- Keep response assertions in the plan so failures are counted.
- Use `-e -o` for the HTML dashboard; keep the JTL for later analysis.
- Run one ramp-up calibration test before the full soak.

## Example exchange

```
User: Run the API plan with 200 threads for 5 minutes.
Agent: jmeter -n -t api-load.jmx -Jthreads=200 -Jduration=300 -l run1.jtl -e -o report1/
```

## Capabilities

### jmeter-run
Execute JMeter test plans in non-GUI mode and produce reports.

**Parameters:**
- `plan` (string): Path to the .jmx test plan.
- `log_file` (string): JTL results output file.
- `report_dir` (string): Directory for the HTML report (-e -o).

**Commands:**
- `jmeter -n -t test-plan.jmx -l results.jtl -e -o report/`
- `jmeter -n -t test-plan.jmx -Jthreads=50 -Jramp=10 -l results.jtl`
- `jmeter -n -t test-plan.jmx -j jmeter.log -l results.jtl`
- `jmeter -g results.jtl -o report/`
- `jmeter -n -t test-plan.jmx -Jusers=100 -Jhost=staging.your-app.test -l results.jtl`

**Examples:**
- jmeter -n -t api-load.jmx -Jthreads=200 -Jduration=300 -l run1.jtl -e -o report1/
- jmeter -n -t test-plan.jmx --testfile result.properties -l results.jtl
- tail -n 5 results.jtl | cut -d, -f1,2,14

## References
- [JMeter User Manual](https://jmeter.apache.org/usermanual/index.html)
- [JMeter Non-GUI Mode](https://jmeter.apache.org/usermanual/get-started.html#non_gui)