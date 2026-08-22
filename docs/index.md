# Kdesk-Catalog Documentation

**Universal AI Agents & Skills Registry** — 3,093 production-ready definitions converting to 45+ platforms.

## What is Kdesk?

Kdesk-Catalog is a registry where you write an AI agent or skill **once** in YAML, and it converts automatically to every major platform: Claude Code, Cursor, GitHub Copilot, Windsurf, OpenCode, Codex CLI, Gemini CLI, Zed, and 35+ more.

## Key Features

- **Write once, deploy everywhere** — 45+ output formats from a single YAML source
- **Agent composition** — agents delegate to sub-agents (sequential/parallel/conditional)
- **Skill marketplace** — publish, search, install with semver resolution
- **Policy-as-code** — 12 built-in quality rules with custom policy support
- **Testing framework** — unit test agents without real tool execution
- **Interactive graph** — visualize catalog dependencies in your browser

## Quick Example

```yaml
name: my-deploy-agent
display_name: Deploy Agent
category: devops
description: >
  Automates application deployment to Kubernetes clusters using Helm charts,
  handles rollback on failure, validates health checks post-deploy.
version: 1.0.0
capabilities:
  - name: deploy
    description: Deploy app via Helm
    commands:
      - helm upgrade --install myapp ./chart --namespace prod
    examples:
      - helm upgrade --install myapp ./chart --namespace prod
    parameters:
      - name: namespace
        type: string
        description: Target namespace
instructions: >
  You are a deployment specialist. Always verify cluster connectivity first,
  then run the deployment, then check pod status until all are Running.
knowledge:
  - title: Helm Docs
    source: https://helm.sh/docs
platforms:
  claude_code:
    tools: [Bash, Read]
```

Convert to Claude Code:
```bash
python scripts/universal-converter.py --platforms claude_code --quiet
cp -r platform-agents/claude_code/.claude/agents/my-deploy-agent.md ~/.claude/agents/
```

## Navigation

Use the sidebar or search bar above to find detailed documentation.
