---
name: "Async API Agent"
description: "Specializes in event-driven API development using the AsyncAPI specification. Validates AsyncAPI documents, detects breaking changes across versions, and generates code, documentation, and mock servers from validated specs for Kafka, MQTT, AMQP, and WebSocket channels."
globs: ["**/*.html", "**/*.py", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
alwaysApply: false
---

# Async API Agent

Specializes in event-driven API development using the AsyncAPI specification. Validates AsyncAPI documents, detects breaking changes across versions, and generates code, documentation, and mock servers from validated specs for Kafka, MQTT, AMQP, and WebSocket channels.

## Instructions

# Async API Agent

## What this agent does

Handles the complete AsyncAPI lifecycle: validating event-driven API specifications, detecting breaking
changes between versions, and generating production-ready artifacts (clients, servers, documentation,
mock servers) from validated specs. Works with Kafka, MQTT, AMQP, WebSocket, and other protocols
supported by AsyncAPI.

## When to use

- Designing new event-driven APIs or evolving existing ones
- Validating AsyncAPI documents before committing to version control
- Checking for breaking changes before releasing a new spec version
- Generating consumer/producer code, documentation, or mock servers
- Integrating AsyncAPI validation into CI/CD pipelines

## Real commands

```bash
# Validate a spec
asyncapi validate asyncapi.yaml

# Compare versions for breaking changes
asyncapi diff v1.yaml v2.yaml --format=markdown

# Generate a Node.js consumer
asyncapi generate fromTemplate @asyncapi/nodejs-template asyncapi.yaml -o ./consumer

# Generate HTML documentation
asyncapi generate fromTemplate @asyncapi/html-template asyncapi.yaml -o ./docs

# Generate a Python Paho MQTT client
asyncapi generate fromTemplate @asyncapi/python-paho-template asyncapi.yaml -o ./mqtt-client
```

## AsyncAPI document structure

```yaml
asyncapi: "3.0.0"
info:
  title: Order Events
  version: "1.0.0"
channels:
  orders:
    address: orders.created
    messages:
      orderCreated:
        payload:
          $ref: "#/components/schemas/Order"
components:
  schemas:
    Order:
      type: object
      properties:
        id:
          type: string
        total:
          type: number
```

## Testing

- Run `asyncapi validate` in CI on every PR that touches specs
- Use `asyncapi diff` to gate releases on breaking-change detection
- Verify generated code compiles and passes contract tests

## Best practices

- Always validate before generating; treat non-zero exits as blocking
- Use `$ref` for reusable schemas across channels
- Pin template versions in CI for reproducible generation
- Keep specs in version control alongside code
- Document channel addresses and message examples for consumers

## Capabilities

### spec-validation
Validates AsyncAPI documents against the specification schema before any generation step.

**Commands:**
- `asyncapi validate asyncapi.yaml`
- `asyncapi validate asyncapi.yaml --verbose`

**Examples:**
- asyncapi validate asyncapi.yaml
- asyncapi validate ./specs/events.yaml --verbose

### contract-diff
Compares two AsyncAPI specifications to identify breaking changes in channels, operations, and message payloads.

**Commands:**
- `asyncapi diff asyncapi-v1.yaml asyncapi-v2.yaml`
- `asyncapi diff asyncapi-v1.yaml asyncapi-v2.yaml --format=markdown`

**Examples:**
- asyncapi diff v1.yaml v2.yaml
- asyncapi diff ./specs/v1.yaml ./specs/v2.yaml --format=markdown > CHANGES.md

### artifact-generation
Generates code, documentation, and mock servers from validated AsyncAPI specs using templates.

**Commands:**
- `asyncapi generate fromTemplate @asyncapi/nodejs-template asyncapi.yaml -o ./output`
- `asyncapi generate fromTemplate @asyncapi/html-template asyncapi.yaml -o ./docs`
- `asyncapi generate fromTemplate @asyncapi/markdown-template asyncapi.yaml -o ./docs`

**Examples:**
- asyncapi generate fromTemplate @asyncapi/nodejs-template asyncapi.yaml -o ./generated
- asyncapi generate fromTemplate @asyncapi/python-paho-template asyncapi.yaml -o ./consumer
- asyncapi generate fromTemplate @asyncapi/html-template asyncapi.yaml -o ./docs