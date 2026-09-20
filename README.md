# Kdesk-Catalog

**Author:** Kdesk  
**License:** MIT  
**Status:** Production-ready pipeline; 2,909 agents/skills verified across 45 AI coding platforms

---

## What Is This?

A **universal registry** of AI agents and skills that converts **once** to **45 platforms** (Claude Code, Cursor, GitHub Copilot, Windsurf, OpenCode, Codex CLI, Gemini CLI, Zed, Cline, and 36 more).

| Type | Count |
|------|-------|
| **Agents** | 1,766 |
| **Skills** | 1,143 |
| **Total** | **2,909** |
| **Platforms** | **45** |

**Source of truth:** `universal-agents/` (YAML files)  
**Output:** `platform-agents/` (130,954 files, auto-generated, gitignored)

---

## Quick Start

### 1. Clone & Generate

```bash
git clone https://github.com/yourusername/Kdesk-Catalog
cd Kdesk-Catalog

# Generate for ALL platforms (~15 min, 130k files)
python scripts/universal-converter.py --platforms all --output ./platform-agents --universal-dir universal-agents

# Or just one platform (fast)
python scripts/universal-converter.py --platforms claude_code --output ./claude-agents --universal-dir universal-agents
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

## Add Your Own Agents & Skills

The power of Kdesk-Catalog: **write YAML once → works everywhere**.

### Example: Persona Agent (like agency-agents)

Create `universal-agents/personas/ml-engineer.yaml`:

```yaml
name: ml-engineer
display_name: "ML Engineer"
category: personas
subcategory: ml
description: "End-to-end ML: data → training → deployment → monitoring"
version: "1.0.0"
capabilities:
  - name: "Pipeline Design"
    description: "Build reproducible ML pipelines"
    commands:
      - "dvc init && dvc add data/"
      - "mlflow ui --port 5000"
      - "kubectl apply -f k8s/model-server.yaml"
    examples:
      - "dvc repro train.dvc"
    parameters: []
knowledge:
  - title: "MLOps Best Practices"
    type: documentation
    source: "https://ml-ops.org"
    description: "Production ML patterns"
instructions: |
  You are a senior ML engineer. Think in pipelines.
  - Validate data first (Great Expectations)
  - Track experiments (MLflow)
  - Deploy via containers (Docker/K8s)
  - Monitor drift (Prometheus + Evidently)
platforms:
  claude_code:
    tools: [Bash, Read, Write, Edit, Glob, Grep]
    model: inherit
```

### Example: Skill Pack (like google/skills)

Create `universal-agents/gcp/skill/gke-basics.yaml`:

```yaml
name: gke-basics
display_name: "GKE Basics"
category: cloud
subcategory: kubernetes
description: "Deploy, scale, and operate Google Kubernetes Engine clusters"
version: "1.0.0"
tags: [gcp, kubernetes, gke]
prerequisites: [gcloud]
capabilities:
  - name: "Cluster Creation"
    description: "Create Autopilot or zonal GKE clusters"
    commands:
      - "gcloud container clusters create-auto CLUSTER --region=REGION"
      - "gcloud container clusters create CLUSTER --zone=ZONE"
    examples:
      - "gcloud container clusters create-auto prod --region=us-central1"
    parameters:
      - name: cluster
        type: string
        description: Cluster name
        required: true
      - name: region
        type: string
        description: GCP region
        required: false
knowledge:
  - title: "GKE Documentation"
    type: documentation
    source: "https://cloud.google.com/kubernetes-engine/docs"
    description: "Official GKE guides"
instructions: |
  You are a GKE specialist. Use Autopilot for most workloads.
  Prefer Workload Identity. Enable GKE Gateway for ingress.
platforms:
  claude_code:
    tools: [Bash, Read, Write]
    model: inherit
```

### Then Regenerate

```bash
python scripts/universal-converter.py --platforms all --output ./platform-agents --universal-dir universal-agents
```

**Both examples now work on all 45 platforms automatically.**

---

## Built-in Templates

Already included (copy and customize):

```
universal-agents/patterns/template-skill.yaml           # Skill template
universal-agents/patterns/agent/patterns-template-agent.yaml  # Agent template
```

---

## Categories (Agents + Skills per Domain)

| Domain | Agents | Skills | Description |
|--------|--------|--------|-------------|
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
| **Specialized** | 16 | 67 | AR/VR, blockchain, computer vision, climate, quantum, robotics, speech, web3, etc. |

> **Total: 1,766 agents + 1,143 skills = 2,909 universal definitions**

---

## Key Commands

```bash
# Validate all YAMLs (0 violations required)
python scripts/schema-check.py

# Full verification
python scripts/verify-all.py

# Convert single platform
python scripts/universal-converter.py --platforms claude_code --output ./out --universal-dir universal-agents

# Run tests
pytest -q tests
```

---

## Project Structure (Simplified)

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
│   ├── patterns/              # 10 agents, 10 skills + templates
│   ├── mobile/                # 15 agents, 14 skills
│   ├── devtools/              # 12 agents, 30 skills
│   ├── networking/            # 5 agents, 12 skills
│   ├── personas/              # ← ADD YOUR PERSONAS HERE
│   ├── gcp/skill/             # ← ADD YOUR SKILL PACKS HERE
│   └── ... (40+ more categories)
├── scripts/                   # Automation (converter, validators, etc.)
├── platform-agents/           # AUTO-GENERATED (gitignored)
├── schemas/universal-agent.schema.json
├── tests/
└── README.md                  # You are here
```

---

## Quality Gates (All Pass)

- ✅ Schema validation: 0 violations on 2,909 files
- ✅ Unique names & command sets
- ✅ Real CLI commands (no templates)
- ✅ Platform format correctness (all 45)
- ✅ 135 unit tests passing

---

## Known Limits (Honest)

- ~95% template-generated; curation ongoing
- 53/1,143 skills are conceptual (no CLI binary)
- 204 near-duplicate families flagged for review
- `platform-agents/` is gitignored — regenerate with converter

---

## License

MIT © Kdesk