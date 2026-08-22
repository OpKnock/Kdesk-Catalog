# Chaos Toolkit

Design and run repeatable chaos experiments with the Chaos Toolkit CLI, including probes, steady-state checks, and Docker/Kubernetes actions.

## Instructions

# Chaos Toolkit

Run reproducible chaos engineering experiments.

## When to Use

- Automated resilience testing in CI or on schedules
- Validating steady-state hypotheses before and after faults
- Team-wide shareable experiment definitions

## Install

```bash
pip install chaostoolkit chaostoolkit-http chaostoolkit-docker
chaos --help
```

## Experiment Manifest

```json
{
  "version": "1.0.0",
  "title": "API latency under network delay",
  "description": "Inject 100ms latency and verify the API stays healthy",
  "steady-state-hypothesis": {
    "title": "API is healthy",
    "probes": [
      {
        "type": "probe",
        "name": "health-check",
        "provider": {
          "type": "http",
          "url": "http://localhost:8080/health",
          "expected_status": 200
        }
      }
    ]
  },
  "method": [
    {
      "type": "action",
      "name": "add-latency",
      "provider": {
        "type": "process",
        "path": "tc",
        "arguments": "qdisc add dev eth0 root netem delay 100ms"
      }
    }
  ],
  "rollbacks": [
    {
      "type": "action",
      "name": "remove-latency",
      "provider": {
        "type": "process",
        "path": "tc",
        "arguments": "qdisc del dev eth0 root"
      }
    }
  ]
}
```

## Run

```bash
chaos run --dry-run experiment.json
chaos run experiment.json --rollback-strategy always
chaos run experiment.json --hypothesis-strategy before-and-after
```

## Explore

```bash
chaos init
chaos info
```

## Testing

```bash
# Force a probe failure to validate the hypothesis logic
chaos run --hypothesis-strategy after experiment.json
```

## Best Practices

- Always define a steady-state hypothesis
- Always define rollbacks and set --rollback-strategy always
- Run experiments in staging first
- Keep experiments in git with versioned manifests
- Report results from chaos report into CI dashboards
- Start with small blast radius: one pod, one service

## Capabilities

### experiment-run
Create, validate, and run Chaos Toolkit experiments from JSON manifests

**Commands:**
- `chaos init`
- `chaos run experiment.json`
- `chaos run --dry-run experiment.json`
- `chaos --help`

**Examples:**
- chaos init && chaos run --dry-run experiment.json
- chaos run experiments/network-delay.json --rollback-strategy always
- chaos run experiment.json --hypothesis-strategy before-and-after

### extensions
Install Chaos Toolkit extension packages for Docker, Kubernetes, HTTP, and other platforms

**Commands:**
- `pip install chaostoolkit`
- `pip install chaostoolkit-kubernetes`
- `pip install chaostoolkit-docker`
- `pip install chaostoolkit-http`

**Examples:**
- pip install chaostoolkit chaostoolkit-kubernetes
- pip install chaostoolkit-docker chaostoolkit-http
- chaos info