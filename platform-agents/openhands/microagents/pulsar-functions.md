---
name: "pulsar-functions"
description: "Pulsar Functions: create, deploy, trigger and manage lightweight stream processors."
type: knowledge
triggers: ["pulsar-functions", "pulsar-functions-operations"]
---

# Pulsar Functions

Pulsar Functions: create, deploy, trigger and manage lightweight stream processors.

## Instructions

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
