"""Phase I: CLI installer lifecycle + exit-code semantics (subprocess)."""
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest  # noqa: E402

CLI = str(Path(__file__).resolve().parents[1] / "kdesk" / "cli.py")
REPO = str(Path(__file__).resolve().parents[1])


def _run(args, cwd):
    env = dict(os.environ)
    env["PYTHONPATH"] = REPO + os.pathsep + env.get("PYTHONPATH", "")
    return subprocess.run(
        [sys.executable, CLI] + args,
        capture_output=True, text=True, cwd=str(cwd), env=env, timeout=120)


@pytest.fixture()
def repo(tmp_path):
    import shutil
    REPO = str(Path(__file__).resolve().parents[1])
    # Copy the real universal-agents to the temp repo
    shutil.copytree(Path(REPO) / "universal-agents", tmp_path / "universal-agents")
    (tmp_path / "platform-agents" / "cursor").mkdir(parents=True)
    (tmp_path / "platform-agents" / "cursor" / "review.mdc").write_text(
        "---\ndescription: review\n---\nReview.\n", encoding="utf-8")
    return tmp_path


def test_cli_install_then_status_doctor_ok(repo):
    r = _run(["install", "cursor", "--root", str(repo), "--base", str(repo)],
             repo)
    assert r.returncode == 0
    data = json.loads(r.stdout)
    assert data["results"][0]["copied"] == 1

    r = _run(["status", "--root", str(repo), "--base", str(repo)], repo)
    assert r.returncode == 0
    assert json.loads(r.stdout)["installs"] == 1

    r = _run(["doctor", "--platform", "cursor", "--root", str(repo),
              "--base", str(repo)], repo)
    assert r.returncode == 0
    assert json.loads(r.stdout)["status"] == "OK"


def test_cli_drift_exit_3_when_tampered(repo):
    r = _run(["install", "cursor", "--root", str(repo), "--base", str(repo)],
             repo)
    assert r.returncode == 0
    (repo / ".cursor" / "rules" / "review.mdc").write_text(
        "tampered", encoding="utf-8")
    r = _run(["drift", "--root", str(repo), "--base", str(repo)], repo)
    assert r.returncode == 3
    assert json.loads(r.stdout)["clean"] is False


def test_cli_drift_clean_exit_0(repo):
    r = _run(["install", "cursor", "--root", str(repo), "--base", str(repo)],
             repo)
    assert r.returncode == 0
    r = _run(["drift", "--root", str(repo), "--base", str(repo)], repo)
    assert r.returncode == 0
    assert json.loads(r.stdout)["clean"] is True


def test_cli_uninstall_removes(repo):
    r = _run(["install", "cursor", "--root", str(repo), "--base", str(repo)],
             repo)
    assert r.returncode == 0
    r = _run(["uninstall", "cursor", "--root", str(repo), "--base", str(repo)],
             repo)
    assert r.returncode == 0
    assert not (repo / ".cursor" / "rules").exists()
    assert json.loads(r.stdout)["removed"][0]["status"] == "removed"


def test_cli_uninstall_not_installed_exit_1(repo):
    r = _run(["uninstall", "cursor", "--root", str(repo), "--base", str(repo)],
             repo)
    assert r.returncode == 1
    assert "not installed" in r.stdout


def test_cli_rollback_restores_backup(repo):
    r = _run(["install", "cursor", "--root", str(repo), "--base", str(repo)],
             repo)
    assert r.returncode == 0
    (repo / "platform-agents" / "cursor" / "review.mdc").write_text(
        "hello v2\n", encoding="utf-8")
    r = _run(["install", "cursor", "--root", str(repo), "--base", str(repo)],
             repo)
    assert r.returncode == 0
    target = repo / ".cursor" / "rules" / "review.mdc"
    assert target.read_text(encoding="utf-8") == "hello v2\n"
    r = _run(["rollback", "cursor", "--root", str(repo), "--base", str(repo)],
             repo)
    assert r.returncode == 0
    assert json.loads(r.stdout)["restored"][0]["status"] == "restored"
    assert target.read_text(encoding="utf-8") == "---\ndescription: review\n---\nReview.\n"


def test_cli_install_home_target(repo):
    home = repo / "home"
    r = _run(["install", "cursor", "--root", str(repo), "--base", str(repo),
              "--target", "home", "--home", str(home)], repo)
    assert r.returncode == 0
    assert (home / ".cursor" / "rules" / "review.mdc").is_file()