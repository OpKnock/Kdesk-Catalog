#!/usr/bin/env python3
"""Create a clean release archive (ZIP) of the repository.

Excludes development/runtime artifacts:

    .git/
    .pytest_cache/
    __pycache__/
    *.pyc
    dist/
    build/
    *.egg-info/
    .kdesk/runtime/

Keeps source files, catalog content, schemas, scripts, package files,
documentation, and generated marketplace/platform output.
"""
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "dist"
OUT_NAME = "kdesk-catalog-release.zip"

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
}

EXCLUDED_SUFFIXES = {".pyc", ".pyo"}
EXCLUDED_NAMES = {".DS_Store", "Thumbs.db"}


def excluded(rel: Path) -> bool:
    parts = rel.parts
    for p in parts:
        if p in EXCLUDED_DIRS or p.endswith(".egg-info"):
            return True
        if p == "__pycache__":
            return True
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
            for n in [".git", ".pytest_cache", "__pycache__", "dist", "build"]
        ):
            bad.append(r)
    if bad:
        print(f"ERROR: archive contains excluded entries: {bad[:20]}")
        return 1

    print("Archive contents verified clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
