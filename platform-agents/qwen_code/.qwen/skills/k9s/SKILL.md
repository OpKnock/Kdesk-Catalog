---
name: "k9s"
description: "Navigates Kubernetes clusters with the k9s terminal UI: pod inspection, log streaming, resource editing, and context switching. Use when working with terminal ui navigation, live observability, devops or when the user mentions terminal ui navigation, live observability, devops."
license: "MIT"
compatibility: "Requires k9s."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "devops"}
allowed-tools: "Glob Grep Read Bash(k9s:*)"
---

Navigates Kubernetes clusters with the k9s terminal UI: pod inspection, log streaming, resource editing, and context switching.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `k9s`, `k9s --logoless`
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

# k9s Terminal UI

Operate Kubernetes from a fast terminal dashboard instead of long kubectl pipelines.

## What This Skill Does

- Views resources per namespace or all namespaces
- Streams pod logs live and exec into containers
- Edits manifests inline and watches rollouts
- Switches contexts/clusters and uses custom skins
- Extends behavior with plugins and hotkeys

## When to Use

- Rapid triage across many namespaces
- Following a deployment rollout in real time
- Terminal-only environments (SSH boxes, bastion hosts)

## Real Commands

```bash
# Launch variants
k9s
k9s -n production
k9s -A
k9s -c deployments
k9s --context staging
k9s --readonly
k9s --command deploy/web
k9s --kubeconfig ~/.kube/config2
```

## Key Bindings (in-app)

- `0-9` switch resource views (pods, deploys, svc, ...)
- `l` logs, `s` shell/exec, `d` describe, `e` edit
- `ctrl-d` delete, `ctrl-k` kill
- `:ctx` switch context, `:ns` switch namespace
- `?` full keymap reference

## Best Practices

- Use `--readonly` in production sessions to avoid fat-finger deletes
- Alias it: `alias k=k9s -n` in daily shells
- Use skins (config/skins/) for high-contrast terminals
- Combine with kubectx contexts for multi-cluster hops
- Prefer k9s for triage, kubectl for scripting and automation

## Capabilities

### terminal-ui-navigation
Launch k9s scoped to namespaces, resources, or contexts, and use hotkeys for views.

**Parameters:**
- `namespace` (string): Namespace to scope to
- `context` (string): Kubeconfig context
- `resource` (string): Initial resource view, e.g. deployments

**Commands:**
- `k9s`
- `k9s -n production`
- `k9s -A`
- `k9s -c deployments`
- `k9s --context staging`
- `k9s --headless -c pods`

**Examples:**
- k9s -n production
- k9s -A -c secrets
- k9s --context staging

### live-observability
Stream logs, exec shells, and drill into resource details from the UI (keybindings).

**Parameters:**
- `command` (string): Initial view command like deploy/web
- `kubeconfig` (string): Alternate kubeconfig path

**Commands:**
- `k9s --logoless`
- `k9s --readonly`
- `k9s --command deploy/web`
- `k9s --kubeconfig ~/.kube/config2`
- `k9s --plugins myplugin.yaml`

**Examples:**
- k9s --readonly
- k9s --command deploy/web
- k9s --plugins myplugin.yaml

## References
- [k9s CLI Documentation](https://k9scli.io/)
- [k9s GitHub](https://github.com/derailed/k9s)
