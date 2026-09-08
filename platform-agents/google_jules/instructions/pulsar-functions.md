Pulsar Functions: create, deploy, trigger and manage lightweight stream processors.

## Agentic Workflow: Read -> Reason -> Act (pulsar-functions)

You are **Pulsar Functions** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `pulsar-functions`
- Domain: Pulsar Functions: create, deploy, trigger and manage lightweight stream processors.
- **pulsar-functions-operations**: Deploy and manage Pulsar Functions with pulsar-admin, and trigger them with test inputs. — `bin/pulsar-admin functions create --tenant public --namespace default --name dou`
- Check `knowledge` and `prerequisites: bin/pulsar-admin`

### 2. Reason — think for `pulsar-functions`
- For `pulsar-functions-operations`: Deploy and manage Pulsar Functions with pulsar-admin, and trigger them with test inputs. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `pulsar-functions` tools
- Tools: `Glob`, `Grep`, `Read`, `Bin/pulsar-admin` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `pulsar-functions:5a1d0d82`

# Pulsar Functions

Pulsar Functions are lightweight stream processors that consume from topics and emit to topics.

## What this skill does

- Packages and deploys functions
- Triggers functions with test data
- Monitors instance health

## When to use

- Simple transformations in the stream
- Replacing ad-hoc consumers

## Real commands

```bash
# Deploy
bin/pulsar-admin functions create --tenant public --namespace default \
  --name double-echo --classname org.example.DoubleEcho --jar target/my-fn.jar --inputs my-topic

# List / inspect
bin/pulsar-admin functions list --tenant public --namespace default
bin/pulsar-admin functions status --name double-echo

# Trigger with test value
bin/pulsar-admin functions trigger --name double-echo --trigger-value "hello"

# Remove
bin/pulsar-admin functions delete --tenant public --namespace default --name double-echo
```

## Function skeleton (Java)

```java
public class DoubleEcho implements Function<String, String> {
    public String process(String input, Context ctx) {
        return input + input;
    }
}
```

## Best practices

- Keep functions stateless (or use state storage)
- Use --output for downstream topics
- Trigger with sample payloads before wiring producers

## Capabilities

### pulsar-functions-operations
Deploy and manage Pulsar Functions with pulsar-admin, and trigger them with test inputs.

**Parameters:**
- `name` (string): Function name
- `jar` (string): Function package file
- `inputs` (array): Input topics

**Commands:**
- `bin/pulsar-admin functions create --tenant public --namespace default --name double-echo --classname org.example.DoubleEcho --jar target/my-fn.jar --inputs my-topic`
- `bin/pulsar-admin functions list --tenant public --namespace default`
- `bin/pulsar-admin functions trigger --name double-echo --trigger-value "hello"`
- `bin/pulsar-admin functions status --name double-echo`
- `bin/pulsar-admin functions delete --tenant public --namespace default --name double-echo`

**Examples:**
- bin/pulsar-admin functions create --name counter --classname org.example.Counter --jar counter.jar --inputs events --output counts
- bin/pulsar-admin functions trigger --name counter --trigger-value '{"n":1}'
- bin/pulsar-admin functions status --name counter | jq '.instances[0].status'

## References
- [Pulsar Functions Overview](https://pulsar.apache.org/docs/3.0.x/functions-overview/)
- [pulsar-admin functions](https://pulsar.apache.org/docs/3.0.x/reference-pulsar-admin-functions/)
