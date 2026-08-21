# Kdesk-Catalog

**Universal AI Agents & Skills Registry** — 2,909 definitions that convert once to 45+ platforms (Claude Code, Cursor, GitHub Copilot, Windsurf, OpenCode, Codex CLI, Gemini CLI, Zed, Cline, Goose, and 35 more).

| Type | Count | Status |
|------|-------|--------|
| **Agents** | 1,766 | Persona, specialist, automation |
| **Skills** | 1,143 | Tool workflows, patterns, integrations |
| **Total** | **2,909** | **2,833 curated / 76 template / 0 unknown** |
| **Platforms** | **45+** | Auto-generated from single YAML source |

**Source of truth:** `universal-agents/` (YAML)  
**Output:** `platform-agents/` (130k+ files, auto-generated, gitignored)  
**Trust layer:** `reports/curation-status.json` (per-file tier)

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

> Each platform folder has its own `README.md` with exact instructions.

---

## Browse Agents & Skills

### By Category (Agents + Skills)

| Domain | Agents | Skills | What You Get |
|--------|--------|--------|--------------|
| **ML & AI** | 501 | 543 | Training, inference, MLOps, LLMs, RAG, vector DBs, pipelines |
| **API** | 14 | 494 | REST, GraphQL, gRPC, WebSockets, AsyncAPI, contracts, auth, caching, rate-limiting, versioning |
| **DevOps** | 38 | 142 | Git, Docker, K8s, Terraform, Helm, ArgoCD, CI/CD, pipelines |
| **Backend** | 51 | 67 | Python, Node.js, Go, Rust, Java, .NET, FastAPI, Django, Flask, Express |
| **Security** | 31 | 66 | Trivy, Gitleaks, Semgrep, Snyk, Vault, Kubescape, Falco, Cosign, mTLS |
| **Code Quality** | 46 | 73 | ESLint, Prettier, Ruff, Black, MyPy, Clippy, SonarQube, Hadolint, linting |
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

---

## Classification Breakdown

### Agent Types

| Type | Count | Description | Examples |
|------|-------|-------------|----------|
| **Persona** | ~200 | Role-based experts with full workflows | `ml-engineer`, `api-architect`, `sre-engineer`, `devops-engineer` |
| **Specialist** | ~1,200 | Deep domain tool operators | `terraform-module-builder`, `kubernetes-deployment-specialist`, `api-security-engineer` |
| **Automation** | ~366 | Pipeline/workflow executors | `ci-pipeline-optimizer`, `deployment-strategy-engineer`, `background-job-scheduler` |

### Skill Types

| Type | Count | Description | Examples |
|------|-------|-------------|----------|
| **Tool Workflow** | ~600 | End-to-end CLI tool operations | `terraform-infrastructure`, `docker-deployment`, `kubernetes-deployment` |
| **Pattern/Architecture** | ~200 | Design patterns & system architectures | `circuit-breaker-pattern`, `sidecar-pattern`, `adapter-pattern` |
| **Integration** | ~200 | Third-party API connections | `stripe-payments`, `github-webhooks`, `slack-bot` |
| **Security/Compliance** | ~143 | Hardening, scanning, audit | `trivy-security-scanner`, `semgrep-security`, `soc2-compliance` |

### Curation Tiers

| Tier | Count | Trust Level | How to Verify |
|------|-------|-------------|---------------|
| **Curated** | 2,833 | ✅ Hand-curated: real commands, official docs, unique instructions | `reports/curation-status.json` → `"tier": "curated"` |
| **Template** | 76 | ⚠️ Generated: conceptual/architectural (no CLI) | `reports/curation-status.json` → `"tier": "template"` |
| **Unknown** | 0 | ❌ Unparseable | None (all fixed) |

> **Tip:** Every `universal-agents/**/*.yaml` starts as untrusted. A definition is trustworthy when it appears as `curated` in `reports/curation-status.json` OR you've read and verified its commands.

---

## Example: Find & Use an Agent

### Find a Kubernetes Deployment Specialist

```bash
# Search by category
find universal-agents -name "*kubernetes*deployment*" -type f

# Or by capability
grep -r "kubernetes-deployment" universal-agents/ --include="*.yaml" | head -5
```

**Result:** `universal-agents/devops/deployment/kubernetes-deployment.yaml`

### Install to Claude Code

```bash
# After generating
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

### What's Inside (Skill Structure)

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

# Classify every definition into curated/template tiers
python scripts/curate-tier.py --quiet

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
├── scripts/                   # Automation (converter, validators, curate-tier)
├── reports/                   # Curation status (trust layer)
├── platform-agents/           # AUTO-GENERATED (gitignored)
├── schemas/universal-agent.schema.json
├── tests/
└── README.md                  # You are here
```

---

## Verification Status

- ✅ `schema-check.py` — 0 violations across 2,909 files
- ✅ `yaml-to-json.py` — deterministic JSON regeneration with skill wiring
- ✅ `curate-tier.py` — 2,833 curated / 76 template / 0 unknown
- ✅ Tests: `test_wire_skills.py`, `test_yaml_to_json.py`, `test_marketplaces.py` — pass

---

## License

MIT © Mehul Wagde