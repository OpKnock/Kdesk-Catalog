"""Phase G: transactional installer tests (copy-based contract)."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from kdesk.adapters import AdapterRegistry  # noqa: E402
from kdesk.installer import Installer, InstallError  # noqa: E402


@pytest.fixture
def root(tmp_path):
    return tmp_path / "root"


@pytest.fixture
def proj(tmp_path):
    return tmp_path / "proj"


@pytest.fixture
def home(tmp_path):
    return tmp_path / "home"


@pytest.fixture
def registry(root):
    return AdapterRegistry(root)


@pytest.fixture
def cursor_output(root):
    out = root / "platform-agents" / "cursor"
    out.mkdir(parents=True)
    (out / "a.mdc").write_text("hello", encoding="utf-8")
    (out / "b.mdc").write_text("world", encoding="utf-8")
    return out


def _installer(registry, proj, home=None, dry_run=False):
    return Installer(registry, dry_run=dry_run, base=proj, home_dir=home)


# -------------------------------------------------------------- errors
def test_installer_unknown_platform(registry, proj):
    with pytest.raises(InstallError):
        _installer(registry, proj).install("ghost")


def test_installer_void_not_installable(registry, proj):
    with pytest.raises(InstallError):
        _installer(registry, proj).install("void")


def test_installer_missing_output(registry, proj):
    with pytest.raises(InstallError):
        _installer(registry, proj).install("windsurf")


# ---------------------------------------------------------------- install
def test_install_dry_run(registry, proj, cursor_output):
    result = _installer(registry, proj, dry_run=True).install(
        "cursor", target="project", base=proj)
    assert result["results"][0]["status"] == "DRY-RUN"
    assert not (proj / ".cursor" / "rules" / "a.mdc").exists()


def test_install_actual_and_idempotent(registry, proj, cursor_output):
    installer = _installer(registry, proj)
    result = installer.install("cursor", target="project", base=proj)
    assert result["results"][0]["status"] == "OK"
    assert result["results"][0]["copied"] == 2
    assert (proj / ".cursor" / "rules" / "a.mdc").read_text(encoding="utf-8") == "hello"
    assert (proj / ".cursor" / "rules" / "b.mdc").read_text(encoding="utf-8") == "world"
    result2 = installer.install("cursor", target="project", base=proj)
    assert result2["results"][0]["copied"] == 0
    assert result2["results"][0]["status"] == "OK"


def test_install_records_manifest(registry, proj, cursor_output):
    installer = _installer(registry, proj)
    installer.install("cursor", target="project", base=proj)
    manifest_path = proj / ".kdesk" / "manifest.json"
    assert manifest_path.is_file()
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert ".cursor/rules/a.mdc" in data["installs"]["cursor"]["targets"]
    assert data["installs"]["cursor"]["targets"][".cursor/rules/a.mdc"]


def test_install_tilde_goes_home(registry, proj, home):
    out = registry.root / "platform-agents" / "claude_code"
    (out / ".claude" / "agents" / "x.md").mkdir(parents=True)
    (out / ".claude" / "agents" / "x.md" / "a.md").write_text("hi",
                                                             encoding="utf-8")
    result = _installer(registry, proj, home=home).install(
        "claude_code", target="home", base=proj)
    assert result["results"][0]["destination"].startswith(str(home))
    assert (home / ".claude" / "agents" / "x.md" / "a.md").is_file()


# -------------------------------------------------------------- uninstall
def test_uninstall_removes_files_and_entry(registry, proj, cursor_output):
    installer = _installer(registry, proj)
    installer.install("cursor", target="project", base=proj)
    result = installer.uninstall("cursor", base=proj)
    assert result["removed"][0]["status"] == "removed"
    assert not (proj / ".cursor" / "rules" / "a.mdc").exists()
    assert installer.manifest.entry("cursor") is None


def test_uninstall_not_installed_raises(registry, proj, cursor_output):
    with pytest.raises(InstallError):
        _installer(registry, proj).uninstall("cursor", base=proj)


def test_uninstall_dry_run_keeps_files(registry, proj, cursor_output):
    installer = _installer(registry, proj)
    installer.install("cursor", target="project", base=proj)
    result = _installer(registry, proj, dry_run=True).uninstall("cursor", base=proj)
    assert result["removed"][0]["status"] == "removed"
    assert (proj / ".cursor" / "rules" / "a.mdc").is_file()


# ------------------------------------------------------------------ drift
def test_drift_clean_after_install(registry, proj, cursor_output):
    installer = _installer(registry, proj)
    installer.install("cursor", target="project", base=proj)
    report = installer.drift(base=proj)
    assert report["clean"] is True


def test_drift_detects_missing_file(registry, proj, cursor_output):
    installer = _installer(registry, proj)
    installer.install("cursor", target="project", base=proj)
    (proj / ".cursor" / "rules" / "a.mdc").unlink()
    report = installer.drift("cursor", base=proj)
    assert report["clean"] is False
    assert ".cursor/rules/a.mdc" in report["platforms"]["cursor"]["missing"]


def test_drift_detects_modified_file(registry, proj, cursor_output):
    installer = _installer(registry, proj)
    installer.install("cursor", target="project", base=proj)
    (proj / ".cursor" / "rules" / "a.mdc").write_text("tampered", encoding="utf-8")
    report = installer.drift("cursor", base=proj)
    assert report["clean"] is False
    assert ".cursor/rules/a.mdc" in report["platforms"]["cursor"]["modified"]


def test_drift_unknown_platform_raises(registry, proj):
    with pytest.raises(InstallError):
        _installer(registry, proj).drift("ghost", base=proj)


# --------------------------------------------------------------- rollback
def test_rollback_restores_backup(registry, proj, cursor_output):
    installer = _installer(registry, proj)
    installer.install("cursor", target="project", base=proj)
    (registry.root / "platform-agents" / "cursor" / "a.mdc").write_text(
        "hello v2", encoding="utf-8")
    installer.install("cursor", target="project", base=proj)
    assert (proj / ".cursor" / "rules" / "a.mdc").read_text(
        encoding="utf-8") == "hello v2"
    result = installer.rollback("cursor", base=proj)
    assert result["restored"][0]["status"] == "restored"
    assert (proj / ".cursor" / "rules" / "a.mdc").read_text(
        encoding="utf-8") == "hello"


def test_rollback_no_backup_skips(registry, proj, cursor_output):
    installer = _installer(registry, proj)
    installer.install("cursor", target="project", base=proj)
    result = installer.rollback("cursor", base=proj)
    assert result["restored"][0]["status"] == "no-backup"


def test_rollback_not_installed_raises(registry, proj):
    with pytest.raises(InstallError):
        _installer(registry, proj).rollback("cursor", base=proj)


# ----------------------------------------------------------------- status
def test_status_counts(registry, proj, cursor_output):
    installer = _installer(registry, proj)
    installer.install("cursor", target="project", base=proj)
    status = installer.status(base=proj)
    assert status["installs"] == 1
    assert status["rows"][0]["platform"] == "cursor"
    assert status["rows"][0]["targets"] == 2


def test_status_empty(registry, proj):
    assert _installer(registry, proj).status(base=proj)["installs"] == 0