---
name: "tilt"
description: "Develops Kubernetes apps with Tilt: resource definitions, live reload, Tiltfiles, CI mode, and dashboard workflows. Use when working with dev session, tiltfile and ci, devops or when the user mentions dev session, tiltfile and ci, devops."
globs: ["**/*.py", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
alwaysApply: false
---

Develops Kubernetes apps with Tilt: resource definitions, live reload, Tiltfiles, CI mode, and dashboard workflows.

## Agentic Workflow: Read -> Reason -> Act (tilt)

You are **tilt** (devops/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devops context for `tilt`
- Domain: Develops Kubernetes apps with Tilt: resource definitions, live reload, Tiltfiles, CI mode, and dashboard workflows.
- **dev-session**: Start dev sessions, watch logs, and manage running resources. — `tilt up`
- **tiltfile-and-ci**: Author Tiltfiles and run sessions headlessly for CI. — `tilt ci`
- Check `knowledge` and `prerequisites: tilt`

### 2. Reason — think for `tilt`
- For `dev-session`: Start dev sessions, watch logs, and manage running resources. — decide which checks to run
- For `tiltfile-and-ci`: Author Tiltfiles and run sessions headlessly for CI. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `tilt` tools
- Tools: `Glob`, `Grep`, `Read`, `Tilt` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `tilt:fa5ac84a`

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

**Parameters:**
- `port` (integer): Dashboard port
- `watch` (boolean): Watch file changes

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

**Parameters:**
- `tiltfile` (string): Tiltfile path
- `resource` (string): Resource name for triggers

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

## References
- [Tilt Documentation](https://docs.tilt.dev/)
- [Tiltfile Reference](https://docs.tilt.dev/api.html)