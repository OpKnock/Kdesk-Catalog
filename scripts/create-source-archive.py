#!/usr/bin/env python3
"""Create a clean SOURCE archive (ZIP) of the repository.

Excludes generated/development/runtime artifacts:

    .git/
    .pytest_cache/
    __pycache__/
    *.pyc
    dist/
    build/
    *.egg-info/
    .kdesk/runtime/
    agents/ (generated JSON)
    skills/ (generated JSON)
    workflows/ (generated JSON)
    platform-agents/ (generated platform output)
    marketplaces/ (generated manifests)
    reports/ (generated reports)

Keeps only source files:
    universal-agents/ (source YAML definitions)
    kdesk/ (Python package source)
    scripts/ (Python scripts)
    tests/ (test files)
    pyproject.toml
    README.md
    .gitignore
    divisions.json
    docs/
    .github/
    CONTRIBUTING.md
    AGENTS.md
    LICENSE
"""
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "dist"
OUT_NAME = "Kdesk-Catalog-source.zip"

EXCLUDED_DIRS = {
    ".git",
    ".pytest_cache",
    "__pycache__",
    "dist",
    "build",
    ".venv",
    "venv",
    ".idea",
    ".vscode",
    "kdesk.egg-info",
    "agents",
    "skills",
    "workflows",
    "platform-agents",
    "marketplaces",
    "reports",
}

EXCLUDED_SUFFIXES = {".pyc", ".pyo"}
EXCLUDED_NAMES = {".DS_Store", "Thumbs.db"}


def excluded(rel: Path) -> bool:
    parts = rel.parts
    # Only exclude root-level directories (first part)
    if parts:
        first = parts[0]
        if first in EXCLUDED_DIRS or first.endswith(".egg-info"):
            return True
        if first == "__pycache__":
            return True
    # Check for .kdesk/runtime at any level
    if len(parts) >= 2 and parts[0] == ".kdesk" and parts[1] == "runtime":
        return True
    if rel.suffix in EXCLUDED_SUFFIXES:
        return True
    if rel.name in EXCLUDED_NAMES:
        return True
    return False


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / OUT_NAME
    if out_path.exists():
        out_path.unlink()

    files = sorted(
        (p.relative_to(ROOT) for p in ROOT.rglob("*") if p.is_file() and not excluded(p.relative_to(ROOT))),
        key=lambda r: r.as_posix(),
    )

    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for rel in files:
            zf.write(ROOT / rel, rel.as_posix())

    print(f"Wrote {out_path} ({len(files)} files)")

    bad = []
    for rel in files:
        r = rel.as_posix()
        if any(
            r.startswith(n + "/")
            or r.endswith(".pyc")
            or "/__pycache__/" in r
            or ".kdesk/runtime/" in r
            or r.endswith(".egg-info/")
            for n in [".git", ".pytest_cache", "__pycache__", "dist", "build", "agents", "skills", "workflows", "platform-agents", "marketplaces", "reports"]
        ):
            # Only flag if it's a root-level exclusion
            first_part = r.split("/")[0] if "/" in r else r
            if first_part in [".git", ".pytest_cache", "__pycache__", "dist", "build", "agents", "skills", "workflows", "platform-agents", "marketplaces", "reports"]:
                bad.append(r)
    if bad:
        print(f"ERROR: archive contains excluded entries: {bad[:20]}")
        return 1

    print("Source archive contents verified clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())