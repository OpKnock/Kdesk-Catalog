#!/usr/bin/env python3
"""
Smoke test for clean installation of Kdesk.

Kdesk is a repository-backed tool - it requires a catalog repository (with
universal-agents/) to operate. The package provides the CLI/runtime, while the
catalog data lives in a separate repository.

This test verifies:
1. The package builds and installs correctly in a clean environment
2. The installed CLI can be invoked and loads a catalog repository correctly
3. The installed package is used (not the source tree)
4. The CLI fails appropriately when no catalog repository is provided
"""
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run(cmd: list, cwd: Path = None, timeout: int = 120) -> subprocess.CompletedProcess:
    cwd = cwd or Path(__file__).resolve().parent.parent
    print(f"  Running: {cmd} (cwd={cwd}, timeout={timeout})")
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
        python_exe = venv_dir / "Scripts" / "python.exe"

        print("Installing package in clean venv...")
        result = run([str(pip), "install", str(wheel)])
        if result.returncode != 0:
            print(f"Install failed: {result.stderr}")
            return 1

        # Verify the installed package location
        print("Verifying installed package location...")
        # Run from temp directory to avoid importing from source tree
        test_cwd = Path(tmpdir)
        result = run([str(python_exe), "-c", "import kdesk; print(kdesk.__file__)"], cwd=test_cwd)
        if result.returncode != 0:
            print(f"Failed to import installed kdesk: {result.stderr}")
            return 1
        installed_path = result.stdout.strip()
        print(f"  Installed kdesk at: {installed_path}")
        if "site-packages" not in installed_path:
            print(f"ERROR: kdesk imported from source tree, not installed package!")
            return 1
        print("  OK: kdesk imported from installed package")

        # Test 1: CLI with --root pointing to repo (repository-backed mode)
        print("\nTest 1: CLI with --root pointing to catalog repository...")
        cmd = [str(python_exe), "-m", "kdesk.cli", "stats", "--root", str(ROOT), "--format", "json", "--fast"]
        print(f"  cmd: {cmd}")
        result = run(cmd, timeout=120, cwd=test_cwd)
        if result.returncode != 0:
            print(f"CLI smoke test failed: {result.stderr}")
            return 1

        import json
        stats = json.loads(result.stdout)
        if stats.get("agents") != 1766 or stats.get("skills") != 1143:
            print(f"Stats mismatch: {stats}")
            return 1

        print("  Test 1 passed!")
        print(f"  Agents: {stats['agents']}")
        print(f"  Skills: {stats['skills']}")
        print(f"  Total: {stats['definitions_total']}")

        # Test 2: CLI without --root should fail (no catalog packaged)
        print("\nTest 2: CLI without --root should fail (no catalog packaged)...")
        result = run([str(python_exe), "-m", "kdesk.cli", "stats", "--format", "json", "--fast"], cwd=test_cwd)
        if result.returncode == 0:
            print(f"ERROR: CLI should fail without catalog repository")
            return 1
        if "universal-agents directory not found" not in result.stderr:
            print(f"ERROR: Expected 'universal-agents directory not found' error, got: {result.stderr}")
            return 1
        print("  Test 2 passed! CLI correctly fails without catalog repository.")

    print("\n=== ALL SMOKE TESTS PASSED ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())