# Kdesk Platform Matrix

**Generated:** 2026-08-13 · **Data:** `scripts/universal-converter.py` `PLATFORM_INFO` + `tests/test_platform_spec.py` + live `platform-agents/` inventory

## Summary

| Metric | Value |
|--------|-------|
| Platforms | **45** |
| Formats | 5 families (legacy 6, Agent Skills SKILL.md 23, rules .md/.mdc 7, special 3, single-file 5, deprecated 1) |
| Platform files | 130,955 (measured) · ~2,909–2,911 per platform |
| Source items | 2,909 (1,766 agents + 1,143 skills) |

## Legacy Core (6)

| Platform | Format | Install target | Support |
|----------|--------|----------------|---------|
| `claude_code` | `.md` YAML frontmatter (`model: inherit`) | `~/.claude/agents/` + `~/.claude/skills/` | SUPPORTED |
| `cursor` | `.mdc` rules (description/globs/alwaysApply only) | `.cursor/rules/` | SUPPORTED |
| `github_copilot` | `.instructions.md` frontmatter + `applyTo` | `.github/instructions/` | SUPPORTED |
| `windsurf` | rules `.md` (trigger frontmatter) | `.windsurf/rules/` | SUPPORTED |
| `opencode` | agents `.md` + `SKILL.md` | `.opencode/agents/` + `.opencode/skills/` | SUPPORTED |
| `generic` | `.json` (system prompt + tool list) | any LLM agent | SUPPORTED |

## Agent Skills — SKILL.md open standard (23)

`codex_cli` (.agents/skills), `gemini_cli` (.gemini/skills), `antigravity` (.agent/skills), `devin` (.devin/skills), `zed` (.agents/skills), `cline` (.clinerules/skills), `roo_code` (.roo/skills), `kilo_code` (.kilocode/skills), `trae` (.trae/skills), `qwen_code` (.qwen/skills), `kiro` (.kiro/skills), `junie` (.junie/skills), `zencoder` (.agents/skills), `amp` (.agents/skills), `factory_droid` (.factory/skills), `crush` (.crush/skills), `mcpjam` (.mcpjam/skills), `mux` (.mux/skills), `pi` (.pi/skills), `qoder` (.qoder/skills), `codebuddy` (.codebuddy/skills), `commandcode` (.commandcode/skills), `neovate` (.neovate/skills)

All SUPPORTED (SKILL.md per agentskills.io; also readable by 40+ skills-compatible tools).

## Rules — .md / .mdc (7)

| Platform | Format | Install target | Support |
|----------|--------|----------------|---------|
| `grok_build` | plain `.md` | `.grok/rules/` | SUPPORTED |
| `amazon_q` | plain `.md` | `.amazonq/rules/` | SUPPORTED |
| `augment` | `.md` (type: Always) | `.augment/rules/` | SUPPORTED |
| `firebase_studio` | `.mdc` | `.idx/rules/` | SUPPORTED |
| `continue` | `.md` frontmatter | `.continue/rules/` | SUPPORTED |
| `tabnine` | plain `.md` guidelines | `.tabnine/guidelines/` | SUPPORTED |
| `supermaven` | plain `.md` | `.supermaven/rules/` | SUPPORTED |

## Special native formats (3)

| Platform | Format | Install target | Support |
|----------|--------|----------------|---------|
| `goose` | recipes YAML (title/description/instructions) | `~/.config/goose/recipes/` | SUPPORTED |
| `aider` | conventions `.md` | `aider --read` / `.aider.conf.yml` | SUPPORTED |
| `openhands` | microagents `.md` (type repo/knowledge + triggers) | `.openhands/microagents/` | SUPPORTED |

## Single-file instruction platforms (5)

| Platform | Format | Install target | Support |
|----------|--------|----------------|---------|
| `google_jules` | `AGENTS.md` | repo root | SUPPORTED |
| `warp` | `WARP.md` | repo root | SUPPORTED |
| `codegpt` | `AGENTS.md` | repo root | PARTIALLY_SUPPORTED (native file not yet assembled; 1 test skipped) |
| `cody` | `.vscode/cody.json` commands | `.vscode/` | PARTIALLY_SUPPORTED (native file not yet assembled; 1 test skipped) |
| `firebender` | `.firebender/agents/*.md` + `firebender.json` | `.firebender/` | PARTIALLY_SUPPORTED (native file not yet assembled; 1 test skipped) |

## Deprecated (1)

| Platform | Format | Install target | Support |
|----------|--------|----------------|---------|
| `void` | fragments only, no native file | — | PARTIALLY_SUPPORTED (⚠ unverified; `.void/config.json` is an OAuth token cache, not a rules file) |

## Frontmatter contracts (enforced by tests/test_platform_spec.py)

- **Claude Code:** `.md` with `name`, `description`, `tools`, `model: inherit`.
- **Cursor / Firebase Studio:** `.mdc` with `description`, `globs`, `alwaysApply` — no `model`, no `rule_type`.
- **GitHub Copilot:** `.instructions.md` with `applyTo`.
- **Goose:** `recipes/*.yaml` (title/description/instructions).
- **OpenHands:** `microagents/*.md` with `type: repo` or `type: knowledge` (knowledge must carry non-empty `triggers`).

## Health

- 45/45 platform dirs present in `platform-agents/`; ~2,909–2,911 files each (2,909 items + README/manifest/registry).
- 3 native-file assembly gaps (codegpt, cody, firebender) — tracked by skipped tests; all other contracts green.
- `void` emits fragments only by design (deprecated tool).