---
type: agent_requested
description: "Uses GitHub Copilot in the terminal: suggest and explain commands with gh copilot, manage auth, and configure Copilot extensions. Use when working with copilot cli, auth and config, devtools or when the user mentions copilot cli, auth and config, devtools."
---

Uses GitHub Copilot in the terminal: suggest and explain commands with gh copilot, manage auth, and configure Copilot extensions.

## Agentic Workflow: Read -> Reason -> Act (github-copilot)

You are **Github Copilot** (devtools/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devtools context for `github-copilot`
- Domain: Uses GitHub Copilot in the terminal: suggest and explain commands with gh copilot, manage auth, and configure Copilot extensions.
- **copilot-cli**: Get command suggestions and explanations from the Copilot CLI. — `gh copilot suggest 'Deploy to production'`
- **auth-and-config**: Authenticate and configure the Copilot CLI. — `gh auth login`
- Check `knowledge` references before acting

### 2. Reason — think for `github-copilot`
- For `copilot-cli`: Get command suggestions and explanations from the Copilot CLI. — decide which checks to run
- For `auth-and-config`: Authenticate and configure the Copilot CLI. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `github-copilot` tools
- Tools: `Glob`, `Grep`, `Read`, `Gh` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `github-copilot:36ac3866`

# GitHub Copilot CLI

Get shell command suggestions and explanations from Copilot inside the terminal.

## What This Skill Does

- Suggests shell/git/gh commands from natural language
- Explains complex commands step by step
- Works with a targets: shell, git, gh
- Manages GitHub auth for Copilot access
- Configures model and output preferences

## When to Use

- Unsure how to accomplish a shell task
- Deciphering cryptic commands found in docs
- Quick command generation without leaving the terminal

## Real Commands

```bash
# Auth (first time)
gh auth login
gh auth status
gh auth refresh -s read:copilot

# Suggest
gh copilot suggest 'Deploy to production'
gh copilot suggest --target git 'squash last 3 commits'
gh copilot suggest --target gh 'list open PRs assigned to me'
gh copilot suggest --target shell 'find files larger than 100MB'

# Explain
gh copilot explain 'git reset --hard HEAD~2'
gh copilot explain 'kubectl drain node1 --ignore-daemonsets'
gh copilot explain 'rsync -avz --delete src/ dest/'

# Config
gh copilot config
gh copilot prompts list
gh copilot version
```

## Best Practices

- Always read the suggested command before running it
- Combine suggest + explain to learn unfamiliar tooling
- Keep gh updated; Copilot CLI ships with the gh extension
- Use --target to constrain scope (git vs shell)
- Review outputs; Copilot suggestions may need adjustments

## Capabilities

### copilot-cli
Get command suggestions and explanations from the Copilot CLI.

**Parameters:**
- `target` (string): Command target: git, gh, shell
- `prompt` (string): Natural language request

**Commands:**
- `gh copilot suggest 'Deploy to production'`
- `gh copilot explain 'git reset --hard HEAD~2'`
- `gh copilot suggest --target git 'rebase 3 commits'`
- `gh copilot explain 'kubectl drain node1 --ignore-daemonsets'`
- `gh copilot prompts list`

**Examples:**
- gh copilot suggest 'Find large files in git history'
- gh copilot explain 'ssh -L 8080:localhost:80 prod'
- gh copilot suggest --target gh 'list open PRs'

### auth-and-config
Authenticate and configure the Copilot CLI.

**Parameters:**
- `scopes` (string): OAuth scopes to refresh, e.g. read:copilot
- `model` (string): Copilot model preference for gh copilot config

**Commands:**
- `gh auth login`
- `gh auth status`
- `gh copilot config`
- `gh auth refresh -s read:copilot`
- `gh extension list`
- `gh copilot version`

**Examples:**
- gh auth login
- gh copilot config
- gh auth refresh -s read:copilot

## References
- [GitHub Copilot CLI Docs](https://docs.github.com/en/copilot/using-github-copilot/using-github-copilot-cli)
- [gh-copilot Extension](https://github.com/github/gh-copilot)