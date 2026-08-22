---
name: "trace-sampling"
description: "Control trace volume with head and tail sampling strategies. Configures OpenTelemetry SDK samplers via environment variables (traceidratio, parentbased_traceidratio, always_on), sets Jaeger probabilistic or rate-limiting sampling, and describes collector-side tail sampling policies that retain errors while dropping successful traces."
---

# Trace Sampling

Control trace volume with head and tail sampling strategies. Configures OpenTelemetry SDK samplers via environment variables (traceidratio, parentbased_traceidratio, always_on), sets Jaeger probabilistic or rate-limiting sampling, and describes collector-side tail sampling policies that retain errors while dropping successful traces.

## Instructions

# Trace Sampling

Hand-crafted skill for controlling trace volume with sampling.

## What this skill does

- Configures SDK head sampling with OTel env vars
- Sets Jaeger probabilistic or rate-limiting sampling
- Describes tail sampling for error-priority retention

## When to use

- Trace volume blows past the backend budget
- Errors must be kept even at low sample rates
- Balancing cost vs debuggability per service

## Real commands

```bash
# Head sampling: keep 10% of traces by trace-id hash
export OTEL_TRACES_SAMPLER=traceidratio OTEL_TRACES_SAMPLER_ARG=0.1

# Parent-based: honor the parent span's decision
export OTEL_TRACES_SAMPLER=parentbased_traceidratio OTEL_TRACES_SAMPLER_ARG=0.25

# Debug: keep everything
export OTEL_TRACES_SAMPLER=always_on

# Jaeger: probabilistic 10%
docker run -p 16686:16686 jaegertracing/all-in-one --sampling.type=probabilistic --sampling.param=0.1

# Jaeger: 10 spans/second per service
docker run -p 16686:16686 jaegertracing/all-in-one --sampling.type=ratelimiting --sampling.param=10

# Ask the agent what it samples
curl -g 'http://localhost:16686/api/sampling?service=api' | jq
```

## Tail sampling (collector)

```yaml
processors:
  tail_sampling:
    decision_wait: 10s
    policies:
      - name: keep-errors
        type: status_code
        status_code: { status_codes: [ERROR] }
      - name: keep-10-percent
        type: probabilistic
        probabilistic: { sampling_percentage: 10 }
```

## Testing

```bash
export OTEL_TRACES_SAMPLER=traceidratio OTEL_TRACES_SAMPLER_ARG=1.0
# run traffic, then lower to 0.1 and compare span counts in Jaeger
```

## Best practices

- Use parent-based samplers in microservices to keep traces complete
- Sample by error status in tail sampling for reliability work
- Record sampler choice in service config for reproducibility

## Capabilities

### sampling-strategy
Configure head and tail trace sampling rates

**Commands:**
- `export OTEL_TRACES_SAMPLER=traceidratio OTEL_TRACES_SAMPLER_ARG=0.1`
- `export OTEL_TRACES_SAMPLER=parentbased_traceidratio OTEL_TRACES_SAMPLER_ARG=0.25`
- `docker run -p 16686:16686 jaegertracing/all-in-one --sampling.type=probabilistic --sampling.param=0.1`
- `curl -g 'http://localhost:16686/api/sampling?service=api' | jq`
- `export OTEL_TRACES_SAMPLER=always_on`

**Examples:**
- export OTEL_TRACES_SAMPLER=traceidratio OTEL_TRACES_SAMPLER_ARG=0.1
- curl -g 'http://localhost:16686/api/sampling?service=api' | jq
- docker run -p 16686:16686 jaegertracing/all-in-one --sampling.type=ratelimiting --sampling.param=10
