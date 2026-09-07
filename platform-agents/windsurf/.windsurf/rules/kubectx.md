---
trigger: glob
description: "Switches Kubernetes contexts and namespaces fast with kubectx/kubens, including fuzzy aliases and cross-platform install. Use when working with context switching, namespace switching, devops or when the user mentions context switching, namespace switching, devops."
globs: ["**/*.r", "**/*.sh"]
---

Switches Kubernetes contexts and namespaces fast with kubectx/kubens, including fuzzy aliases and cross-platform install.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `kubectx`, `kubens`
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

# kubectx / kubens

Switch Kubernetes contexts and namespaces in one keystroke.

## What This Skill Does

- Lists and switches contexts without remembering long names
- Switches namespaces inside the current context
- Toggles between last two contexts/namespaces with `-`
- Integrates with fzf for fuzzy search
- Works with completion scripts and aliases

## When to Use

- Multi-cluster day-to-day operations
- Rapid context hopping during incidents
- Terminal workflows where kubectl config use-context is too slow

## Real Commands

```bash
# Contexts
kubectx                       # list all
kubectx prod-east             # switch
kubectx -                     # toggle back
kubectx -c                    # current
kubectx old new               # rename

# Namespaces
kubens                        # list
kubens kube-system            # switch
kubens -                      # toggle back
kubens -c                     # current
```

## With fzf

```bash
# fuzzy switch
kubectx                     # press tab or use fzf if installed
kubens
```

## Best Practices

- Install completions: `source <(kubectx --completion zsh)`
- Add aliases `alias kx=kubectx` and `alias kns=kubens` to shell profile
- Verify switch with `kubectl config current-context` in scripts
- Pair with `KUBECONFIG` merge for vendor contexts
- Use `kubens -` during incident toggling between app and kube-system

## Capabilities

### context-switching
List, switch, and fuzzy-search kubectl contexts.

**Parameters:**
- `context` (string): Context name to switch to
- `prev` (string): Toggle back to previous context with -

**Commands:**
- `kubectx`
- `kubectx prod-east`
- `kubectx -`
- `kubectx -c`
- `kubectx demo-old demo-new`
- `kubectl config get-contexts`

**Examples:**
- kubectx
- kubectx prod-east
- kubectx -

### namespace-switching
List and switch namespaces within the current context.

**Parameters:**
- `namespace` (string): Namespace to switch to
- `toggle` (boolean): Return to previous namespace with -

**Commands:**
- `kubens`
- `kubens kube-system`
- `kubens -`
- `kubens -c`
- `kubens default`

**Examples:**
- kubens
- kubens kube-system
- kubens -

## References
- [kubectx GitHub](https://github.com/ahmetb/kubectx)
- [Kubernetes kubectl config](https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/)
