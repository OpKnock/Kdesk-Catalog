"""kdesk unit tests: adapters, installer, doctor, security, provenance, quality, license, duplicates."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest

from kdesk.adapters import AdapterRegistry, SupportLevel
from kdesk.doctor import Doctor
from kdesk.duplicates import DuplicateDetector
from kdesk.installer import Installer, InstallError
from kdesk.license import LicenseAudit
from kdesk.provenance import Provenance, verify_wiring
from kdesk.quality import QualityReport
from kdesk.registry import Catalog
from kdesk.security import SecurityScanner


# ---------------------------------------------------------------- adapters
def test_adapter_registry_45_platforms(tmp_path):
    reg = AdapterRegistry(tmp_path)
    assert len(reg.names()) == 45
    assert reg.get("claude_code") is not None
    assert reg.get("void") is not None


def test_adapter_support_levels(tmp_path):
    reg = AdapterRegistry(tmp_path)
    assert reg.get("claude_code").support_level == SupportLevel.SUPPORTED
    assert reg.get("codegpt").support_level == SupportLevel.PARTIALLY_SUPPORTED


def test_adapter_verify_missing(tmp_path):
    reg = AdapterRegistry(tmp_path)
    v = reg.get("cursor").verify()
    assert v["status"] == "MISSING"
    assert v["scanned_files"] == 0


def test_adapter_verify_present(tmp_path):
    reg = AdapterRegistry(tmp_path)
    out = tmp_path / "platform-agents" / "cursor"
    (out / "rules").mkdir(parents=True)
    (out / "rules" / "a.mdc").write_text("---\ndescription: x\n---\nbody", encoding="utf-8")
    v = reg.get("cursor").verify()
    assert v["status"] == "OK"
    assert v["items"] == 1


# ---------------------------------------------------------------- installer
def test_installer_unknown_platform(tmp_path):
    reg = AdapterRegistry(tmp_path)
    with pytest.raises(InstallError):
        Installer(reg).install("ghost")


def test_installer_dry_run_and_actual(tmp_path):
    reg = AdapterRegistry(tmp_path)
    out = tmp_path / "platform-agents" / "cursor"
    out.mkdir(parents=True)
    (out / "a.mdc").write_text("hello", encoding="utf-8")
    installer = Installer(reg, dry_run=True)
    result = installer.install("cursor", target="project", base=tmp_path / "proj")
    assert result["results"][0]["status"] == "DRY-RUN"
    installer = Installer(reg, dry_run=False)
    result = installer.install("cursor", target="project", base=tmp_path / "proj")
    assert result["results"][0]["status"] == "OK"
    assert (tmp_path / "proj" / ".cursor" / "rules" / "a.mdc").read_text(encoding="utf-8") == "hello"
    # idempotent second run
    result2 = installer.install("cursor", target="project", base=tmp_path / "proj")
    assert result2["results"][0]["copied"] == 0


def test_installer_void_not_installable(tmp_path):
    reg = AdapterRegistry(tmp_path)
    with pytest.raises(InstallError):
        Installer(reg).install("void")


# ---------------------------------------------------------------- doctor
def test_doctor_not_generated(tmp_path):
    reg = AdapterRegistry(tmp_path)
    assert Doctor(reg, base=tmp_path).check("cursor")["status"] == "NOT_GENERATED"


def test_doctor_ok_after_install(tmp_path):
    reg = AdapterRegistry(tmp_path)
    out = tmp_path / "platform-agents" / "cursor" / "rules"
    out.mkdir(parents=True)
    (out / "a.mdc").write_text("x", encoding="utf-8")
    (tmp_path / "proj" / ".cursor" / "rules").mkdir(parents=True)
    (tmp_path / "proj" / ".cursor" / "rules" / "a.mdc").write_text("x", encoding="utf-8")
    check = Doctor(reg, base=tmp_path / "proj").check("cursor")
    assert check["status"] == "OK"
    assert check["scanned_files"] >= 1


def test_doctor_empty_never_ok(tmp_path):
    reg = AdapterRegistry(tmp_path)
    out = tmp_path / "platform-agents" / "cursor" / "rules"
    out.mkdir(parents=True)
    assert Doctor(reg, base=tmp_path).check("cursor")["status"] == "EMPTY"


# ---------------------------------------------------------------- security
def _catalog_with(tmp_path, **kwargs):
    base = tmp_path / "universal-agents"
    (base / "devops" / "agent").mkdir(parents=True)
    body = f"name: {kwargs.get('name', 'agent-a')}\ncategory: devops\n"
    body += f"description: {kwargs.get('description', 'x' * 250)}\ntype: agent\n"
    body += "capabilities:\n  - name: run\n    description: run\n    commands: ['helm lint']\n"
    (base / "devops" / "agent" / "a.yaml").write_text(body, encoding="utf-8")
    return Catalog(base)


def test_security_scanner_clean(tmp_path):
    catalog = _catalog_with(tmp_path)
    assert SecurityScanner(catalog).scan() == []


def test_security_scanner_finds_secret(tmp_path):
    catalog = _catalog_with(tmp_path, description=("x" * 199) + " sk-ABCDEFGHIJKLMNOPQRSTUVWXYZ123456")
    findings = SecurityScanner(catalog).scan()
    assert any(f["pattern"] == "api_key" for f in findings)
    assert findings[0]["severity"] == "HIGH"


# ---------------------------------------------------------------- provenance
def test_provenance_verify_missing_provenance(tmp_path):
    catalog = _catalog_with(tmp_path, name="agent-a")
    agents_dir = tmp_path / "agents" / "json"
    agents_dir.mkdir(parents=True)
    (agents_dir / "agent-a.json").write_text(json.dumps({"name": "agent-a"}), encoding="utf-8")
    result = Provenance(tmp_path).verify()
    assert not result["verified"]
    assert any("missing _provenance.source" in p for p in result["problems"])


def test_provenance_verify_ok(tmp_path):
    catalog = _catalog_with(tmp_path, name="agent-a")
    src = catalog.agents["agent-a"].source_path
    agents_dir = tmp_path / "agents" / "json"
    agents_dir.mkdir(parents=True)
    checksum = Provenance.sha256(src)
    (agents_dir / "agent-a.json").write_text(
        json.dumps(
            {
                "name": "agent-a",
                "_provenance": {
                    "source": str(src.relative_to(tmp_path)).replace("\\", "/"),
                    "checksum": checksum,
                },
            }
        ),
        encoding="utf-8",
    )
    result = Provenance(tmp_path).verify()
    assert result["verified"]


def test_provenance_checksum_mismatch(tmp_path):
    catalog = _catalog_with(tmp_path, name="agent-a")
    src = catalog.agents["agent-a"].source_path
    agents_dir = tmp_path / "agents" / "json"
    agents_dir.mkdir(parents=True)
    (agents_dir / "agent-a.json").write_text(
        json.dumps(
            {
                "_provenance": {
                    "source": str(src.relative_to(tmp_path)).replace("\\", "/"),
                    "checksum": "deadbeef",
                }
            }
        ),
        encoding="utf-8",
    )
    result = Provenance(tmp_path).verify()
    assert not result["verified"]
    assert any("checksum mismatch" in p for p in result["problems"])


def test_verify_wiring(tmp_path):
    wiring = tmp_path / "skills" / "wiring.json"
    wiring.parent.mkdir(parents=True)
    wiring.write_text(
        json.dumps(
            {
                "version": "1.0.0",
                "wiring": {
                    "a": [{"skill": "s", "evidence": ["helm"], "score": 0.9}],
                    "b": [{"skill": "s", "manual": True}],
                },
            }
        ),
        encoding="utf-8",
    )
    assert verify_wiring(tmp_path)["verified"]
    wiring.write_text(
        json.dumps({"version": "1.0.0", "wiring": {"a": [{"skill": "s"}]}}),
        encoding="utf-8",
    )
    result = verify_wiring(tmp_path)
    assert not result["verified"]


# ---------------------------------------------------------------- quality
def test_quality_scoring(tmp_path):
    catalog = _catalog_with(tmp_path)
    report = QualityReport(catalog).score()
    assert report["definitions"] == 1
    assert report["files_scanned"] == 1
    assert report["scores"][0]["score"] >= 3


# ---------------------------------------------------------------- license
def test_license_audit(tmp_path):
    catalog = _catalog_with(tmp_path)
    report = LicenseAudit(catalog).audit()
    assert report["definitions"] == 1
    assert report["missing_count"] == 1


# ---------------------------------------------------------------- duplicates
def test_duplicate_detector(tmp_path):
    catalog = _catalog_with(tmp_path)
    assert DuplicateDetector(catalog).detect()["family_count"] == 0
    base = tmp_path / "universal-agents" / "devops" / "agent"
    (base / "b.yaml").write_text(
        (base / "a.yaml").read_text(encoding="utf-8").replace("agent-a", "agent-b"),
        encoding="utf-8",
    )
    catalog = Catalog(tmp_path / "universal-agents")
    assert DuplicateDetector(catalog).detect()["family_count"] == 1