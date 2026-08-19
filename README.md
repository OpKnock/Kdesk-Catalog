# Kdesk-Catalog

**Author:** Mehul Wagde  
**License:** MIT  
**Repo:** https://github.com/OpKnock/Kdesk-Catalog

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

## Trust & Curation Status

This catalog is **not** fully hand-authored. It was bulk-generated, and curation is an ongoing, tracked effort. Read the numbers before you trust a definition.

| Tier | Count |
|------|-------|
| **Curated** (hand-written: real commands, real knowledge links, unique text) | 227 (7.8%) |
| **Template** (generated: placeholder commands, frozen timestamps, boilerplate) | 2,682 (92.2%) |

- Machine-readable per-file classification: `reports/curation-status.json`
- Human-readable breakdown by category and fingerprint: `reports/CURATION-STATUS.md`
- Classifier: `scripts/curate-tier.py` (deterministic, fingerprint-based)

How to use this: every `universal-agents/**/*.yaml` starts untrusted. A definition is trustworthy once it (a) appears as `curated` in `reports/curation-status.json` **or** (b) you have read it and verified its commands yourself. Do not copy commands from template-tier files into production setups without checking them.

Curated example (this repo's own quality bar):

- `universal-agents/ml/rag/rag.yaml` — RAG pipeline: build → serve → query
- `universal-agents/ml/rag/ml-rag-python.yaml` — full LangChain/LlamaIndex stack
- `universal-agents/ml/rag/ml-rag-node.yaml` — Node.js + LangChain.js stack
- `universal-agents/ml/rag/ml-rag-deploy.yaml` — vLLM/Llama.cpp serving with health-gated rollout

Each curated file: real executable CLI commands (curl, docker, python), real official-documentation links, per-capability `commands` / `examples` / `parameters`, and expert `instructions` — not placeholders.

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

## Add Your Own Agents & Skills

The power of Kdesk-Catalog: **write YAML once → works everywhere**.

### Example: Persona Agent

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

### Example: Skill Pack

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
python scripts/universal-converter.py --platforms all --quiet
```

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
# Validate all source YAMLs (0 violations required)
python scripts/schema-check.py

# Classify every definition into curated / template tiers
python scripts/curate-tier.py --quiet

# Regenerate JSON definitions (agents/, skills/, workflows/) from YAML
python scripts/yaml-to-json.py --inplace --wiring skills/wiring.json

# Regenerate per-platform marketplace manifests + report
python scripts/generate-marketplaces.py

# Convert single platform
python scripts/universal-converter.py --platforms windsurf --quiet

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
├── scripts/                   # Automation (converter, validators, curate-tier)
├── reports/                   # Curation status (trust layer)
├── platform-agents/           # AUTO-GENERATED (gitignored)
├── schemas/universal-agent.schema.json
├── tests/
└── README.md                  # You are here
```

---

## Verification (Honest)

- ✅ `schema-check.py` — 0 violations across 2,909 files
- ✅ `yaml-to-json.py` — deterministic JSON regeneration with skill wiring
- ✅ `curate-tier.py` — deterministic curated/template classification
- ✅ `test_wire_skills.py`, `test_yaml_to_json.py`, `test_marketplaces.py` — pass
- ⚠️ Platform-format tests (`test_platform_spec.py`) need a full `--platforms all` conversion first (~15 min); they check the generated output, not the YAMLs
- ⚠️ `deep-audit.py` currently crashes on an unhashable-command edge case (pre-existing) — fix in progress

---

## Known Limits (Honest)

- 92% of definitions are template-tier (2,682 of 2,909) — bulk-generated, needs curation
- Most template-tier files carry the same frozen `created_at` timestamp and `template_author` fingerprints (2,616 files)
- ~1,483 files link to the generic Kdesk agents page rather than topic-specific docs
- 535 placeholder-style commands flagged by `curate-tier.py`
- 53/1,143 skills are conceptual (no CLI binary)
- `platform-agents/` is gitignored — regenerate with the converter

---

## License

MIT © Mehul Wagde