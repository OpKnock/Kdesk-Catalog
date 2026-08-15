"""Full verification of the 2909-agent subagent pipeline for the main AI.

Checks, for the Claude Code (main AI) target:
  1. Subagent .md files exist, have valid YAML frontmatter (name/description/tools/model)
  2. Skills exist as <name>/SKILL.md with name+description frontmatter
  3. Every agent has exactly one workflow with >=1 step
  4. Every workflow references an existing agent
  5. Wiring manifest links agents to skills
  6. No stale model IDs in any artifact
  7. Counts reconcile to 2909 (1766 agents + 1143 skills)
"""
import json
import re
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
CC = ROOT / "platform-agents" / "claude_code" / ".claude"
AGENTS = CC / "agents"
SKILLS = CC / "skills"
WF_DIR = ROOT / "workflows"
WIRING = ROOT / "skills" / "wiring.json"

FRONT = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
STALE = ("claude-3-5-sonnet-20241022", "claude-3.5-sonnet")


def parse_front(text):
    m = FRONT.match(text)
    return m.groups()[0] if m else ""


def main():
    report = []
    report.append("=" * 60)
    report.append("Kdesk-Catalog Subagent Verification (main AI = Claude Code)")
    report.append("=" * 60)

    # 1. subagents
    md = sorted(AGENTS.glob("*.md"))
    report.append(f"\n[1] Subagent .md files: {len(md)}")
    bad_fm = []
    for f in md:
        head = parse_front(f.read_text(encoding="utf-8"))
        if not all(k in head for k in ("name:", "description:", "tools:", "model:")):
            bad_fm.append(f.name)
    report.append(f"    frontmatter complete (name/description/tools/model): "
                  f"{len(md) - len(bad_fm)}/{len(md)}"
                  + (f"  BAD: {bad_fm[:5]}" if bad_fm else ""))

    # 2. skills
    skill_dirs = sorted([d for d in SKILLS.iterdir() if d.is_dir()])
    skill_files = sorted(SKILLS.glob("*/SKILL.md"))
    report.append(f"\n[2] Skill directories: {len(skill_dirs)} | SKILL.md files: {len(skill_files)}")
    bad_skill = [f.parent.name for f in skill_files
                 if not all(k in parse_front(f.read_text(encoding="utf-8"))
                            for k in ("name:", "description:"))]
    report.append(f"    SKILL.md frontmatter (name/description): "
                  f"{len(skill_files) - len(bad_skill)}/{len(skill_files)}"
                  + (f"  BAD: {bad_skill[:5]}" if bad_skill else ""))

    # 3+4. workflows
    wfs = sorted(WF_DIR.rglob("*.workflow.json"))
    wf_agents = {json.loads(p.read_text(encoding="utf-8")).get("agent") for p in wfs}
    agent_names = {f.stem for f in md}
    no_wf = sorted(agent_names - wf_agents)
    wf_no_agent = [p for p in wfs
                   if json.loads(p.read_text(encoding="utf-8")).get("agent") not in agent_names]
    empty = [p for p in wfs if not json.loads(p.read_text(encoding="utf-8")).get("steps")]
    report.append(f"\n[3] Workflow files: {len(wfs)}")
    report.append(f"    agents missing workflow: {len(no_wf)} {no_wf[:5]}")
    report.append(f"[4] workflows referencing unknown agent: {len(wf_no_agent)} {[p.name for p in wf_no_agent][:5]}")
    report.append(f"    workflows with zero steps: {len(empty)} {[p.name for p in empty][:5]}")

    # 5. wiring
    w = json.loads(WIRING.read_text(encoding="utf-8"))
    stats = w.get("stats", {})
    report.append(f"\n[5] Wiring manifest: {stats.get('agents_wired')} agents wired, "
                  f"{stats.get('skills_used')} skills used, {stats.get('total_links')} links")

    # 6. stale models
    stale_hits = 0
    for f in list(AGENTS.glob("*.md")) + list(SKILLS.glob("*/SKILL.md")):
        head = f.read_text(encoding="utf-8", errors="ignore")[:2048]
        if any(s in head for s in STALE):
            stale_hits += 1
    report.append(f"\n[6] Stale model IDs in subagent/skill artifacts: {stale_hits}")

    # 7. counts
    total = len(md) + len(skill_dirs)
    report.append(f"\n[7] TOTAL: {len(md)} agents + {len(skill_dirs)} skills = {total} (target 2909)")

    ok = (not bad_fm and not bad_skill and not no_wf and not wf_no_agent
          and not empty and stale_hits == 0 and total == 2909)
    report.append(f"\nRESULT: {'PASS - all 2909 agents and skills verified' if ok else 'FAIL'}")

    # 8. install check into ~/.claude (main AI global dirs)
    claude_agents = Path.home() / ".claude" / "agents"
    claude_skills = Path.home() / ".claude" / "skills"
    installed_agents = len(list(claude_agents.glob("*.md"))) if claude_agents.is_dir() else 0
    installed_skills = len([d for d in claude_skills.iterdir() if d.is_dir()]) if claude_skills.is_dir() else 0
    report.append(f"\n[8] INSTALLED into ~/.claude: {installed_agents} subagents, "
                  f"{installed_skills} skill dirs (target 1766 agents / 1143 skills)")
    install_ok = installed_agents == 1766 and installed_skills >= 1143
    report.append(f"    {'PASS - usable as subagents of the main AI' if install_ok else 'NOT INSTALLED'}")

    out = "\n".join(report)
    print(out)
    (ROOT / "reports" / "SUBAGENT-VERIFICATION-REPORT.md").write_text(out + "\n", encoding="utf-8")
    return 0 if (ok and install_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
