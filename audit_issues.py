"""Audit: find duplicate dict keys, dead code, and security issues."""
import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
issues = []

# 1. Duplicate dictionary keys in platform metadata
for py_file in [ROOT / "kdesk" / "compatibility.py", ROOT / "kdesk" / "scanner.py"]:
    if not py_file.exists():
        continue
    tree = ast.parse(py_file.read_text(encoding="utf-8", errors="ignore"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            seen = set()
            for k in node.keys:
                if isinstance(k, ast.Constant) and isinstance(k.value, str):
                    if k.value in seen:
                        issues.append(f"DUP_KEY: {py_file.name}:{node.lineno} duplicate '{k.value}'")
                    seen.add(k.value)

# 2. Duplicate imports in cli.py
cli = ROOT / "kdesk" / "cli.py"
if cli.exists():
    lines = cli.read_text(encoding="utf-8").splitlines()
    imports = {}
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("from kdesk.") or stripped.startswith("import "):
            if stripped in imports:
                issues.append(f"DUP_IMPORT: cli.py:{i} '{stripped}' (first at line {imports[stripped]})")
            else:
                imports[stripped] = i

# 3. Unsafe git commands in executor read-only allowlist
executor = ROOT / "kdesk" / "executor.py"
if executor.exists():
    content = executor.read_text(encoding="utf-8", errors="ignore")
    for unsafe in ["config", "branch", "tag", "remote"]:
        if f'"{unsafe}"' in content and "read_only" in content.lower():
            # Check if it's in a read-only context
            for i, line in enumerate(content.splitlines(), 1):
                if f'"{unsafe}"' in line and any(w in line.lower() for w in ["allow", "safe", "readonly", "read_only"]):
                    issues.append(f"GIT_UNSAFE: executor.py:{i} allows 'git {unsafe}' as read-only")

# 4. Placeholder scores in fixer/diagnostics
for name in ["fixer.py", "diagnostics.py", "doctor.py"]:
    fp = ROOT / "kdesk" / name
    if fp.exists():
        content = fp.read_text(encoding="utf-8", errors="ignore")
        if "placeholder" in content.lower() and "score" in content.lower():
            for i, line in enumerate(content.splitlines(), 1):
                if "placeholder" in line.lower() or ("score" in line.lower() and "= 0" in line):
                    issues.append(f"PLACEHOLDER: {name}:{i} {line.strip()[:80]}")

print(f"Found {len(issues)} issues:")
for issue in issues:
    print(f"  {issue}")
