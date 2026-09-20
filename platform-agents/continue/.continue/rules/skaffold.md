---
name: "skaffold"
description: "Develops Kubernetes applications with Skaffold: continuous build/sync/deploy loop, profiles, debugging, and CI render pipelines. Use when working with dev loop, build and deploy, devops or when the user mentions dev loop, build and deploy, devops."
globs: ["**/*.java", "**/*.json", "**/*.py", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
alwaysApply: false
---

Develops Kubernetes applications with Skaffold: continuous build/sync/deploy loop, profiles, debugging, and CI render pipelines.

## Agentic Workflow: Read -> Reason -> Act (skaffold)

You are **skaffold** (devops/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devops context for `skaffold`
- Domain: Develops Kubernetes applications with Skaffold: continuous build/sync/deploy loop, profiles, debugging, and CI render pipelines.
- **dev-loop**: Run the watch-loop: auto build, sync, and deploy on file changes. — `skaffold dev`
- **build-and-deploy**: One-shot build, render, and deploy for CI pipelines. — `skaffold build`
- Check `knowledge` and `prerequisites: skaffold`

### 2. Reason — think for `skaffold`
- For `dev-loop`: Run the watch-loop: auto build, sync, and deploy on file changes. — decide which checks to run
- For `build-and-deploy`: One-shot build, render, and deploy for CI pipelines. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `skaffold` tools
- Tools: `Glob`, `Grep`, `Read`, `Skaffold` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `skaffold:06665022`

# Skaffold Development Loop

Iterate on Kubernetes apps locally: watch files, rebuild images, redeploy automatically.

## What This Skill Does

- Runs the dev loop: build, push, deploy, watch
- Syncs changed files into running containers without rebuilds
- Port-forwards services for local testing
- Runs interactive debuggers with skaffold debug
- Renders final manifests for CI deploy stages

## When to Use

- Local Kubernetes development against a cluster
- Fast inner loop without writing deploy scripts
- CI: build artifacts in one stage, deploy in another

## Real Commands

```bash
# Dev loop
skaffold dev
skaffold dev --port-forward
skaffold dev --profile dev --trigger notify
skaffold debug

# CI
skaffold build --file-output artifacts.json
skaffold deploy -a artifacts.json
skaffold run
skaffold render --digest-source=remote > rendered.yaml
skaffold delete
```

## skaffold.yaml Sketch

```yaml
apiVersion: skaffold/v4beta11
kind: Config
build:
  artifacts:
    - image: myapp
      context: .
  tagPolicy:
    sha256: {}
deploy:
  kubectl:
    manifests:
      - k8s/*.yaml
```

## Best Practices

- Use file sync for interpreted languages (Node, Python) to skip rebuilds
- Keep skaffold.yaml versioned in repo; profiles per env
- Use build/deploy split in CI for artifact reuse
- Use `skaffold debug` for Node/Java/Python debugger integration
- Add `--kube-context` in multi-cluster environments

## Capabilities

### dev-loop
Run the watch-loop: auto build, sync, and deploy on file changes.

**Parameters:**
- `profile` (string): Skaffold profile to activate
- `trigger` (string): Change trigger: notify, polling, manual

**Commands:**
- `skaffold dev`
- `skaffold dev --port-forward`
- `skaffold dev --profile dev`
- `skaffold dev --trigger notify`
- `skaffold debug`

**Examples:**
- skaffold dev --port-forward
- skaffold dev --profile dev
- skaffold debug

### build-and-deploy
One-shot build, render, and deploy for CI pipelines.

**Parameters:**
- `artifacts` (string): Artifacts file for staged CI builds
- `file` (string): skaffold.yaml path

**Commands:**
- `skaffold build`
- `skaffold build --file-output artifacts.json`
- `skaffold deploy -a artifacts.json`
- `skaffold run`
- `skaffold render --digest-source=remote > rendered.yaml`
- `skaffold delete`

**Examples:**
- skaffold build --file-output artifacts.json
- skaffold deploy -a artifacts.json
- skaffold render --digest-source=remote

## References
- [Skaffold Documentation](https://skaffold.dev/docs/)
- [Skaffold YAML Reference](https://skaffold.dev/docs/references/yaml/)