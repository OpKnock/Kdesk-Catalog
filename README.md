# Kdesk-Catalog

**Universal AI Agents & Skills Registry** — 2,909 production-ready definitions that convert once to 45+ platforms.

[![Platforms](https://img.shields.io/badge/platforms-45%2B-blue)](https://github.com/OpKnock/Kdesk-Catalog)
[![Agents](https://img.shields.io/badge/agents-1,766-green)](https://github.com/OpKnock/Kdesk-Catalog/tree/main/universal-agents)
[![Skills](https://img.shields.io/badge/skills-1,143-green)](https://github.com/OpKnock/Kdesk-Catalog/tree/main/universal-agents)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## Overview

Kdesk-Catalog is a hand-curated registry of AI agents and skills. Each definition is written once in YAML and automatically converts to work across **45+ platforms** — including Claude Code, Cursor, GitHub Copilot, Windsurf, OpenCode, Codex CLI, Gemini CLI, Zed, Cline, Goose, and more.

**Source of truth:** `universal-agents/` — every agent and skill is a single YAML file with real commands, official documentation links, and expert instructions.

**Output:** `platform-agents/` — auto-generated platform-specific formats (gitignored, regenerated on demand).

---

## Quick Start

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

## Catalog Contents

### By Domain

| Domain | Agents | Skills | Description |
|--------|--------|--------|-------------|
| **ML & AI** | 501 | 543 | Training, inference, MLOps, LLMs, RAG, vector DBs, pipelines |
| **API** | 14 | 494 | REST, GraphQL, gRPC, WebSockets, AsyncAPI, contracts, auth, caching, rate-limiting, versioning |
| **DevOps** | 38 | 142 | Git, Docker, K8s, Terraform, Helm, ArgoCD, CI/CD, pipelines |
| **Backend** | 51 | 67 | Python, Node.js, Go, Rust, Java, .NET, FastAPI, Django, Flask, Express |
| **Security** | 31 | 66 | Trivy, Gitleaks, Semgrep, Snyk, Vault, Kubescape, Falco, Cosign, mTLS |
| **Code Quality** | 46 | 73 | ESLint, Prettier, Ruff, Black, MyPy, Clippy, SonarQube, Hadolint |
| **Cloud** | 27 | 22 | AWS, GCP, Azure, Firebase, Vercel, Netlify, Fly.io, Railway, Render |
| **Database** | 28 | 44 | PostgreSQL, MySQL, MongoDB, Redis, Elasticsearch, Cassandra, migrations, replication |
| **Frontend** | 31 | 27 | React, Vue, Svelte, Angular, Next.js, Remix, Astro, Tailwind |
| **Testing** | 24 | 52 | Jest, pytest, Playwright, Cypress, k6, Artillery, Robot Framework, Bats |
| **Data & Analytics** | 26 | 32 | Airflow, dbt, Spark, Flink, Kafka, Snowflake, Databricks, visualization |
| **Monitoring & SRE** | 17 | 28 | Prometheus, Grafana, Datadog, Sentry, Jaeger, OpenTelemetry, runbooks, chaos |
| **Infrastructure** | 17 | 19 | Nginx, HAProxy, DNS, Cert-Manager, Consul, Vault, networking |
| **FinOps** | 7 | 12 | AWS/GCP/Azure cost optimization, Infracost |
| **Messaging** | 7 | 9 | Kafka, RabbitMQ, NATS, Pulsar, Redis Streams, MQTT |
| **Compliance** | 9 | 19 | SOC2, PCI, GDPR, HIPAA, ISO27001, CIS |
| **Patterns** | 10 | 10 | Design patterns (Singleton, Factory, Builder, Template, etc.) |
| **Mobile** | 15 | 14 | Flutter, React Native, Kotlin, Swift |
| **DevTools** | 12 | 30 | Git, Docker, nvm, Volta, Homebrew, Copilot, Windsurf, OpenCode |
| **Specialized** | 16 | 67 | AR/VR, blockchain, computer vision, climate, quantum, robotics, speech, web3 |

**Total: 1,766 agents + 1,143 skills = 2,909 universal definitions**

---

## Agent & Skill Types

### Agent Types

| Type | Description | Examples |
|------|-------------|----------|
| **Persona Agents** | Role-based experts with full end-to-end workflows | `ml-engineer`, `api-architect`, `sre-engineer`, `devops-engineer` |
| **Specialist Agents** | Deep domain tool operators | `terraform-module-builder`, `kubernetes-deployment-specialist`, `api-security-engineer` |
| **Automation Agents** | Pipeline/workflow executors | `ci-pipeline-optimizer`, `deployment-strategy-engineer`, `background-job-scheduler` |

### Skill Types

| Type | Description | Examples |
|------|-------------|----------|
| **Tool Workflow Skills** | End-to-end CLI tool operations | `terraform-infrastructure`, `docker-deployment`, `kubernetes-deployment` |
| **Pattern & Architecture Skills** | Design patterns & system architectures | `circuit-breaker-pattern`, `sidecar-pattern`, `adapter-pattern` |
| **Integration Skills** | Third-party API connections | `stripe-payments`, `github-webhooks`, `slack-bot` |
| **Security & Compliance Skills** | Hardening, scanning, audit | `trivy-security-scanner`, `semgrep-security`, `soc2-compliance` |

---

## Example: Find & Use an Agent

### Find a Kubernetes Deployment Specialist

```bash
# Search by capability
grep -r "kubernetes-deployment" universal-agents/ --include="*.yaml" | head -5
```

**Result:** `universal-agents/devops/deployment/kubernetes-deployment.yaml`

### Install to Claude Code

```bash
# After generating platform files
cp platform-agents/claude_code/.claude/agents/devops/deployment/kubernetes-deployment.yaml ~/.claude/agents/
cp platform-agents/claude_code/.claude/skills/devops/kubernetes/* ~/.claude/skills/
```

### Use in Your Session

```
/kubernetes-deployment create production --replicas=5 --image=myapp:v2.1
/kubernetes-deployment rollout status
/kubernetes-deployment scale --replicas=10
```

---

## Example: Find & Use a Skill

### Find Terraform Infrastructure Skill

```bash
find universal-agents -path "*/terraform*" -name "*.yaml" | grep -v test
```

**Result:** `universal-agents/terraform/terraform-infrastructure.yaml`

### Skill Structure (What's Inside)

```yaml
name: terraform-infrastructure
display_name: "Terraform Infrastructure"
category: devops
subcategory: infrastructure
capabilities:
  - name: "infrastructure-as-code"
    commands:
      - terraform init
      - terraform plan -out=tfplan
      - terraform apply tfplan
    examples:
      - terraform init && terraform plan
    parameters:
      - name: workspace
        type: string
        description: Terraform workspace (dev/staging/prod)
knowledge:
  - title: "Terraform Documentation"
    source: "https://developer.hashicorp.com/terraform/docs"
instructions: |
  You are a Terraform expert. Manage infrastructure as code...
```

---

## Add Your Own Agent or Skill

### 1. Create Agent YAML

```bash
cat > universal-agents/personas/my-engineer.yaml << 'EOF'
name: my-engineer
display_name: "My Engineer"
category: personas
subcategory: backend
description: "Custom backend engineer for my stack"
version: "1.0.0"
tags: [backend, api, python]
capabilities:
  - name: "API Development"
    description: "Build REST APIs with FastAPI"
    commands:
      - "fastapi dev main.py"
      - "pytest tests/"
    examples:
      - "fastapi dev main.py --port 8000"
    parameters:
      - name: port
        type: integer
        default: 8000
knowledge:
  - title: "FastAPI Documentation"
    source: "https://fastapi.tiangolo.com/"
    description: "Modern, fast web framework"
instructions: |
  You are a backend engineer specializing in FastAPI.
  - Use Pydantic for validation
  - Use async/await for I/O
  - Write tests with pytest
platforms:
  claude_code:
    tools: [Bash, Read, Write, Edit, Glob, Grep]
    model: inherit
EOF
```

### 2. Create Skill YAML

```bash
cat > universal-agents/my-tools/skill/docker-build.yaml << 'EOF'
name: docker-build
display_name: "Docker Build"
category: devtools
subcategory: container
description: "Build, test, and push Docker images"
version: "1.0.0"
prerequisites: [docker]
capabilities:
  - name: "multi-stage-build"
    description: "Build optimized multi-stage Docker images"
    commands:
      - "docker build --target builder -t myapp:builder ."
      - "docker build --target runtime -t myapp:latest ."
      - "docker push myapp:latest"
    examples:
      - "docker build -t myapp:v1.0 . && docker push myapp:v1.0"
    parameters:
      - name: tag
        type: string
        description: Image tag
        required: true
knowledge:
  - title: "Docker Best Practices"
    source: "https://docs.docker.com/develop/develop-images/dockerfile_best-practices/"
instructions: |
  You are a Docker expert. Build minimal, secure images.
  - Use multi-stage builds
  - Pin base image digests
  - Scan with trivy before push
platforms:
  claude_code:
    tools: [Bash, Read, Write, Edit]
    model: inherit
EOF
```

### 3. Regenerate & Install

```bash
python scripts/universal-converter.py --platforms all --quiet
# Then copy to your platform (see Quick Start table)
```

---

## Key Commands

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

## Project Structure

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

## Verification Status

- ✅ **Schema validation** — 0 violations across 2,909 files
- ✅ **JSON regeneration** — deterministic with skill wiring
- ✅ **Tests** — `test_wire_skills.py`, `test_yaml_to_json.py`, `test_marketplaces.py` pass

---

## Kdesk Doctor

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

- **Project Scanner**: Discovers AI development configuration across 45+ platforms (Claude Code, Cursor, OpenCode, Codex CLI, Gemini CLI, etc.)
- **Compatibility Engine**: Analyzes components against platform capabilities with severity levels (CRITICAL, ERROR, WARNING, INFO)
- **Compatibility Score**: Deterministic scoring (0-100) based on errors, warnings, and unsupported features
- **Automatic Fix Engine**: Safe fixes with backups (add_field, remove_field, replace_tool, replace_value)
- **Secret Redaction**: Automatic redaction of API keys, tokens, passwords in reports
- **CI Mode**: Exit codes based on health threshold for pipeline integration
- **JSON Output**: Machine-readable output for all modes

### Demo

```bash
# Scan the demo project
kdesk doctor --mode scan --project-root ./demo

# Diagnose compatibility issues
kdesk doctor --mode diagnose --platform claude_code --project-root ./demo --json

# Fix issues (dry-run)
kdesk doctor --mode fix --platform claude_code --project-root ./demo --dry-run --json

# Apply fixes
kdesk doctor --mode fix --platform claude_code --project-root ./demo --json

# Full pipeline with CI
kdesk doctor --mode diagnose --platform claude_code --project-root ./demo --ci --threshold 90 --json
```

---

## License

MIT © Kdesk