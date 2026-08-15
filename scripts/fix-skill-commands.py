#!/usr/bin/env python3
"""
Fix 9 skill files that have real commands embedded in instructions
but empty capabilities[].commands. Extracts bash commands and a few
examples from the instructions into the capabilities block.
"""
import re
import yaml
from pathlib import Path

FILES = [
    "backend/spring-skill.yaml",
    "database/kafka-cli-skill.yaml",
    "database/redis-cli-skill.yaml",
    "devops/envoy-skill.yaml",
    "mobile/flutter-skill.yaml",
    "mobile/react-native-skill.yaml",
    "security/kyverno-skill.yaml",
    "testing/pact-skill.yaml",
    "testing/rest-assured-skill.yaml",
]

AGENTS_DIR = Path(__file__).resolve().parents[1] / "universal-agents"

def extract_bash_commands(text):
    cmds = []
    for m in re.finditer(r"```bash\s*\n(.*?)```", text, re.S):
        for line in m.group(1).splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            line = re.sub(r"\s*#.*$", "", line).strip()
            if line and not line.startswith(("$", ">", "sudo ")):
                cmds.append(line)
    return cmds

def main():
    for rel in FILES:
        path = AGENTS_DIR / rel
        with open(path, "r", encoding="utf-8") as f:
            doc = yaml.safe_load(f)

        cmds = extract_bash_commands(doc.get("instructions", ""))
        if not cmds:
            print(f"[SKIP] no bash commands found: {rel}")
            continue

        for cap in doc.get("capabilities", []):
            if isinstance(cap, dict):
                cap["commands"] = cmds
                cap["examples"] = cmds[:3]
                if not cap.get("description"):
                    cap["description"] = doc.get("description", "")

        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(doc, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        print(f"[OK] {rel}: {len(cmds)} commands extracted")

if __name__ == "__main__":
    main()
