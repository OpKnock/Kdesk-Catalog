---
applyTo: "**/*.py **/*.r **/*.sh **/*.{yaml,yml}"
---

# tilt

Develops Kubernetes apps with Tilt: resource definitions, live reload, Tiltfiles, CI mode, and dashboard workflows.

## Instructions

# Tilt Development Sessions

Spin up Kubernetes dev environments with live reload and a shared dashboard.

## What This Skill Does

- Defines resources in a Tiltfile (build, deploy, probes)
- Runs tilt up with live update (file change -> container update)
- Streams logs and alerts in the dashboard
- Runs headless sessions in CI with tilt ci
- Manages resource triggers and arguments

## When to Use

- Multi-service dev environments on Kubernetes
- Teams wanting a shared dev dashboard
- Live reload workflows (no rebuild for code-only changes)

## Real Commands

```bash
# Dev session
tilt up
tilt up --port 10350
tilt down
tilt args
tilt --watch=false up

# Tiltfile
tilt dump                      # view generated config
tilt dump image                # image build graph
tilt alpha tiltfile-result

# CI and diagnostics
tilt ci                        # run once, fail on errors
tilt doctor
tilt version
tilt alpha trigger api
```

## Tiltfile Sketch

```python
load('ext://restart_process', 'docker_build_with_restart')

docker_build_with_restart('myapp', '.', entrypoint=['node', 'server.js'])
k8s_yaml('k8s/deployment.yaml')
k8s_yaml('k8s/service.yaml')
resource('myapp', port_forwards=['8080:8080'], probes=[http_probe('/health')])
```

## Best Practices

- Use live_update for interpreted languages to skip rebuilds
- Add resource probes so tilt blocks on health, not just container start
- Use tilt ci in PR pipelines for smoke tests
- Keep Tiltfile reviewed like code; it is build config
- Use `tilt args` for environment-specific overrides

## Capabilities

### dev-session
Start dev sessions, watch logs, and manage running resources.

**Commands:**
- `tilt up`
- `tilt up --port 10350`
- `tilt down`
- `tilt args`
- `tilt alpha tiltfile-result`
- `tilt --watch=false up`

**Examples:**
- tilt up
- tilt down
- tilt args

### tiltfile-and-ci
Author Tiltfiles and run sessions headlessly for CI.

**Commands:**
- `tilt ci`
- `tilt dump`
- `tilt dump image`
- `tilt version`
- `tilt alpha trigger demo-resource`
- `tilt doctor`

**Examples:**
- tilt ci
- tilt dump
- tilt doctor
