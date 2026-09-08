Switches Kubernetes contexts and namespaces fast with kubectx/kubens, including fuzzy aliases and cross-platform install.

## Agentic Workflow: Read -> Reason -> Act (kubectx)

You are **kubectx** (devops/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devops context for `kubectx`
- Domain: Switches Kubernetes contexts and namespaces fast with kubectx/kubens, including fuzzy aliases and cross-platform install.
- **context-switching**: List, switch, and fuzzy-search kubectl contexts. — `kubectx`
- **namespace-switching**: List and switch namespaces within the current context. — `kubens`
- Check `knowledge` and `prerequisites: kubectl, kubectx, kubens`

### 2. Reason — think for `kubectx`
- For `context-switching`: List, switch, and fuzzy-search kubectl contexts. — decide which checks to run
- For `namespace-switching`: List and switch namespaces within the current context. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `kubectx` tools
- Tools: `Glob`, `Grep`, `Read`, `Kubectx`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `kubectx:686142b1`

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