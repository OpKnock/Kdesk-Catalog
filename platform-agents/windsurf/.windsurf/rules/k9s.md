---
trigger: glob
description: "Navigates Kubernetes clusters with the k9s terminal UI: pod inspection, log streaming, resource editing, and context switching."
globs: ["**/*.go", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

# k9s

Navigates Kubernetes clusters with the k9s terminal UI: pod inspection, log streaming, resource editing, and context switching.

## Instructions

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
