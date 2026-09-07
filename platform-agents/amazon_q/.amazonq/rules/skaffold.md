Develops Kubernetes applications with Skaffold: continuous build/sync/deploy loop, profiles, debugging, and CI render pipelines.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `skaffold dev`, `skaffold build`
- Check `knowledge` references and prerequisites before proceeding

### 2. Reason
Analyze and plan:
- Compare current state vs desired state (drift, checksums, policy)
- Evaluate trust, compatibility, and risk: use `kdesk trust` and `kdesk doctor` patterns
- Decide: which capabilities/tools are needed, which can be skipped

### 3. Act
Execute with guards:
- Run only `allowed-tools` (see frontmatter); use `safe_path` for writes
- Prefer `Bash` with explicit binaries (`curl`, `kubectl`, `kdesk`) over generic shell
- Record evidence: file paths, checksums, and tool outputs for verification

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