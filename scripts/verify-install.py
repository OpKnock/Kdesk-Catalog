"""Verify the install into ~/.claude (main AI global dirs)."""
import io
import json
import os
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
with open(ROOT / "reports" / "catalog-stats.json", "r", encoding="utf-8") as f:
    STATS = json.load(f)
total_agents = STATS["agents"]
total_skills = STATS["skills"]

CLAUDE = Path(os.environ.get("KDESK_CLAUDE_DIR", Path.home() / ".claude"))
AGENTS = CLAUDE / "agents"
SKILLS = CLAUDE / "skills"
FRONT = re.compile(r"^---\n(.*?)\n---", re.DOTALL)

md = sorted(AGENTS.glob("*.md"))
skill_dirs = [d for d in SKILLS.iterdir() if d.is_dir()]
skill_files = sorted(SKILLS.glob("*/SKILL.md"))

bad_agent = []
for f in md:
    m = FRONT.search(f.read_text(encoding="utf-8"))
    head = m.group(1) if m else ""
    if not all(k in head for k in ("name:", "description:", "tools:", "model:")):
        bad_agent.append(f.name)

bad_skill = []
for f in skill_files:
    m = FRONT.search(f.read_text(encoding="utf-8"))
    head = m.group(1) if m else ""
    if not all(k in head for k in ("name:", "description:")):
        bad_skill.append(f.parent.name)

pre_existing = {"agent-reach", "learned", "openwork"}
new_skill_dirs = [d.name for d in skill_dirs if d.name not in pre_existing]

print("installed subagents :", len(md))
print("installed skills    :", len(new_skill_dirs), "(+3 pre-existing)")
print("subagent frontmatter OK:", len(md) - len(bad_agent), "/", len(md), bad_agent[:5])
print("skill frontmatter OK   :", len(skill_files) - len(bad_skill), "/", len(skill_files), bad_skill[:5])

sample = md[0]
print("\nsample installed subagent:", sample.name)
print(open(sample, encoding="utf-8").read()[:300])

missing = total_agents - len(md)
missing_skills = total_skills - len(new_skill_dirs)
print("\nmissing agents:", missing, "| missing skills:", missing_skills)
print("RESULT:", "INSTALL COMPLETE" if missing == 0 and missing_skills == 0 and not bad_agent and not bad_skill else "INCOMPLETE")
