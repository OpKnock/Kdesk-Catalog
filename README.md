# Kdesk-Catalog

**Universal AI Agents & Skills Registry** — 3,093 production-ready definitions that convert once to 45+ platforms.

[![Platforms](https://img.shields.io/badge/platforms-45%2B-blue)](https://github.com/OpKnock/Kdesk-Catalog)
[![Agents](https://img.shields.io/badge/agents-1,858-green)](https://github.com/OpKnock/Kdesk-Catalog/tree/main/universal-agents)
[![Skills](https://img.shields.io/badge/skills-1,235-green)](https://github.com/OpKnock/Kdesk-Catalog/tree/main/universal-agents)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## 🎭 The Catalog: AI Specialists Ready to Transform Your Workflow

> **A complete AI agent & skill registry at your fingertips** — From ML engineers to Reddit community ninjas, from whimsy injectors to reality checkers. Each definition is a specialized expert with personality, processes, and proven deliverables.

[![Platforms](https://img.shields.io/badge/platforms-45%2B-blue)](https://github.com/OpKnock/Kdesk-Catalog)
[![Agents](https://img.shields.io/badge/agents-1,858-green)](https://github.com/OpKnock/Kdesk-Catalog/tree/main/universal-agents)
[![Skills](https://img.shields.io/badge/skills-1,235-green)](https://github.com/OpKnock/Kdesk-Catalog/tree/main/universal-agents)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## 🚀 What Is This?

**Kdesk-Catalog** is a hand-curated registry of AI agents and skills. Each definition is written once in YAML and automatically converts to work across **45+ platforms** — including Claude Code, Cursor, GitHub Copilot, Windsurf, OpenCode, Codex CLI, Gemini CLI, Zed, Cline, Goose, and more.

> **Source of truth:** `universal-agents/` — every agent and skill is a single YAML file with real commands, official documentation links, and expert instructions.

**Output:** `platform-agents/` — auto-generated platform-specific formats (gitignored, regenerated on demand).

[![Platforms](https://img.shields.io/badge/platforms-45%2B-blue)](https://github.com/OpKnock/Kdesk-Catalog)
[![Agents](https://img.shields.io/badge/agents-1,858-green)](https://github.com/OpKnock/Kdesk-Catalog/tree/main/universal-agents)
[![Skills](https://img.shields.io/badge/skills-1,235-green)](https://github.com/OpKnock/Kdesk-Catalog/tree/main/universal-agents)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## 🚀 Quick Start

### 1. Clone & Generate

```bash
git clone https://github.com/OpKnock/Kdesk-Catalog
cd Kdesk-Catalog

# Generate for ALL platforms (~15 min, 130k files)
python scripts/universal-converter.py --platforms all --quiet

# Or just one platform (fast)
python scripts/universal-converter.py --platforms windsurf --quiet
```

### 2. Install to Your Tool

| Platform | Install Command |
|----------|-----------------|
| **Claude Code** | `cp -r platform-agents/claude_code/.claude/agents/* ~/.claude/agents/ && cp -r platform-agents/claude_code/.claude/skills/* ~/.claude/skills/` |
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

## 🎭 The Catalog: AI Specialists Ready to Transform Your Workflow

> **A complete AI agent & skill registry at your fingertips** — From ML engineers to Reddit community ninjas, from whimsy injectors to reality checkers. Each definition is a specialized expert with personality, processes, and proven deliverables.

---

## 🎭 The Catalog Roster

### 💻 Engineering Division

Building the future, one commit at a time.

| Agent | Specialty | When to Use |
|-------|-----------|-------------|
| [ML Engineer](universal-agents/ml/agent/ml-engineer.yaml) | ML pipelines, training, deployment | End-to-end ML pipelines, model serving, MLOps |
| [API Architect](universal-agents/api/agent/api-architect.yaml) | REST/GraphQL design, contracts | API design, versioning, contract testing |
| [SRE Engineer](universal-agents/sre/agent/sre-engineer.yaml) | Reliability, SLOs, incident response | SLOs, error budgets, chaos engineering |
| [DevOps Engineer](universal-agents/devops/agent/devops-engineer.yaml) | CI/CD, infrastructure automation | CI/CD pipelines, infrastructure as code |
| [API Security Engineer](universal-agents/security/agent/api-security-engineer.yaml) | API security, auth, rate limiting | Auth, rate limiting, threat modeling |
| [Terraform Module Builder](universal-agents/devops/agent/devops-terraform-module-builder.yaml) | Terraform modules, providers | Module design, registry publishing |
| [Kubernetes Deployment Specialist](universal-agents/devops/deployment/kubernetes-deployment.yaml) | K8s deployments, Helm, Kustomize | K8s manifests, Helm charts, ArgoCD |

### 🎨 Design Division

| Agent | Specialty | When to Use |
|-------|-----------|-------------|
| [UI Designer](universal-agents/design/agent/design-ui-designer.yaml) | Visual design, component libraries | Interface creation, brand consistency |
| [UX Researcher](universal-agents/design/agent/design-ux-researcher.yaml) | User testing, behavior analysis | User research, usability testing |
| [Design Systems Engineer](universal-agents/design/agent/design-design-systems-engineer.yaml) | Design systems, component libraries | Design tokens, component libraries, Storybook |

### 💰 Paid Media Division

| Agent | Specialty | When to Use |
|-------|-----------|-------------|
| [PPC Campaign Strategist](universal-agents/paid-media/agent/paid-media-ppc-strategist.yaml) | Google/Meta/LinkedIn Ads | Account buildouts, budget allocation, scaling |
| [Search Query Analyst](universal-agents/paid-media/agent/paid-media-search-query-analyst.yaml) | Search term analysis, negative keywords | Query audits, wasted spend elimination |
| [Creative Strategist](universal-agents/paid-media/agent/paid-media-creative-strategist.yaml) | Ad creative, testing programs | Creative launches, ad fatigue refreshes |

### 💼 Sales Division

| Agent | Specialty | When to Use |
|-------|-----------|-------------|
| [Outbound Strategist](universal-agents/sales/agent/sales-outbound-strategist.yaml) | Signal-based prospecting | Pipeline building, ICP targeting |
| [Deal Strategist](universal-agents/sales/agent/sales-deal-strategist.yaml) | MEDDPICC, competitive positioning | Deal scoring, win strategies |
| [Sales Engineer](universal-agents/sales/agent/sales-engineer.yaml) | Technical demos, POCs | Technical demos, POC scoping |

### 📢 Marketing Division

| Agent | Specialty | When to Use |
|-------|-----------|-------------|
| [Growth Hacker](universal-agents/marketing/agent/marketing-growth-hacker.yaml) | Rapid user acquisition | Viral loops, user acquisition |
| [Content Creator](universal-agents/marketing/agent/marketing-content-creator.yaml) | Multi-platform content | Content strategy, copywriting |
| [Social Media Strategist](universal-agents/marketing/agent/marketing-social-media-strategist.yaml) | Cross-platform strategy | Social strategy, campaigns |

### 📊 Product Division

| Agent | Specialty | When to Use |
|-------|-----------|-------------|
| [Product Manager](universal-agents/product/agent/product-manager.yaml) | Full lifecycle product ownership | Discovery, PRDs, roadmap, GTM |
| [Product Analyst](universal-agents/product/agent/product-analyst.yaml) | Metrics, experimentation | Metrics design, A/B testing, funnels |

### 🛠 DevOps Division

| Agent | Specialty | When to Use |
|-------|-----------|-------------|
| [Kubernetes Deployment Specialist](universal-agents/devops/deployment/kubernetes-deployment.yaml) | K8s, Helm, ArgoCD | K8s manifests, Helm charts, ArgoCD |
| [Terraform Module Builder](universal-agents/devops/agent/devops-terraform-module-builder.yaml) | Terraform modules | Module design, registry publishing |
| [CI/CD Pipeline Optimizer](universal-agents/devops/agent/ci-pipeline-optimizer.yaml) | CI/CD pipelines | Pipeline optimization, caching, parallelization |

### 🔒 Security Division

| Agent | Specialty | When to Use |
|-------|-----------|-------------|
| [API Security Engineer](universal-agents/security/agent/api-security-engineer.yaml) | API auth, rate limiting | Auth, rate limiting, threat modeling |
| [Security Scanner](universal-agents/security/agent/security-trivy-agent.yaml) | Container/image scanning | Trivy, Grype, Syft integration |
| [Compliance Scanner](universal-agents/security/agent/compliance-scanner.yaml) | SOC2, PCI, GDPR | Audit prep, evidence collection |

### 🧪 Testing Division

| Agent | Specialty | When to Use |
|-------|-----------|-------------|
| [Playwright E2E Automator](universal-agents/testing/agent/testing-playwright-e2e-automator.yaml) | E2E testing | E2E test suites, visual regression |
| [Load Testing Engineer](universal-agents/testing/agent/testing-load-testing-engineer.yaml) | k6, Locust, performance | Load testing, stress testing |
| [Security Testing Engineer](universal-agents/testing/agent/testing-security-testing-engineer.yaml) | Security testing | SAST/DAST, penetration testing |

---

## 🛠 Skill Categories

### 🛠 Tool Workflow Skills

| Skill | Description |
|-------|-------------|
| [Terraform Infrastructure](universal-agents/devops/skill/terraform-infrastructure.yaml) | Infrastructure as code with Terraform |
| [Docker Deployment](universal-agents/devops/skill/docker-deployment.yaml) | Container deployment workflows |
| [Kubernetes Deployment](universal-agents/devops/skill/kubernetes-deployment.yaml) | K8s deployment patterns |
| [CI/CD Pipeline](universal-agents/devops/skill/ci-cd-pipeline.yaml) | CI/CD pipeline patterns |

### 🔒 Security & Compliance Skills

| Skill | Description |
|-------|-------------|
| [Trivy Security Scanner](universal-agents/security/skill/trivy-security-scanner.yaml) | Container vulnerability scanning |
| [Semgrep Security](universal-agents/security/skill/semgrep-security.yaml) | Static analysis security rules |
| [SOC2 Compliance](universal-agents/security/skill/soc2-compliance.yaml) | SOC2 audit preparation |

### 🔧 Pattern & Architecture Skills

| Skill | Description |
|-------|-------------|
| [Circuit Breaker Pattern](universal-agents/patterns/skill/circuit-breaker-pattern.yaml) | Resilience patterns |
| [Sidecar Pattern](universal-agents/patterns/skill/sidecar-pattern.yaml) | Sidecar proxy patterns |
| [Adapter Pattern](universal-agents/patterns/skill/adapter-pattern.yaml) | Interface adaptation |

---

## 📦 Installation Examples

### For Claude Code
```bash
# Agents
cp -r platform-agents/claude_code/.claude/agents/* ~/.claude/agents/
# Skills
cp -r platform-agents/claude_code/.claude/skills/* ~/.claude/skills/
```

### For Cursor
```bash
cp -r platform-agents/cursor/* .cursor/rules/
```

### For GitHub Copilot
```bash
cp -r platform-agents/github_copilot/.github .github/
```

### For Windsurf
```bash
cp -r platform-agents/windsurf/* .windsurf/rules/
```

### For OpenCode
```bash
opencode plugin install ./platform-agents/opencode
```

---

## 🔧 Key Commands

```bash
# Validate all YAMLs (0 violations required)
python scripts/schema-check.py

# Regenerate JSON definitions from YAML
python scripts/yaml-to-json.py --inplace --wiring skills/wiring.json

# Generate per-platform marketplace manifests
python scripts/generate-marketplaces.py

# Convert single platform
python scripts/universal-converter.py --platforms windsurf --quiet

# Run tests
pytest -q tests
```

---

## 🏗 Project Structure

```
Kdesk-Catalog/
├── universal-agents/          # ← EDIT THESE (source of truth)
│   ├── ml/                    # 501 agents, 543 skills
│   ├── api/                   # 14 agents, 494 skills
│   ├── devops/                # 38 agents, 142 skills
│   ├── backend/               # 51 agents, 67 skills
│   ├── security/              # 31 agents, 66 skills
│   ├── code-quality/          # 46 agents, 73 skills
│   ├── cloud/                 # 27 agents, 22 skills
│   ├── database/              # 28 agents, 44 skills
│   ├── frontend/              # 31 agents, 27 skills
│   ├── testing/               # 24 agents, 52 skills
│   ├── data/                  # 26 agents, 32 skills
│   ├── monitoring/            # 10 agents, 14 skills
│   ├── sre/                   # 7 agents, 14 skills
│   ├── infrastructure/        # 8 agents, 19 skills
│   ├── finops/                # 7 agents, 12 skills
│   ├── messaging/             # 7 agents, 9 skills
│   ├── compliance/            # 9 agents, 19 skills
│   ├── patterns/              # 10 agents, 10 skills
│   ├── mobile/                # 15 agents, 14 skills
│   ├── devtools/              # 12 agents, 30 skills
│   ├── networking/            # 5 agents, 12 skills
│   ├── personas/              # ADD YOUR PERSONAS HERE
│   ├── gcp/skill/             # ADD YOUR SKILL PACKS HERE
│   └── ... (40+ more categories)
├── scripts/                   # Automation (converter, validators)
├── reports/                   # Status reports
├── platform-agents/           # AUTO-GENERATED (gitignored)
├── schemas/universal-agent.schema.json
├── tests/
└── README.md                  # You are here
```

---

## ✅ Verification Status

- ✅ **Schema validation** — 0 violations across 3,093 files
- ✅ **JSON regeneration** — deterministic with skill wiring
- ✅ **Tests** — `test_wire_skills.py`, `test_yaml_to_json.py`, `test_marketplaces.py` pass

---

## 🏥 Kdesk Doctor

Kdesk Doctor is a developer-facing compatibility, diagnosis, repair, and validation system for AI agent/skill projects.

### Quick Start

```bash
# Scan project for AI configuration
kdesk doctor --mode scan --project-root ./my-project

# Diagnose compatibility for a target platform
kdesk doctor --mode diagnose --platform claude_code --project-root ./my-project --json

# Fix issues (dry-run preview)
kdesk doctor --mode fix --platform claude_code --project-root ./my-project --dry-run

# Apply fixes
kdesk doctor --mode fix --platform claude_code --project-root ./my-project

# Full pipeline: diagnose + fix
kdesk doctor --mode diagnose --platform claude_code --project-root ./my-project --fix

# CI mode with threshold
kdesk doctor --mode diagnose --platform claude_code --project-root ./my-project --ci --threshold 90 --json
```

### Features

- **Project Scanner**: Discovers AI development configuration across 45+ platforms
- **Compatibility Engine**: Analyzes components against platform capabilities with severity levels (CRITICAL, ERROR, WARNING, INFO)
- **Compatibility Score**: Deterministic scoring (0-100) based on errors, warnings, and unsupported features
- **Automatic Fix Engine**: Safe fixes with backups (add_field, remove_field, replace_tool, replace_value)
- **Secret Redaction**: Automatic redaction of API keys, tokens, passwords in reports
- **CI Mode**: Exit codes based on health threshold for pipeline integration
- **JSON Output**: Machine-readable output for all modes

---

## ✅ Verification Status

- ✅ **Schema validation** — 0 violations across 3,093 files
- ✅ **JSON regeneration** — deterministic with skill wiring
- ✅ **Tests** — `test_wire_skills.py`, `test_yaml_to_json.py`, `test_marketplaces.py` pass

---

## 📜 License

MIT © Mehul Wagde

---

> **Built with ❤️ for AI developers everywhere** — Transform your workflow with specialized AI experts at your fingertips.