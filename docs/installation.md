# Kdesk Installation

How to install, use, and uninstall the Kdesk-Catalog platform content.

## 1. Prerequisites

- Python ≥ 3.9 (`PyYAML` for the converter; `kdesk` package itself is stdlib-only except `PyYAML` and optional `platformdirs`)
- The Kdesk-Catalog repository (content source)

## 2. Generate platform files

```bash
# All 45 platforms (~15 min, 130,955 files)
python scripts/universal-converter.py --platforms all --quiet

# Single platform (fast)
python scripts/universal-converter.py --platforms claude_code --quiet
```

## 3. Install per platform

| Platform | Command |
|----------|---------|
| Claude Code | `cp -r platform-agents/claude_code/.claude/agents/* ~/.claude/agents/ && cp -r platform-agents/claude_code/.claude/skills/* ~/.claude/skills/` |
| Cursor | `cp -r platform-agents/cursor/* .cursor/rules/` |
| GitHub Copilot | `cp -r platform-agents/github_copilot/.github .github/` |
| OpenCode | `opencode plugin install ./platform-agents/opencode` |
| Windsurf | `cp -r platform-agents/windsurf/* .windsurf/agents/` |
| Codex CLI | `cp -r platform-agents/codex_cli/.agents .` |
| Gemini CLI / Antigravity | `cp -r platform-agents/gemini_cli/.gemini .` |
| Devin | `cp -r platform-agents/devin/.devin .` |
| Zed | `cp -r platform-agents/zed/.agents .` |
| Cline | `cp -r platform-agents/cline/.clinerules .` |
| Roo Code | `cp -r platform-agents/roo_code/.roo .` |
| Kilo Code | `cp -r platform-agents/kilo_code/.kilocode .` |
| Trae | `cp -r platform-agents/trae/.trae .` |
| Qwen Code | `cp -r platform-agents/qwen_code/.qwen .` |
| Kiro | `cp -r platform-agents/kiro/.kiro .` |
| Grok Build | `cp -r platform-agents/grok_build/.grok .` |
| Amazon Q | `cp -r platform-agents/amazon_q/.amazonq .` |
| Continue | `cp -r platform-agents/continue/.continue .` |
| OpenHands | `cp -r platform-agents/openhands/microagents .openhands/microagents/` |
| Goose | `cp -r platform-agents/goose/recipes/* ~/.config/goose/recipes/` |
| Aider | `aider --read platform-agents/aider/conventions/NAME.md` |
| Generic/Other | Use `generic/` JSON files with your custom loader |

Every platform directory contains a `README.md` with exact install instructions.

**Recommended:** use `kdesk install <platform> [--project|--home]` to install and `kdesk doctor` to verify.

## 4. kdesk CLI

```bash
kdesk registry search "helm"          # query the catalog
kdesk graph --agent my-agent          # agent -> skills graph
kdesk workflow validate wf-my-agent   # validate a workflow
kdesk workflow run wf-my-agent --dry-run
kdesk install claude_code --home      # install to ~/.claude
kdesk doctor                          # verify all installed platforms
kdesk adapters                        # support-level matrix
kdesk security scan                   # secret scan of definitions
kdesk provenance verify               # JSON -> YAML traceability
kdesk quality report                  # content quality scoring
kdesk duplicates                      # duplicate-family report
```

## 5. Verify installation

```bash
kdesk doctor                          # per-platform OK/MISSING/EXTRA/MALFORMED
pytest tests/test_platform_spec.py -v   # platform contract tests
python scripts/verify-all.py          # legacy full verification
```

Expected: 1,766 agents + 1,143 skills per platform (~2,909 items), all frontmatter contracts met.

## 6. Uninstall

Remove the copied directories per platform (e.g. `rm -rf ~/.claude/agents ~/.claude/skills`, `rm -rf .cursor/rules`, `rm -rf .github/instructions`). Platform files are regenerable — the catalog is never modified by installation.

## 7. Versioning

- **Content version = git revision.** The catalog has no independent semantic
  version: `universal-agents/` is the source of truth and every generated
  artifact (platform files, JSON definitions, marketplaces) is regenerable from
  it. Pin your installs to a git tag or commit SHA when you need reproducibility.
- **Tool version.** `kdesk` reports its own version via
  `kdesk --version` (`kdesk.__version__`, e.g. `1.1.0`) and includes it in
  `kdesk verify` output.
- **Install manifest.** `kdesk install` records every installed file (relative
  target + SHA-256) in `<base>/.kdesk/manifest.json` (manifest format v1).
  `kdesk verify` compares installed files against the manifest, and
  `kdesk uninstall`/rollback uses it to remove only what kdesk installed.
- **Keeping installs current.** After pulling new catalog revisions, re-run the
  converter (`python scripts/universal-converter.py --platforms <name>`) and
  re-install (`kdesk install <platform>`); files whose SHA-256 changed are
  re-copied, identical files are skipped. Platform artifacts are never
  hand-edited, so drift is limited to locally modified copies, which
  `kdesk verify` reports as `MALFORMED`/`EXTRA`.

## 8. Notes

- `platform-agents/` is gitignored: always regenerate from `universal-agents/` after pulling updates.
- Model pins: keep `inherit` (portable default) — do not hand-edit installed files.
- If a platform is deprecated (`void`), fragments are emitted for reference only; no native file is installed.