<h1 align="center">🔧 Kdesk-Catalog</h1>

<p align="center">
  <strong>Universal AI Agents & Skills Registry</strong><br>
  3,093 production-ready definitions · 45+ platforms · Write once, deploy everywhere
</p>

<p align="center">
  <a href="https://github.com/OpKnock/Kdesk-Catalog/actions"><img src="https://img.shields.io/github/actions/workflow/status/OpKnock/Kdesk-Catalog/ci.yml?branch=main&label=CI&logo=github" alt="CI"></a>
  <a href="https://github.com/OpKnock/Kdesk-Catalog"><img src="https://img.shields.io/badge/platforms-45%2B-blue" alt="Platforms"></a>
  <a href="https://github.com/OpKnock/Kdesk-Catalog/tree/main/universal-agents"><img src="https://img.shields.io/badge/agents-1%2C858-green" alt="Agents"></a>
  <a href="https://github.com/OpKnock/Kdesk-Catalog/tree/main/universal-agents"><img src="https://img.shields.io/badge/skills-1%2C235-green" alt="Skills"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-brightgreen" alt="License"></a>
  <a href="https://github.com/OpKnock/Kdesk-Catalog/pulls"><img src="https://img.shields.io/badge/PRs-welcome-orange" alt="PRs Welcome"></a>
</p>

---

## 🚀 What Is This?

**Kdesk-Catalog** is an all-in-one platform for building, sharing, and deploying AI agents and skills across every major AI coding tool.

Every AI coding assistant has its **own proprietary format** — Claude Code wants `.md` files, Cursor wants `.mdc`, Copilot wants `.instructions.md`. If you build an agent for one tool, it doesn't work in another. Kdesk eliminates that: **write once in YAML → deploy everywhere.**

---

### 🏗️ The Three Core Components

#### 1. Kdesk Catalog — The Registry

A library of **3,093 production-ready definitions** (1,858 agents + 1,235 skills) organized into 45 categories — ML, DevOps, Security, Design, Sales, Healthcare, and more. Each definition is a single YAML file containing:

- Who the agent is (name, description, personality)
- What it can do (capabilities with real CLI commands like `kubectl apply` or `terraform plan`)
- What tools it needs (kubectl, terraform, docker, python...)
- How to use it (instructions, examples, parameters)

You can use the existing catalog as-is, or add your own agents to it.

#### 2. Kdesk Converter — The Multi-Platform Engine

The converter takes any YAML definition and generates the exact native format for each platform. One YAML file becomes:

- `.claude/agents/ml-engineer.md` for Claude Code
- `.cursor/rules/ml-engineer.mdc` for Cursor  
- `.github/instructions/ml-engineer.instructions.md` for Copilot
- `.windsurf/rules/ml-engineer.mdc` for Windsurf
- ...and 41 more platforms automatically

```bash
python scripts/universal-converter.py --platforms claude_code,cursor,windsurf --quiet
```

No manual rewriting, no format research — just run the converter and copy the output.

#### 3. Kdesk Doctor — Diagnostics & Repair

A compatibility scanner that analyzes **any project directory** for AI configuration issues:

```bash
kdesk doctor --mode diagnose --platform claude_code --project-root ./my-project
```

It discovers what AI tools are configured, detects broken/incompatible agent files, finds missing fields and invalid formats, scans for leaked secrets, produces a health score (0–100), and applies automatic fixes with backups.

---

### ⚡ Everything Else Built On Top

| Feature | What It Does | Command |
|---------|-------------|---------|
| **Agent Composition** | Agents delegate to sub-agents (sequential/parallel/conditional) | `kdesk delegate ml-pipeline-orchestrator` |
| **Skill Marketplace** | Publish/search/install skills with semver versioning | `kdesk skill search "terraform"` |
| **Policy-as-Code** | 12 quality rules enforced across the catalog + custom rules | `kdesk policy` |
| **Agent Versioning** | Resolve agents with semver constraints (`@^2.0`) + breaking-change detection | `kdesk resolve-version my-skill@^2.0` |
| **Testing Framework** | Unit test agents without real tool execution (mock executors, assertions) | `pytest tests/test_agent_framework.py` |
| **Dependency Graph** | Interactive D3.js visualization of catalog relationships | `python scripts/generate-graph.py` |
| **Telemetry** | Anonymous opt-in usage stats (local only) | `kdesk telemetry` |
| **VS Code Extension** | YAML schema validation + autocomplete snippets for editing definitions | Copy `.vscode-kdesk/` to extensions |
| **Docs Site** | MkDocs Material site with search and navigation | `mkdocs serve` |
| **GitHub Auto-Convert** | CI regenerates all platform outputs when YAML changes on PRs | Automatic |

---

### 🔄 How It All Fits Together

```
┌─────────────────────────────────────────────────────────┐
│                    YOU (Developer)                       │
│  Write agent/skill YAML in universal-agents/            │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              Kdesk Converter                             │
│  Validates schema → checks policy rules → converts      │
│  to native formats for 45+ platforms                     │
└──────────────────────┬──────────────────────────────────┘
                       │
         ┌─────────────┼─────────────┐
         ▼             ▼             ▼
   Claude Code    Cursor       Windsurf    ...40 more
   (.claude/)   (.cursor/)  (.windsurf/)
         │             │             │
         └─────────────┼─────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│              Kdesk Doctor                                │
│  Scans installed configs → diagnoses issues →           │
│  scores health (0-100) → applies fixes with backups      │
└─────────────────────────────────────────────────────────┘
```

---

### 📦 Quick Example

Write this YAML once:

```yaml
name: db-migration
display_name: Database Migration Specialist
category: database
description: >
  Plans and executes zero-downtime database migrations with rollback
  strategies, schema validation, and cutover planning.
version: 1.0.0
capabilities:
  - name: migrate
    description: Run migration
    commands:
      - flyway migrate -configFile=./flyway.conf
    examples:
      - flyway migrate -configFile=./flyway.conf
    parameters:
      - name: config_path
        type: string
        description: Path to Flyway config
instructions: >
  Analyze current schema, identify breaking changes, propose a phased
  migration plan with rollback steps, validate data integrity after.
platforms:
  claude_code:
    tools: [Bash, Read]
```

Then:

```bash
# Generate for Claude Code
python scripts/universal-converter.py --platforms claude_code --quiet

# Install it
cp platform-agents/claude_code/.claude/agents/db-migration.md ~/.claude/agents/

# Done! Also works for Cursor, Copilot, Windsurf, etc.
cp platform-agents/cursor/db-migration.mdc .cursor/rules/
```

---

## 🚀 Quick Start

### 1. Clone & Generate

```bash
git clone https://github.com/OpKnock/Kdesk-Catalog
cd Kdesk-Catalog

# Generate for ALL platforms
python scripts/universal-converter.py --platforms all --quiet

# Or just one platform (fast)
python scripts/universal-converter.py --platforms windsurf --quiet
```

### 2. Install to Your Tool

| Platform | Install Command |
|----------|-----------------|
| **Claude Code** | `cp -r platform-agents/claude_code/.claude/* ~/.claude/` |
| **Cursor** | `cp -r platform-agents/cursor/* .cursor/rules/` |
| **GitHub Copilot** | `cp -r platform-agents/github_copilot/.github .github/` |
| **Codex CLI** | `cp -r platform-agents/codex_cli/.agents .` |
| **Gemini CLI** | `cp -r platform-agents/gemini_cli/.gemini .` |
| **Windsurf** | `cp -r platform-agents/windsurf/* .windsurf/rules/` |
| **OpenCode** | `opencode plugin install ./platform-agents/opencode` |
| **Zed** | `cp -r platform-agents/zed/.agents .` |
| **Cline** | `cp -r platform-agents/cline/.clinerules .` |
| **Goose** | `cp -r platform-agents/goose/recipes/* ~/.config/goose/recipes/` |

> Each platform folder in `platform-agents/` has its own `README.md` with exact instructions.

---

## 🎯 Platform Output Formats

Each of the 45 platforms receives agents/skills in its **native format**:

| Platform | Format | Agent Location | Skill Location |
|----------|--------|----------------|----------------|
| **Claude Code** | `.md` + frontmatter | `.claude/agents/*.md` | `.claude/skills/<name>/SKILL.md` |
| **Cursor** | `.mdc` (rules) | `.cursor/rules/*.mdc` | `.cursor/rules/*.mdc` |
| **GitHub Copilot** | `.instructions.md` | `.github/instructions/*.instructions.md` | N/A |
| **Codex CLI** | `.md` | `.agents/*.md` | N/A |
| **Gemini CLI** | `SKILL.md` | N/A | `.gemini/skills/*/SKILL.md` |
| **Windsurf** | `.mdc` | `.windsurf/rules/*.mdc` | `.windsurf/rules/*.mdc` |
| **OpenCode** | Plugin | `.opencode/agents/` | `.opencode/skills/` |
| **Zed** | `SKILL.md` | N/A | `.agents/skills/*/SKILL.md` |
| **Cline** | `SKILL.md` | N/A | `.clinerules/skills/*/SKILL.md` |
| **Goose** | YAML recipes | `.goose/recipes/*.yaml` | N/A |
| **Aider** | `.md` conventions | `conventions/*.md` | N/A |
| **And 35+ more...** | Platform-specific | Platform-specific | Platform-specific |

---

## ✨ Features

### 🔗 Agent Composition & Chaining

Agents can delegate work to specialized sub-agents:

```yaml
name: ml-pipeline-orchestrator
sub_agents:
  - data-engineer
  - ml-engineer
  - model-deployer
delegation_pattern: sequential   # or parallel | conditional
```

Runtime resolution via CLI:

```bash
# Resolve and execute sub-agent delegation chain
kdesk delegate ml-pipeline-orchestrator
```

Supports recursive delegation (up to depth 5), failure propagation in sequential mode, and first-match-wins in conditional mode.

---

### 🛒 Skill Marketplace

Real local registry backed by `marketplace-registry.json`:

```bash
# Publish a skill from the catalog
kdesk skill publish terraform-infrastructure

# Search by keyword
kdesk skill search "terraform"

# Resolve a specific version (semver)
kdesk skill install kubernetes-deployment@^2.0.0

# List all published skills
kdesk skill list
```

Supports semver constraints (`^`, `~`, `>=`, `<`), duplicate detection, and checksum validation.

---

### 🔢 Agent Versioning & Semver Resolution

Resolve agents/skills with version constraints:

```bash
# Resolve best match for a semver range
kdesk resolve-version terraform-infrastructure@^2.0.0

# Exact version
kdesk resolve-version my-agent@1.2.3

# Any version (latest)
kdesk resolve-version docker-deployment
```

Includes breaking-change detection on major version bumps.

---

### 🧪 Agent Testing Framework

Write unit tests for agents without real tool execution:

```python
from tests.test_agent_framework import AgentTestCase, MockToolExecutor

class TestMyAgent(AgentTestCase):
    def test_agent_has_capabilities(self):
        self.create_test_agent("my-agent", capabilities=[{
            "name": "deploy",
            "description": "Deploy to production",
            "commands": ["kubectl apply -f manifest.yaml"],
            "parameters": [{"name": "env", "type": "string"}]
        }])
        self.assert_capability_exists("my-agent", "deploy")
        self.assert_tool_available("my-agent", "kubectl")

    def test_sub_agent_delegation(self):
        self.create_test_agent("orchestrator", sub_agents=["worker-a"])
        self.assert_sub_agents("orchestrator", ["worker-a"])

    def test_mock_tool_execution(self):
        executor = MockToolExecutor()
        executor.set_response("git", {"success": True, "stdout": "abc123"})
        result = executor.execute("git", ["commit"])
        self.assertTrue(result["success"])
```

Run: `pytest tests/test_agent_framework.py -v`

---

### 📋 Policy-as-Code

Enforce quality rules across the catalog:

```bash
kdesk policy                          # Run 12 built-in rules
kdesk policy --format json            # JSON for CI
kdesk policy --policy-file custom.yaml  # Custom rules
```

Built-in rules: description length, capability completeness, tool declarations, semantic versioning, sub-agent existence, skills-exist, delegation-pattern validity, and more.

Custom policy format:

```yaml
version: "1.0"
rules:
  - id: no-secrets
    name: No Hardcoded Secrets
    severity: critical
    condition: "'password' in str(agent.capabilities).lower()"
    message: Potential secret detected
```

---

### 🕸 Dependency Graph Visualization

Generate an interactive HTML graph:

```bash
python scripts/generate-graph.py --output catalog-graph.html
python scripts/generate-graph.py --category ml --max-nodes 800
```

Features D3.js force-directed layout, search highlighting, tooltips, zoom/pan.

---

### 📊 Anonymous Telemetry

Opt-in usage tracking (local only, no network):

```bash
# View stats
kdesk telemetry

# Enable collection
KD_TELEMETRY=1 kdesk verify
```

Tracks command name, duration, and success/fail. Never records arguments or content.

---

### 🏥 Kdesk Doctor

Compatibility, diagnosis, repair, and validation system:

```bash
# Scan project
kdesk doctor --mode scan --project-root ./my-project

# Diagnose + fix
kdesk doctor --mode diagnose --platform claude_code --project-root ./my-project --fix

# CI gate
kdesk doctor --mode diagnose --platform claude_code --ci --threshold 90 --json
```

Features project scanning, compatibility scoring (0–100), automatic fixes with backups, secret redaction, and CI mode.

---

### 📖 Documentation Site

```bash
pip install mkdocs mkdocs-material
mkdocs serve    # http://localhost:8000
mkdocs build    # generates site/
```

---

### 🧩 VS Code Extension

Schema validation + autocomplete for `universal-agents/` YAML files:

Copy `.vscode-kdesk/` into your `.vscode/extensions/kdesk-yaml/` directory. Provides:
- JSON Schema validation against `schemas/universal-agent.schema.json`
- Snippets for agent (`kdesk-agent`) and skill (`kdesk-skill`) templates

---

### ⚙️ GitHub Auto-Convert

`.github/workflows/convert.yml` auto-regenerates the catalog whenever a PR touches `universal-agents/**/*.yaml`. Validates schema → regenerates outputs → auto-commits.

---

## 🎭 The Catalog Roster

<details>
<summary><strong>💻 Engineering Division</strong></summary>

| Agent | Specialty | When to Use |
|-------|-----------|-------------|
| [ML Engineer](universal-agents/ml/agent/ml-engineer.yaml) | ML pipelines, training, deployment | End-to-end ML pipelines, MLOps |
| [API Architect](universal-agents/api/agent/api-architect.yaml) | REST/GraphQL design | API design, contract testing |
| [SRE Engineer](universal-agents/sre/agent/sre-engineer.yaml) | Reliability, SLOs | SLOs, error budgets, chaos engineering |
| [DevOps Engineer](universal-agents/devops/agent/devops-engineer.yaml) | CI/CD, infrastructure | Pipelines, IaC |
| [Kubernetes Specialist](universal-agents/devops/deployment/kubernetes-deployment.yaml) | K8s deployments | K8s manifests, Helm charts |

</details>

<details>
<summary><strong>🔒 Security Division</strong></summary>

| Agent | Specialty | When to Use |
|-------|-----------|-------------|
| [API Security Engineer](universal-agents/security/agent/api-security-engineer.yaml) | API auth, rate limiting | Auth, threat modeling |
| [Security Scanner](universal-agents/security/agent/security-trivy-agent.yaml) | Container scanning | Trivy, Grype, Syft |
| [Compliance Scanner](universal-agents/security/agent/compliance-scanner.yaml) | SOC2, PCI, GDPR | Audit prep, evidence |

</details>

<details>
<summary><strong>🎨 Design Division</strong></summary>

| Agent | Specialty | When to Use |
|-------|-----------|-------------|
| [UI Designer](universal-agents/design/agent/design-ui-designer.yaml) | Visual design | Interface creation |
| [UX Researcher](universal-agents/design/agent/design-ux-researcher.yaml) | User testing | Usability testing |
| [Design Systems Engineer](universal-agents/design/agent/design-design-systems-engineer.yaml) | Design tokens | Component libraries, Storybook |

</details>

<details>
<summary><strong>💰 Business Divisions</strong></summary>

Paid Media (Google/Meta Ads), Sales (outbound, MEDDPICC), Marketing (growth, content, social), Product (PM, analytics), Finance (fintech, trading), Support (customer success), GIS, Healthcare (HIPAA, FHIR), Academic, Game Development (Unity, Unreal, Godot).

</details>

<details>
<summary><strong>🛠 Skill Categories</strong></summary>

| Category | Examples |
|----------|----------|
| Tool Workflows | Terraform, Docker, Kubernetes, CI/CD Pipeline |
| Security & Compliance | Trivy Scanner, Semgrep, SOC2 Compliance |
| Patterns | Circuit Breaker, Sidecar, Adapter |
| ML Operations | Model Training, Inference Serving, Monitoring |
| Data Engineering | Streaming Pipelines, Data Virtualization |

</details>

---

## 🏗 Project Structure

```
Kdesk-Catalog/
├── universal-agents/          # ← EDIT THESE (source of truth)
│   ├── ml/                    # 501+ agents, 543+ skills
│   ├── api/                   # 14 agents, 494 skills
│   ├── devops/                # 38 agents, 142 skills
│   ├── security/              # 31 agents, 66 skills
│   ├── design/                # Design agents & skills
│   ├── sales/                 # Sales agents & skills
│   ├── healthcare/            # Healthcare agents & skills
│   └── ... (45 categories)
├── kdesk/                     # Python package (CLI engine)
│   ├── cli.py                 # All commands
│   ├── marketplace.py         # Skill marketplace backend
│   ├── delegation.py          # Sub-agent runtime resolution
│   ├── versioning.py          # Semver resolution
│   ├── policy.py              # Policy-as-code engine
│   ├── telemetry.py           # Anonymous usage tracking
│   └── ...
├── scripts/                   # Automation (converter, validators)
│   ├── universal-converter.py # Multi-platform converter
│   ├── generate-graph.py      # Dependency graph visualization
│   └── generate-reports.py    # Report generator
├── schemas/                   # JSON schema for definitions
├── tests/                     # Test suite
│   ├── test_agent_framework.py # Agent testing framework
│   └── ...
├── docs/                      # MkDocs documentation
├── .vscode-kdesk/             # VS Code extension config
├── .github/workflows/         # CI + auto-conversion
├── marketplaces/              # Per-platform marketplace manifests
├── reports/                   # Status reports
├── platform-agents/           # Auto-generated output
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
└── tools.json                 # Platform manifest (45 tools)
```

---

## 🔧 Key Commands

```bash
# Validate schema
python scripts/schema-check.py

# Full verification
python -m kdesk.cli verify --fast

# Policy checks
python -m kdesk.cli policy

# Convert to a platform
python scripts/universal-converter.py --platforms windsurf --quiet

# Generate dependency graph
python scripts/generate-graph.py --output graph.html

# Run tests
pytest tests/test_agent_framework.py -v

# Docs site
mkdocs serve

# Marketplace
python -m kdesk.cli skill search "terraform"

# Sub-agent delegation
python -m kdesk.cli delegate ml-pipeline-orchestrator

# Version resolution
python -m kdesk.cli resolve-version my-skill@^2.0

# Telemetry stats
python -m kdesk.cli telemetry
```

---

## ✅ Verification Status

| Check | Status |
|-------|--------|
| Schema validation | ✅ 0 violations / 3,093 files |
| Policy engine | ✅ 12/12 rules pass |
| Catalog consistency | ✅ 313 divisions |
| Wiring integrity | ✅ 1,476 nodes, no cycles |
| Security scan | ✅ 0 blocking secrets |
| Duplicate scan | ✅ 0 unresolved |
| License gate | ✅ All resolved |
| Quality check | ✅ 0 issues |
| Unit tests | ✅ All passing |
| CI (GitHub Actions) | ✅ Schema + Tests + Verify + CI green |

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. PRs welcome!

Please read our [Code of Conduct](CODE_OF_CONDUCT.md).

---

## 📜 License

MIT © [Kdesk](https://github.com/OpKnock)

---

<div align="center">

**[⭐ Star this repo](https://github.com/OpKnock/Kdesk-Catalog)** if you find it useful!



</div>
