# Universal Agent Format Specification

## Format: YAML (universal, human-readable, easily parsed)

```yaml
# Universal Agent Schema
name: string                    # unique identifier (lowercase, hyphens)
display_name: string            # human-readable name
category: string                # e.g., "ml", "devops", "database", "api", "security"
subcategory: string             # optional: "training", "inference", "deployment", etc.
description: string             # what this agent does
version: string                 # semantic version (1.0.0)
color: string                   # optional UI accent color (hex, #RRGGBB)
emoji: string                   # optional icon emoji for marketplaces
vibe: string                    # optional tone descriptor ("playful", "formal")
voice: string                   # optional voice descriptor ("concise", "friendly")
tags:                           # searchable tags
  - string
author: string                  # optional
license: string                 # optional (MIT, Apache-2.0, etc.)

# Capabilities - what this agent can do
capabilities:
  - name: string                # capability name
    description: string         # what it does
    commands:                   # real CLI commands this capability uses
      - string                  # e.g., "kubectl apply -f deployment.yaml"
    examples:                   # usage examples
      - string
    parameters:                 # configurable parameters
      - name: string
        type: string            # string, int, bool, enum
        description: string
        required: bool
        default: any

# Knowledge base - reference materials
knowledge:
  - title: string
    type: string                # "documentation", "tutorial", "reference", "best-practices"
    source: string              # URL or local path
    description: string

# Platform-specific overrides (optional)
platforms:
  claude_code:
    tools: [Bash, Read, Write, Edit, Glob, Grep]
    model: claude-3-5-sonnet-20241022
  cursor:
    rule_type: string           # "always", "auto", "agent"
    model: string
  github_copilot:
    extension: string
    prompt_file: string
  windsurf:
    config_path: string
  opencode:
    plugin: string
  generic:
    system_prompt: string
    available_tools: [string]

# Metadata
created_at: string              # ISO 8601
updated_at: string              # ISO 8601
checksum: string                # SHA256 for integrity
```

## Directory Structure
```
universal-agents/
├── ml/
│   ├── training/
│   │   ├── pytorch-training.yaml
│   │   ├── tensorflow-training.yaml
│   │   └── ...
│   ├── inference/
│   ├── deployment/
│   └── ...
├── devops/
├── database/
├── api/
├── security/
├── ...
└── registry.yaml              # master index of all agents
```

## Registry Format (registry.yaml)
```yaml
agents:
  - name: pytorch-training
    path: ml/training/pytorch-training.yaml
    category: ml
    subcategory: training
    version: 1.0.0
    tags: [pytorch, training, gpu, distributed]
    platforms: [claude_code, cursor, copilot, windsurf, opencode, generic]
  - name: kubernetes-deployment
    path: devops/kubernetes-deployment.yaml
    ...
```

## Conversion Scripts Provided
- `convert-to-claude-code.py` → generates `.json` for `.claude/agents/`
- `convert-to-cursor.py` → generates `.cursor/rules/` or `.cursor/agents/`
- `convert-to-copilot.py` → generates VS Code extension + prompts
- `convert-to-windsurf.py` → generates `.windsurf/` configs
- `convert-to-opencode.py` → generates OpenCode plugin format
- `convert-to-generic.py` → generates simple system prompt + tool list
- `validate.py` → validates all agents against schema
- `sync.py` → syncs from universal to platform-specific directories
```

## Quick Start
```bash
# Install dependencies
pip install pyyaml jsonschema

# Validate all agents
python scripts/validate.py

# Convert to specific platform
python scripts/convert-to-claude-code.py --output ~/.claude/agents/
python scripts/convert-to-cursor.py --output .cursor/agents/

# Sync all platforms
python scripts/sync.py --platforms claude_code,cursor,copilot,windsurf,opencode
```

This universal format works with **any** AI coding agent - just parse the YAML and map to your platform's format.