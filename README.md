# Kdesk-Catalog

Universal AI agents & skills registry. Write once in YAML, deploy to 45+ platforms — Claude Code, Cursor, GitHub Copilot, Windsurf, OpenCode, Codex CLI, Gemini CLI, Zed, Cline, Goose, and more.

**3,093 definitions** (1,858 agents + 1,235 skills) across 45 categories.

## How It Works

1. **Write** an agent or skill as a YAML file in `universal-agents/`
2. **Convert** it with the built-in converter to any platform's native format
3. **Install** the output files into your tool's directory

```bash
git clone https://github.com/OpKnock/Kdesk-Catalog
cd Kdesk-Catalog

# Generate for all platforms
python scripts/universal-converter.py --platforms all --quiet

# Or just one
python scripts/universal-converter.py --platforms claude_code --quiet

# Copy output to your tool
cp platform-agents/claude_code/.claude/agents/*.md ~/.claude/agents/
```

## Components

| Component | What it does |
|-----------|-------------|
| **Catalog** | 3,093 YAML definitions across 45 categories (ML, DevOps, Security, Design, etc.) |
| **Converter** | Converts universal YAML to native formats for 45+ platforms |
| **Doctor** | Scans projects for AI config issues, diagnoses compatibility, applies fixes |
| **Marketplace** | Local registry: publish, search, install skills with semver resolution |
| **Policy Engine** | 12 quality rules + custom policies, enforced across the catalog |
| **Testing Framework** | Unit test agents without running real tools (mock executors) |
| **Delegation Engine** | Agents delegate to sub-agents (sequential, parallel, or conditional) |
| **Version Resolver** | Resolve `name@^2.0` semver constraints against the catalog |
| **Graph Visualization** | Interactive D3.js dependency graph of the catalog |
| **Telemetry** | Anonymous opt-in usage tracking |

## Installation

```bash
pip install -e .
kdesk --version
```

Requires Python 3.11+ and PyYAML.

## Key Commands

```bash
# Verify catalog integrity
python -m kdesk.cli verify --fast

# Validate schema
python scripts/schema-check.py

# Run policy checks (12 rules)
python -m kdesk.cli policy

# Convert to a specific platform
python scripts/universal-converter.py --platforms windsurf --quiet

# Search marketplace
python -m kdesk.cli skill search "terraform"

# Resolve a version constraint
python -m kdesk.cli resolve-version my-skill@^2.0

# Delegate to sub-agents
python -m kdesk.cli delegate ml-pipeline-orchestrator

# Generate dependency graph
python scripts/generate-graph.py --output graph.html

# Generate compatibility matrix
python scripts/generate-compatibility-matrix.py

# Scan a project for issues
python -m kdesk.cli doctor --mode diagnose --platform claude_code --project-root ./my-project

# Run tests
pytest tests/ -q
```

## Platform Formats

| Platform | Format | Location |
|----------|--------|----------|
| Claude Code | `.md` | `.claude/agents/`, `.claude/skills/` |
| Cursor | `.mdc` | `.cursor/rules/` |
| GitHub Copilot | `.instructions.md` | `.github/instructions/` |
| Windsurf | `.md` | `.windsurf/rules/` |
| OpenCode | Plugin | `.opencode/agents/`, `.opencode/skills/` |
| Zed | `SKILL.md` | `.agents/skills/` |
| Cline | `SKILL.md` | `.clinerules/skills/` |
| Codex CLI | `.md` | `.agents/skills/` |
| Gemini CLI | `SKILL.md` | `.gemini/skills/` |
| Goose | `.yaml` | `.goose/recipes/` |
| Aider | `.md` | `conventions/` |
| + 34 more | | See `tools.json` |

Each platform directory in `platform-agents/` includes its own README with install instructions.

## Writing Agents

Create a YAML file in `universal-agents/<category>/agent/`:

```yaml
name: my-agent
display_name: My Agent
category: devops
description: >
  Describe what this agent does, when to use it, and what tools it needs.
  Minimum 200 characters required by policy engine.
version: 1.0.0
capabilities:
  - name: do-thing
    description: Do the thing
    commands:
      - actual-cli-command --flag value
    examples:
      - actual-cli-command --flag value
    parameters:
      - name: target
        type: string
        description: What to target
instructions: >
  System prompt for the agent. Be specific about behavior.
knowledge:
  - title: Docs
    source: https://example.com/docs
platforms:
  claude_code:
    tools: [Bash, Read]
```

See `CONTRIBUTING.md` for full guidelines and `schemas/universal-agent.schema.json` for the complete schema.

## CI/CD

GitHub Actions automatically:
- Validates schema on every PR
- Runs policy checks, security scans, duplicate detection, license gates
- Regenerates all platform outputs when `universal-agents/` changes
- Tests on Ubuntu, macOS, and Windows
- Generates SBOM (CycloneDX) and runs dependency vulnerability scanning
- Runs golden converter tests to catch output drift

## Project Structure

```
Kdesk-Catalog/
├── universal-agents/       # Source of truth (edit here)
├── kdesk/                  # Python package (CLI engine)
│   ├── cli.py              # Command-line interface
│   ├── platforms.py        # Canonical platform registry
│   ├── marketplace.py      # Skill marketplace backend
│   ├── delegation.py       # Sub-agent runtime resolution
│   ├── versioning.py       # Semver constraint resolver
│   ├── policy.py           # Policy-as-code engine
│   └── ...
├── scripts/                # Production automation
├── schemas/                # JSON schema
├── tests/                  # Test suite
├── marketplaces/           # Per-platform manifests
├── reports/                # Generated status reports
└── platform-agents/        # Generated platform output
```

## License

MIT © Kdesk
