# Kdesk-Catalog

**Author:** Mehul Wagde  
**License:** MIT  
**Status:** Pipeline production-ready; content curation verified (L1–L3, see [Known Limits](#known-limits))

The largest catalog of production-ready AI agents and skills with **real, working CLI commands for 32 FULLY_SUPPORTED AI coding platforms** (the big six: Claude Code, Cursor, GitHub Copilot, Windsurf, OpenCode, generic — plus OpenAI Codex CLI, Antigravity/Gemini CLI, Goose, Aider, Kilo Code, Trae, OpenHands, Qwen Code, Devin, Cline, Roo Code, Kiro, Junie, Zed, Amp, Factory Droid, Crush, MCPJam, Mux, Pi, Qoder, CodeBuddy, Command Code, Neovate, plus 13 PARTIALLY_SUPPORTED platforms requiring manual config merge, and 1 DEPRECATED platform).

## 📊 Project Statistics

| Type | Count | Description |
|------|-------|-------------|
| **Universal Agents** | 1,766 | Real CLI commands for development tasks |
| **Universal Skills** | 1,143 | Real workflows and best practices |
| **Total Universal** | **2,909** | Schema-validated + pipeline-verified (see Known Limits) |
| **Platforms** | **45** | One source of truth, every format |
| **Platform Files** | **130,954** | Regenerated on demand: ~2,910 per platform × 45 (2,909 items + per-platform READMEs/manifests/registry) |

### Supported Platforms

| Platform | Format | Install Target | Support Level |
|----------|--------|----------------|---------------|
| **Claude Code** | `.md` (YAML frontmatter) | `~/.claude/agents/` + `~/.claude/skills/` | **FULLY_SUPPORTED** |
| **Cursor** | `.mdc` | `.cursor/rules/` | **FULLY_SUPPORTED** |
| **GitHub Copilot** | `.instructions.md` (frontmatter + applyTo) | `.github/instructions/` + `.github/copilot-instructions.md` | **FULLY_SUPPORTED** |
| **Windsurf** | `.json` | `.windsurf/` | **FULLY_SUPPORTED** |
| **OpenCode** | `.json` | Plugin system | **FULLY_SUPPORTED** |
| **Generic** | `.json` | Any LLM agent | **FULLY_SUPPORTED** |
| **OpenAI Codex CLI** | `SKILL.md` | `.agents/skills/` | **FULLY_SUPPORTED** |
| **Gemini CLI (Google)** | `SKILL.md` | `.gemini/skills/` | **FULLY_SUPPORTED** |
| **Antigravity (Google)** | `SKILL.md` | `.agent/skills/` | **FULLY_SUPPORTED** |
| **Devin (Cognition)** | `SKILL.md` | `.devin/skills/` | **FULLY_SUPPORTED** |
| **Zed** | `SKILL.md` | `.agents/skills/` | **FULLY_SUPPORTED** |
| **Cline** | `SKILL.md` | `.clinerules/skills/` | **FULLY_SUPPORTED** |
| **Roo Code** | `SKILL.md` | `.roo/skills/` | **FULLY_SUPPORTED** |
| **Kilo Code** | `SKILL.md` | `.kilocode/skills/` | **FULLY_SUPPORTED** |
| **Trae (ByteDance)** | `SKILL.md` | `.trae/skills/` | **FULLY_SUPPORTED** |
| **Qwen Code (Alibaba)** | `SKILL.md` | `.qwen/skills/` | **FULLY_SUPPORTED** |
| **Kiro (Sublime)** | `SKILL.md` | `.kiro/skills/` | **FULLY_SUPPORTED** |
| **JetBrains Junie** | `SKILL.md` | `.junie/skills/` | **FULLY_SUPPORTED** |
| **Zencoder** | `SKILL.md` | `.agents/skills/` | **FULLY_SUPPORTED** |
| **Amp (Sourcegraph)** | `SKILL.md` | `.agents/skills/` | **FULLY_SUPPORTED** |
| **Factory Droid** | `SKILL.md` | `.factory/skills/` | **FULLY_SUPPORTED** |
| **Crush (Charm)** | `SKILL.md` | `.crush/skills/` | **FULLY_SUPPORTED** |
| **MCPJam** | `SKILL.md` | `.mcpjam/skills/` | **FULLY_SUPPORTED** |
| **Mux** | `SKILL.md` | `.mux/skills/` | **FULLY_SUPPORTED** |
| **Pi** | `SKILL.md` | `.pi/skills/` | **FULLY_SUPPORTED** |
| **Qoder** | `SKILL.md` | `.qoder/skills/` | **FULLY_SUPPORTED** |
| **CodeBuddy** | `SKILL.md` | `.codebuddy/skills/` | **FULLY_SUPPORTED** |
| **Command Code** | `SKILL.md` | `.commandcode/skills/` | **FULLY_SUPPORTED** |
| **Neovate** | `SKILL.md` | `.neovate/skills/` | **FULLY_SUPPORTED** |
| **Grok Build (xAI)** | `.md` rules | `.grok/rules/` | **PARTIALLY_SUPPORTED** |
| **Amazon Q Developer CLI** | `.md` rules | `.amazonq/rules/` | **PARTIALLY_SUPPORTED** |
| **Augment Code** | `.md` rules | `.augment/rules/` | **PARTIALLY_SUPPORTED** |
| **Firebase Studio** | `.mdc` rules | `.idx/rules/` | **PARTIALLY_SUPPORTED** |
| **Continue** | `.md` rules | `.continue/rules/` | **PARTIALLY_SUPPORTED** |
| **Goose (Block)** | Recipes YAML | `~/.config/goose/recipes/` | **FULLY_SUPPORTED** |
| **Aider** | `.md` conventions | `--read` / `.aider.conf.yml` | **FULLY_SUPPORTED** |
| **OpenHands** | Microagents `.md` | `.openhands/microagents/` | **FULLY_SUPPORTED** |
| **Google Jules** | `AGENTS.md` | repo root | **PARTIALLY_SUPPORTED** |
| **Warp AI** | `WARP.md` | repo root | **PARTIALLY_SUPPORTED** |
| **Void** | config registry | `.void/config.json` | **DEPRECATED** |
| **Cody (Sourcegraph)** | config registry | `.cody/config.json` | **PARTIALLY_SUPPORTED** |
| **Supermaven** | config registry | `.supermaven/config.json` | **PARTIALLY_SUPPORTED** |
| **CodeGPT** | config registry | `.codegpt/config.json` | **PARTIALLY_SUPPORTED** |
| **Tabnine** | config registry | `.tabnine.yaml` | **PARTIALLY_SUPPORTED** |
| **Firebender** | config registry | `firebender.json` | **PARTIALLY_SUPPORTED** |

**Support Level Definitions:**
- **FULLY_SUPPORTED** — Native per-agent/skill file format; each catalog entry generates a separate file in the platform's native format.
- **PARTIALLY_SUPPORTED** — Single-file or config-registry format; the converter emits instruction fragments + a manifest, but the platform requires manual merge into a single config file (e.g., `AGENTS.md`, `.vscode/cody.json`, `firebender.json`).
- **DEPRECATED** — No longer maintained; no native agent-instructions file documented (Void editor is deprecated).

The `SKILL.md` outputs follow the open Agent Skills standard (agentskills.io), so each also works in every other skills-compatible tool (40+ products).

## 📁 Categories

| Category | Agents | Skills | Description |
|----------|--------|--------|-------------|
| **ML** | 1,044 | 0 | Training, inference, deployment, MLOps, LLMs, RAG, vector DBs |
| **API** | 14 | 494 | REST, GraphQL, gRPC, gRPC-Web, WebSockets, AsyncAPI |
| **Backend** | 74 | 44 | Python, Node.js, Go, Rust, Java, .NET, FastAPI, Django, Flask, Express |
| **DevOps** | 116 | 64 | Git, Docker, K8s, Terraform, Helm, ArgoCD, CI/CD |
| **Security** | 60 | 37 | Trivy, Gitleaks, Semgrep, Snyk, Vault, Kubescape, Falco, Cosign |
| **Code Quality** | 50 | 69 | ESLint, Prettier, Ruff, Black, MyPy, Clippy, SonarQube, Hadolint |
| **Testing** | 46 | 30 | Jest, pytest, Playwright, Cypress, k6, Artillery, Robot Framework, Bats |
| **Data** | 50 | 8 | Airflow, dbt, Spark, Flink, Kafka, Snowflake, Databricks |
| **Database** | 53 | 19 | PostgreSQL, MySQL, MongoDB, Redis, Elasticsearch, Cassandra, etc. |
| **Frontend** | 47 | 11 | React, Vue, Svelte, Angular, Next.js, Remix, Astro, Tailwind |
| **Infrastructure** | 25 | 11 | Nginx, HAProxy, DNS, Cert-Manager, Consul, Vault |
| **Cloud** | 38 | 11 | AWS, GCP, Azure, Firebase, Vercel, Netlify, Fly.io, Railway, Render |
| **DevTools** | 15 | 27 | Git, Docker, nvm, Volta, Homebrew, Copilot, Windsurf, OpenCode |
| **SRE** | 17 | 4 | Runbooks, Chaos Engineering, Incident Response |
| **Mobile** | 24 | 5 | Flutter, React Native, Kotlin, Swift |
| **Compliance** | 23 | 5 | SOC2, PCI, GDPR, HIPAA, ISO27001, CIS |
| **Monitoring** | 17 | 7 | Prometheus, Grafana, Datadog, Sentry, Jaeger, OpenTelemetry |
| **FinOps** | 15 | 4 | AWS/GCP/Azure cost optimization, Infracost |
| **Patterns** | 10 | 10 | Design patterns (Singleton, Factory, Builder, etc.) |
| **Networking** | 15 | 2 | Nginx, HAProxy, WireGuard, DNS, Envoy, Traefik |
| **Messaging** | 13 | 3 | Kafka, RabbitMQ, NATS, Pulsar, Redis Streams, MQTT |
| **Skill-only categories** | 0 | 78 | ai, collaboration, community, culture, desktop, embedded, emerging, environment, gaming, healthcare, legal, management, platform, robotics, strategy, web3, and more |

## 🚀 Quick Start

### 1. Clone and Generate Platform Files
```bash
git clone <repo>
cd Kdesk-Catalog
python scripts/universal-converter.py --platforms all --output ./my-agents --universal-dir universal-agents
```

### 2. Install to Your AI Coding Agent

| Platform | Install Command |
|----------|-----------------|
| **Claude Code** | `cp -r platform-agents/claude_code/.claude/agents/* ~/.claude/agents/ && cp -r platform-agents/claude_code/.claude/skills/* ~/.claude/skills/` |
| **Cursor** | `cp -r platform-agents/cursor/* .cursor/rules/` |
| **GitHub Copilot** | `cp -r platform-agents/github_copilot/.github .github/` |
| **OpenCode** | `opencode plugin install ./platform-agents/opencode` |
| **Windsurf** | `cp -r platform-agents/windsurf/* .windsurf/agents/` |
| **Codex CLI** | `cp -r platform-agents/codex_cli/.agents .` |
| **Gemini CLI / Antigravity** | `cp -r platform-agents/gemini_cli/.gemini .` |
| **Devin** | `cp -r platform-agents/devin/.devin .` |
| **Zed** | `cp -r platform-agents/zed/.agents .` |
| **Cline** | `cp -r platform-agents/cline/.clinerules .` |
| **Roo Code** | `cp -r platform-agents/roo_code/.roo .` |
| **Kilo Code** | `cp -r platform-agents/kilo_code/.kilocode .` |
| **Trae** | `cp -r platform-agents/trae/.trae .` |
| **Qwen Code** | `cp -r platform-agents/qwen_code/.qwen .` |
| **Kiro** | `cp -r platform-agents/kiro/.kiro .` |
| **Grok Build** | `cp -r platform-agents/grok_build/.grok .` |
| **Amazon Q** | `cp -r platform-agents/amazon_q/.amazonq .` |
| **Continue** | `cp -r platform-agents/continue/.continue .` |
| **OpenHands** | `cp -r platform-agents/openhands/microagents .openhands/microagents/` |
| **Goose** | `cp -r platform-agents/goose/recipes/* ~/.config/goose/recipes/` |
| **Aider** | `aider --read platform-agents/aider/conventions/NAME.md` |
| **Generic/Other** | Use `generic/` JSON files with your custom loader |

Every platform directory also contains a `README.md` with the exact install instructions for that tool.

### 3. Generate for Specific Platform Only
```bash
# Only Claude Code
python scripts/universal-converter.py --platforms claude_code --output ./claude-agents --universal-dir universal-agents

# Multiple platforms (comma- or space-separated, or mixed; 'all' for every platform)
python scripts/universal-converter.py --platforms claude_code,cursor,opencode --output ./my-agents --universal-dir universal-agents
```

## 📂 Project Structure

```
Kdesk-Catalog/
├── README.md
├── UNIVERSAL-AGENT-FORMAT.md          # Format specification
├── universal-agents/                   # 2,909 YAML files (source of truth)
│   ├── ml/                            # 1,044
│   ├── api/                           # 508
│   ├── devops/                        # 180
│   ├── code-quality/                  # 119
│   ├── backend/                       # 118
│   ├── security/                      # 97
│   ├── testing/                       # 76
│   ├── database/                      # 72
│   ├── data/ · frontend/              # 58 each
│   ├── cloud/ · devtools/ · mobile/ · compliance/ · infrastructure/ · monitoring/
│   │   sre/ · patterns/ · finops/ · networking/ · messaging/ · infra/   # 9–49 each
│   └── <name>/agent|skill/<name>.yaml # 1,109 files in 300 legacy single-name dirs
│                                       (both layouts coexisting; skills also as
│                                       `*-skill.yaml` next to agents in categories)
├── agents/                             # Native agent definitions (2026 layout)
│   ├── yaml/<category>/                # 1,766 byte-identical YAML copies
│   └── json/<category>/                # 1,766 lossless JSON definitions (definition-v1)
├── skills/                             # Native skill definitions (2026 layout)
│   ├── yaml/<category>/                # 1,143 byte-identical YAML copies
│   └── json/<category>/                # 1,143 lossless JSON definitions (definition-v1)
├── workflows/<category>/               # 1,766 *.workflow.json (workflow-v1, one per agent)
├── skills/wiring.json                  # Evidence-backed agent→skill links (tool evidence; 611 agents, 4,242 links; 1,090 skills with evidence, 53 conceptual without)
├── skills/wiring-overrides.yaml        # Committed hand-verified links (manual: true)
├── schemas/universal-agent.schema.json # Machine-checkable format spec (Draft 2020-12)
├── tests/                              # unittest suite for the pipeline scripts
├── archive/                            # Mirrored shells archived by `catalog-collapse.py` + curation (38, git-tracked)
├── reports/                            # Curated analysis output (renames, merge candidates)
├── CONVERSION-REPORT.md                # YAML→JSON conversion + validation report
├── platform-agents/                    # 130,954 regenerated platform files (gitignored; see below)
│   │                                   # 45 platform dirs × ~3,518 files each (2,909 items +
│   │                                   # manifests/READMEs/registry per platform), fully
│   │                                   # regenerable via universal-converter.py --platforms all
│   ├── claude_code/ · generic/ · opencode/ · windsurf/   # flat agent files (e.g. `1password.json`)
│   ├── cursor/ · firebase_studio/                       # flat `.mdc` rules
│   ├── github_copilot/                                  # flat `.md` (prompt_file per agent)
│   ├── codex_cli/                                       # `.agents/` Agent Skills
│   ├── gemini_cli/ · antigravity/ · devin/ · zed/ · cline/ · roo_code/ · kilo_code/ ·
│   │   trae/ · qwen_code/ · kiro/ · junie/ · zencoder/ · amp/ · factory_droid/ · crush/ ·
│   │   mcpjam/ · mux/ · pi/ · qoder/ · codebuddy/ · commandcode/ · neovate/  # `.agents`-style skills
│   ├── grok_build/ · amazon_q/ · augment/ · continue/  # `.md` rules
│   ├── goose/                                           # `recipes/`
│   ├── aider/                                           # `conventions/`
│   ├── openhands/                                       # `microagents/`
│   ├── google_jules/ · warp/ · void/ · cody/ · supermaven/ · codegpt/ · tabnine/ · firebender/
│   │                                                   # instruction `.md`
│   └── registry.yaml                                    # Master index
└── scripts/                            # Automation scripts
    ├── universal-converter.py         # Main converter (45 platforms)
    ├── migrate-to-universal.py        # Migrate old format
    ├── verify-all.py                  # Full validation
    ├── deep-audit.py                  # 10+ deep checks (incl. all platform outputs)
    ├── instructions-assembler.py      # Merge instruction content
    ├── handcraft-assembler.py         # Merge hand-crafted content
    ├── yaml-to-json.py                # YAML → JSON definitions + workflows
    ├── validate-conversion.py         # 12-check conversion validation
    ├── wire-skills.py / extract-skill-tools.py / extract-parameters.py   # Evidence pipeline
    ├── catalog-rename.py / catalog-collapse.py / catalog-hygiene.py      # Curation (L1/L3)
    ├── de-fingerprint.py              # Content-vs-name consistency pass
    ├── merge-candidates-v2.py         # Family-level merge ranking report
    ├── schema-check.py                # Schema validation of all YAMLs
    └── fix-*.py                       # Data quality fixes
```

## 🔧 Universal Agent Format

Each agent/skill in `universal-agents/` follows this schema:

```yaml
name: unique-name
display_name: Human Readable Name
category: ml|devops|api|backend|...
subcategory: training|deployment|inference|...
description: Brief description
version: 1.0.0
tags: [tag1, tag2]
capabilities:
  - name: Capability Name
    description: What it does
    commands:
      - real cli command 1
      - real cli command 2
    examples:
      - usage example 1
    parameters: []
knowledge:
  - title: Doc Title
    type: documentation|reference|tutorial
    source: url-or-path
    description: What it covers
instructions: |
  Detailed system prompt for the agent
examples:
  - usage example
platforms:
  claude_code:
    tools: [Bash, Read, Write, Edit, Glob, Grep]
    model: claude-3-5-sonnet-20241022
  cursor:
    rule_type: auto
    model: gpt-4
  github_copilot:
    prompt_file: name.md
    extension: github.copilot
  windsurf:
    model: claude-3.5-sonnet
    tools: [bash, read, write, edit]
  opencode:
    plugin: opencode-name
  generic:
    system_prompt: "You are X. Description..."
    available_tools: [bash, read, write, edit]
```

## ⚙️ Scripts

| Script | Purpose |
|--------|---------|
| `universal-converter.py` | Convert universal YAML → 45 platform formats |
| `migrate-to-universal.py` | Migrate old format → universal YAML |
| `verify-all.py` | Validate all universal agents against schema |
| `deep-audit.py` | 10+ deep checks (universal + all platform outputs) |
| `instructions-assembler.py` | Merge instruction content into YAML |
| `handcraft-assembler.py` | Merge hand-crafted fields into YAML |
| `yaml-to-json.py` | YAML → JSON definitions (agents/, skills/) + workflows/ (`--wiring` merges skill links) |
| `validate-conversion.py` | 12 checks: counts, refs, wiring manifest, key/value preservation, integrity |
| `wire-skills.py` | Generate `skills/wiring.json` — evidence-backed agent↔skill links (+`--overrides` manual links) |
| `extract-skill-tools.py` | Derive `prerequisites` for tool-less skills from their own commands (content-derived, idempotent) |
| `extract-parameters.py` | Promote real CLI flags from capability commands into `parameters` (evidence-gated, idempotent) |
| `schema-check.py` | Validate all 2,909 YAMLs against `schemas/universal-agent.schema.json` |
| `catalog-hygiene.py` | `dedup` near-duplicate skill families; `gaps` per-category quality report |
| `catalog-rename.py` | Content-derived renames for combinatorial names (vN/-deploy/-sdk/-server; preview + `--apply`) |
| `catalog-collapse.py` | Evidence-gated collapse of mirrored shells → `archive/` (identical commands + near-duplicate text); writes `reports/merge-candidates.md` |
| `de-fingerprint.py` | Content-vs-name consistency: strips desc serials, quarantines copy-paste keywords, syncs `expert-in` prompts, prunes empty dirs |
| `merge-candidates-v2.py` | Family-level merge ranking (command overlap + instruction Jaccard) → `reports/merge-candidates-v2.md` |
| `fix-*.py` | Fix various data quality issues |

**Usage:**
```bash
# Convert to specific platforms
python scripts/universal-converter.py --platforms claude_code,cursor --output ./out --universal-dir universal-agents

# Validate all agents
python scripts/verify-all.py

# Generate registry
python scripts/universal-converter.py --registry

# (Re)generate JSON definitions + workflows from YAML source
python scripts/extract-skill-tools.py --apply   # optional: prerequisites for tool-less skills
python scripts/extract-parameters.py --apply   # optional: parameters from real CLI flags
python scripts/wire-skills.py --agents universal-agents --out skills/wiring.json
python scripts/yaml-to-json.py --agents universal-agents --out . --wiring skills/wiring.json
python scripts/validate-conversion.py

# Validate source YAMLs against the format schema
python scripts/schema-check.py

# Unit tests for the pipeline
python -m unittest discover -s tests

# Anti-fingerprint curation: content-derived renames (preview first)
python scripts/catalog-rename.py            # preview mapping
python scripts/catalog-rename.py --apply    # apply renames

# Evidence-gated collapse of mirrored shells into archive/
python scripts/catalog-collapse.py --apply

# Content-vs-name consistency pass (descriptions/keywords/prompts, preview first)
python scripts/de-fingerprint.py            # preview
python scripts/de-fingerprint.py --apply    # apply

# Family-level merge ranking (evidence-gated; decide per line, then archive losers)
python scripts/merge-candidates-v2.py
```

## ⚠️ Known Limits (honest status)

The pipeline is production-ready and verified end-to-end (schema → conversion → 130,954
platform files). Content quality is curated but not perfect — here is the measured state:

- **Content is ~95% template-generated.** Curation (L1 renames → L2/L3 collapse → L4
  merge-candidates) has run and is evidence-gated, but each new batch still needs review.
- **53 of 1,143 skills are conceptual** (e.g. `rest`, `pagination`, `oauth2-introspection`,
  `azure-api-management`): they teach HTTP/API conventions via universal primitives
  (`curl`, `go`, `az`) and carry **no distinct CLI binary**, so the tool-evidence wiring
  intentionally does not link them (reported as `skills_without_evidence` in
  `skills/wiring.json`). 9 more were given declared CLI evidence (`op`, `bw`, `k6`, `ng`,
  `yq`, `mb`, `jq`) — wireable where a matching agent exists.
- **1,090/1,143 skills carry tool evidence; 611 agents are wired (4,242 links).**
  Remaining unwired agents are those whose commands use only generic CLIs.
- **144 name-families have >1 member.** These are role/persona suffix groups
  (architect/engineer/specialist/v2). Measured on command overlap + instruction Jaccard:
  **0 pairs meet the evidence-strong duplicate bar** (ovl ≥ 0.7 and sim ≥ 0.4); the
  15 near pairs were human-reviewed and kept as real variants (per-cloud/per-tool/persona);
  295 pairs are clearly distinct. See `reports/merge-candidates-v2.md` (REVIEWED section).
- **Archived duplicates stay queryable** in `archive/` (moved, not deleted) with the
  evidence that triggered the move in the commit history.

## ✅ Quality Assurance

All items pass:
- ✅ Schema validation (required fields, types) — 0 violations on 2,909 files
- ✅ YAML/JSON syntax validity
- ✅ No JSON strings in instructions
- ✅ Real CLI commands (not templates)
- ✅ Unique agent names and command sets
- ✅ Platform-specific format correctness (all 45 platforms, 130,954 files)
- ✅ Registry completeness
- ✅ Unit tests (36 passing: wiring rules, YAML→JSON fidelity, CLI parsing)

## 📄 License

MIT © Mehul Wagde
