#!/usr/bin/env python3
"""
Smoke test for clean installation.
Tests that the package installs and CLI can locate catalog data from repo root.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def run(cmd: list, cwd: Path = ROOT, timeout: int = 120) -> subprocess.CompletedProcess:
    print(f"  Running: {cmd} (cwd={cwd}, timeout={timeout})")
    # Use capture_output=True but ensure arguments are passed as a list
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    print(f"  Return code: {result.returncode}")
    if result.stdout:
        print(f"  STDOUT: {result.stdout[:200]}")
    if result.stderr:
        print(f"  STDERR: {result.stderr[:500]}")
    return result

def main() -> int:
    print("Building package...")
    result = run([sys.executable, "-m", "build"])
    if result.returncode != 0:
        print(f"Build failed: {result.stderr}")
        return 1

    # Find the wheel
    wheels = list((ROOT / "dist").glob("*.whl"))
    if not wheels:
        print("No wheel found in dist/")
        return 1
    wheel = wheels[0]
    print(f"Built: {wheel.name}")

    # Install in a clean virtual environment
    with tempfile.TemporaryDirectory() as tmpdir:
        venv_dir = Path(tmpdir) / "venv"
        print(f"Creating venv at {venv_dir}")
        result = run([sys.executable, "-m", "venv", str(venv_dir)])
        if result.returncode != 0:
            print(f"Venv creation failed: {result.stderr}")
            return 1

        pip = venv_dir / "Scripts" / "pip.exe"
        python = venv_dir / "Scripts" / "python.exe"

        print("Installing package in clean venv...")
        result = run([str(pip), "install", str(wheel)])
        if result.returncode != 0:
            print(f"Install failed: {result.stderr}")
            return 1

        # Test CLI with repo root
        print("Testing CLI with --root pointing to repo...")
        # Use python -m kdesk.cli instead of kdesk.exe to avoid Windows argument passing issues
        python_exe = venv_dir / "Scripts" / "python.exe"
        print(f"  ROOT: {ROOT}")
        print(f"  python: {python_exe}")
        cmd = [str(python_exe), "-m", "kdesk.cli", "stats", "--root", str(ROOT), "--format", "json", "--fast"]
        print(f"  cmd: {cmd}")
        result = run(cmd, timeout=120)
        if result.returncode != 0:
            print(f"CLI smoke test failed: {result.stderr}")
            return 1

        import json
        stats = json.loads(result.stdout)
        if stats.get("agents") != 1766 or stats.get("skills") != 1143:
            print(f"Stats mismatch: {stats}")
            return 1

        print("CLI smoke test passed!")
        print(f"  Agents: {stats['agents']}")
        print(f"  Skills: {stats['skills']}")
        print(f"  Total: {stats['definitions_total']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())