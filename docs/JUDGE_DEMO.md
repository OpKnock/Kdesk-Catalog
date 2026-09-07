# KDesk Beyond Chatbot — Agentic Demo for Judges

> **Beyond a chatbot that can read, reason, compare, and take actions**
> n8n-style: Skills = nodes, Agents = orchestrators, Workflows = pipelines.

---

## 1. What We Built: Specific-Purpose Agent (Not General Assistant)

**Question:** General AI assistant with tool access vs. specific-purpose agent?

**Answer:** Specific-purpose. This repo is a catalog of 3,093 agents/skills — a general assistant would be unbounded and untestable. We built a **Catalog Governance Agent** that demonstrates all four agentic capabilities in one verifiable workflow.

| Capability | Chatbot | Our Agent |
|---|---|---|
| **Read** | Reads chat history | Reads 3,093 YAML source files + 45 platform outputs + provenance JSON + trust scores |
| **Reason** | Next-token prediction | Reasons about drift (YAML 3093 vs JSON 2909), stale provenance paths, trust deltas |
| **Compare** | Compares text | Compares artifact generations, schema versions, platform capability versions |
| **Take Action** | Sends text | Runs `kdesk verify --fast`, `kdesk trust`, `kdesk doctor --fix`, regenerates artifacts, emits n8n-like workflow runs |

General assistant = scope creep. Specific agent = demoable, measurable, judgeable.

---

## 2. Architecture: n8n for Agents/Skills

```
Trigger:  catalog change (new YAML) or schedule or `kdesk verify --fast`
   │
   ▼
┌─────────────────────────────────────────────────────────┐
│  Catalog Auditor Agent (specific-purpose)               │
│  Type: agent | Delegation: parallel + conditional       │
│  Model: inherit (portable, no claude-4 hardcode)       │
└─────────────────────────────────────────────────────────┘
   │
   ├─── Skill Node: read-catalog          ───┐
   │     reads universal-agents/*.yaml        │ parallel
   │     reads agents/*.json + provenance     │
   ├─── Skill Node: read-platforms        ───┘
   │     counts platform-agents/* (136k files)
   │
   ├─── Skill Node: compare-artifacts        ─── conditional
   │     if yaml_count != json_count → drift
   │     if provenance path == "universal-agents/..." → bug (now fixed to normalize)
   │
   ├─── Skill Node: evaluate-trust           ─── sequential
   │     TrustScorer.breakdown() → compatibility / security / policy / provenance
   │     flags: trust < 60, blocked secrets, version mismatch
   │
   └─── Skill Node: take-action              ─── tool nodes
         kdesk verify --fast  → gate
         kdesk doctor --fix   → auto-fix
         safe_path()          → guard writes inside allowed_root
         yaml-to-json         → regenerate 184 missing JSON
```

**Skills = reusable nodes** (read, compare, evaluate). **Agent = orchestrates nodes**. **Workflow = declarative pipeline** (`workflows/catalog-audit.workflow.json`) with `parallel`, `conditional`, `sequential` step types — now validated and executed by `kdesk/workflow.py`.

---

## 3. How to Run (2 minutes)

```bash
# 1. Install
pip install -e "."

# 2. One-liner agentic demo: read → reason → compare → act
python scripts/demo_beyond_chatbot.py

# 3. Or run the workflow engine directly (dry-run)
python -m kdesk.cli workflow --validate catalog-audit
python -m kdesk.cli workflow --run catalog-audit

# 4. Verify the fixes that unblock agentic actions
python -m pytest tests/test_cli_contract.py::TestRuntimeAdapterContract -v
python -m pytest tests/test_cli_contract.py::TestCliWorkflowDelegationContract -v
python -m kdesk.cli adapters --format json | jq '.rows[0] | {platform, version, capabilities_version}'
python -m kdesk.cli stats --format json --fast | jq '{agents, skills, total}'

# 5. Safe path guard demo (prevents traversal / symlink escape)
python -c "from kdesk.security import safe_path; from pathlib import Path; print(safe_path('universal-agents/backend/auth.yaml', Path.cwd()))"
python -c "from kdesk.security import safe_path; safe_path('../../etc/passwd', '.')"  # raises PathSecurityError
```

**Expected output of `demo_beyond_chatbot.py`:**
```
[READ]  3093 YAML definitions, 45 platforms, trust cache warm
[REASON] drift: 184 YAML without JSON, provenance path bug: fixed (normalized), trust median: 78
[COMPARE] YAML generation 3093 vs JSON 2909 vs workflows 1858 vs platform outputs 136k — inconsistent generations
[ACT] kdesk verify --fast → 3 problems (now with generation_id)
[ACT] safe_path guard → blocked traversal attempt (PathSecurityError)
[ACT] WorkflowEngine parallel+conditional validated, dry-run: parallel-invoke, evaluate, sequential-invoke
[ACT] adapters capability versioning: claude_code@1.0.0 supports parallel@1.0
```

---

## 4. What Was Fixed to Make This Possible (Audit → Fix)

| Audit Finding | Fix | File |
|---|---|---|
| YAML→JSON 184 missing, stale provenance | Normalize provenance: `Path(source).parts[0]=="universal-agents"` handling; add `generation_id`/`source_checksum` to reports | `kdesk/provenance.py`, `scripts/yaml-to-json.py` |
| Provenance checker path bug | Normalize before `root / source` | `kdesk/provenance.py:42` |
| Huge line-ending churn (3,078 files, 494k diff) | Add `.gitattributes` `*.yaml text eol=lf` + `git add --renormalize` | `.gitattributes` |
| RuntimeAdapter type bug (`"name" in definition`) | Strict explicit type `if type=="skill" elif type=="agent" else raise ValueError` | `kdesk/adapters/contract.py:232` |
| Claude adapter `model: claude-4` violates inherit | `definition.get("model") or "inherit"` | `kdesk/adapters/contract.py` `render_agent` |
| Workflow parallel/conditional dead code | Add `parallel`, `conditional`, `sequential`, `loop` to `validate` + `execute` + cycle detection | `kdesk/workflow.py:58-170` |
| Stats cache stale on nested file changes | Tree key now covers sorted YAML list + mtime_ns + size (full cache) | `kdesk/registry.py:66` |
| Heavy 407-test suite (>130k file scan) | Split unit vs integration, fixtures, `KDESK_FULL=1` guard, CLI contract tests pinned | `tests/test_cli_contract.py`, `tests/test_platform_spec.py` |
| Platform capability versioning missing | Add `version`, `capabilities_version`, `supports_capability()` to registry | `kdesk/adapters/__init__.py:50-110` |
| Path traversal / symlink escape | Add `kdesk/security.py:safe_path`, `safe_join` with traversal + symlink checks | `kdesk/security.py:21-130` |
| CLI surface untested | Add `tests/test_cli_contract.py` (20 tests, <7s) | `tests/test_cli_contract.py` |

---

## 5. Why This Is Beyond a Chatbot

A chatbot answers: *"How many agents?"* → `"3093"`.

Our agent does:
1. **Reads** 3,093 YAML and 136k platform files via `Catalog.from_repo()` + parse cache.
2. **Reasons** that 3,093 ≠ 2,909 means pipeline is broken, that `_provenance.source` double-joins `universal-agents/`, that `PlatformCapability` version mismatches cause silent drift.
3. **Compares** generations by checksum (`source_checksum == provenance.checksum`) and by `version`/`capabilities_version` per platform (A/B/C tiers).
4. **Acts** via tools with guards: `safe_path` blocks `../../etc/passwd`, `WorkflowEngine` dry-runs parallel branches then delegates via `kdesk run --auto-approve`, `TrustScorer` blocks low-trust installs, `kdesk doctor --fix` renorms line endings.

All actions are validated, versioned, and auditable — not free-text.

---

## 6. n8n Mapping Cheat-Sheet for Judges

| n8n Concept | KDesk Equivalent | Example |
|---|---|---|
| Trigger | `kdesk verify --fast` + file watcher / cron | `scripts/demo_beyond_chatbot.py: trigger()` |
| Node | Skill (`SKILL.md`) | `read-catalog`, `compare-artifacts`, `evaluate-trust`, `take-action` |
| Flow | Agent (`universal-agents/<family>/<name>.yaml` with `skills: [...]`, `sub_agents`, `delegation_pattern`) | `catalog-auditor.yaml` |
| Branch | `parallel` workflow step | `branches: [["read-catalog","read-platforms"]]` |
| If | `conditional` workflow step | `condition: "drift > 0"` |
| Loop | `sequential` / `loop` step | `sequence: ["s1","s2","s3"]` with cycle detection |
| Credentials | `safe_path` + `TrustScore` + `PolicyEngine` | Blocks traversal, low trust, policy violation |
| Execution | `WorkflowEngine.run(dry_run=False)` | `kdesk workflow --run catalog-audit --execute` |

Run `cat workflows/catalog-audit.workflow.json | jq .steps` to see the n8n-like JSON.

---

## 7. Artifacts to Inspect

- `scripts/demo_beyond_chatbot.py` — runnable agentic loop (read/reason/compare/act)
- `workflows/catalog-audit.workflow.json` — declarative n8n-style workflow (parallel/conditional/sequential)
- `universal-agents/governance/catalog-auditor.yaml` — the specific-purpose agent definition
- `universal-agents/governance/*.yaml` — the 4 skills used as nodes
- `tests/test_cli_contract.py` — CLI contract pinning the agent's tool surface
- `kdesk/security.py` — `safe_path` guard (try the traversal demo above)
- `kdesk/adapters/__init__.py` — platform capability versioning (`version`, `supports_capability`)

---

*Specific-purpose agent, n8n-style skills, verifiable actions — that's the beyond-chatbot bar. `python scripts/demo_beyond_chatbot.py` to see it.*
