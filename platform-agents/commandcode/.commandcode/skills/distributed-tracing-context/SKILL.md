---
name: "distributed-tracing-context"
description: "Propagates and validates W3C traceparent headers across services using OpenTelemetry Collector, with curl injection and Jaeger query verification."
---

# Distributed Tracing Context

Propagates and validates W3C traceparent headers across services using OpenTelemetry Collector, with curl injection and Jaeger query verification.

## Instructions

# Distributed Tracing Context

## What this skill does

Distributed tracing links logs and spans across services through propagated context. The W3C `traceparent` header carries trace-id, parent span-id, and sampling flags; OpenTelemetry standardizes instrumentation and export.

## When to use

- Correlating a single user request across microservices
- Debugging why a trace appears in the backend but not the gateway
- Setting up the OTel Collector for the first time

## Real commands

```bash
# Validate the collector config and run it
otelcol-contrib --validate --config config.yaml
otelcol-contrib --config config.yaml

# Inject a trace context into a request and confirm the service keeps it
curl -i -H 'traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01' http://localhost:8080/api/orders | grep -i traceparent

# Send a raw OTLP protobuf trace to the collector
curl -X POST http://localhost:4318/v1/traces -H 'Content-Type: application/x-protobuf' --data-binary @trace.pb

# Query traces in Jaeger
jaeger query --jaeger.host 127.0.0.1 --url http://localhost:16686/api/traces --service orders-service
```

## Collector config example

```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318
exporters:
  jaeger:
    endpoint: jaeger:14250
    tls:
      insecure: true
service:
  pipelines:
    traces:
      receivers: [otlp]
      exporters: [jaeger]
```

## Best practices

- Propagate `traceparent` on every outbound HTTP call; never generate a new trace id mid-path.
- Sample at the edge (head sampling) and consider tail sampling for low-volume important traces.
- Include `trace_id` in application logs so logs and traces join up.
- Test propagation with the curl header injection above before adding instrumentation.

## Testing

```bash
# End-to-end check: send a traced request and search Jaeger for the same trace id
curl -i -H 'traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01' http://localhost:8080/api/orders
curl -s 'http://localhost:16686/api/traces?service=orders-service&traceID=4bf92f3577b34da6a3ce929d0e0e4736' | jq '.data[0].spans | length'
```

## Capabilities

### otel-propagation
Run the OpenTelemetry Collector, test trace-context propagation with curl, and export/query traces.

**Commands:**
- `otelcol-contrib --config config.yaml`
- `docker run -p 4317:4317 -p 4318:4318 otel/opentelemetry-collector-contrib --config /etc/otelcol-contrib/config.yaml`
- `curl -i -H 'traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01' http://localhost:8080/api/orders | grep -i traceparent`
- `curl -X POST http://localhost:4318/v1/traces -H 'Content-Type: application/x-protobuf' --data-binary @trace.pb`
- `jaeger query --jaeger.host 127.0.0.1 --jaeger.port 16686 --url http://localhost:16686/api/traces`

**Examples:**
- curl -i -H 'traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01' http://localhost:8080/api/orders
- docker run -p 4317:4317 -p 4318:4318 otel/opentelemetry-collector-contrib --config /etc/otelcol-contrib/config.yaml
- otelcol-contrib --validate --config config.yaml
