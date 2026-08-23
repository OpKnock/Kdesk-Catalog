import yaml
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "universal-agents"

fixed = 0
for p in SRC.rglob("*.yaml"):
    if p.name == "registry.yaml":
        continue
    doc = yaml.safe_load(p.read_text(encoding="utf-8"))
    if not isinstance(doc, dict):
        continue
    platforms = doc.get("platforms")
    if not isinstance(platforms, dict):
        continue
    cp = platforms.get("github_copilot")
    if not isinstance(cp, dict):
        continue
    name = doc.get("name")
    if not name:
        continue
    expected = f"{name}.md"
    if cp.get("prompt_file") != expected:
        cp["prompt_file"] = expected
        with open(p, "w", encoding="utf-8") as f:
            yaml.dump(doc, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        print(f"fixed {p.relative_to(SRC)}: prompt_file -> {expected}")
        fixed += 1
print(f"total fixed: {fixed}")
